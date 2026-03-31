"""
Harbor adapter — runs our harness agent on Terminal-Bench 2.0 via Harbor framework.

Harbor has two agent types:
  - External (BaseAgent): agent runs outside container, sends commands via environment.exec()
  - Installed (BaseInstalledAgent): agent is installed inside the container

We use Installed agent — our harness.py runs natively inside the container,
so run_bash just works as subprocess without any bridging.

Usage:
  # Install harbor
  pip install harbor

  # Test on hello-world task
  harbor run -d "terminal-bench@2.0" \
    --agent-import-path benchmarks.harbor_agent:HarnessAgent \
    --task-names hello-world

  # Full benchmark
  harbor run -d "terminal-bench@2.0" \
    --agent-import-path benchmarks.harbor_agent:HarnessAgent

  # With Daytona (no Docker needed locally)
  harbor run -d "terminal-bench@2.0" \
    --agent-import-path benchmarks.harbor_agent:HarnessAgent \
    --env daytona
"""
from __future__ import annotations

import os
import shlex
from pathlib import Path

from harbor.agents.installed.base import BaseInstalledAgent, with_prompt_template
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext


class HarnessAgent(BaseInstalledAgent):
    """
    Installs our harness inside the Harbor container and runs it
    with --profile terminal for each task.
    """

    @staticmethod
    def name() -> str:
        return "harness-agent"

    def __init__(self, model_name: str | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model_name = model_name

    async def install(self, environment: BaseEnvironment) -> None:
        """Install dependencies and clone our repo into the container.

        Key challenges in TB2 environments:
        - Some images lack pip3 (only have python3)
        - dpkg lock contention with verifier setup scripts
        - Daytona Tier 2 network restrictions may slow apt-get

        Strategy:
        1. Wait for any concurrent dpkg operations to finish
        2. Clone repo (git is available in most images)
        3. Try pip install via multiple fallback paths
        4. Only use apt-get as absolute last resort, with timeout
        """
        # Step 1: Wait for dpkg lock (verifier setup may be running apt-get concurrently)
        # Then ensure git is available
        await self.exec_as_root(
            environment,
            command=(
                # Wait up to 60s for dpkg lock to be released
                "for i in $(seq 1 30); do "
                "  fuser /var/lib/dpkg/lock >/dev/null 2>&1 || break; "
                "  sleep 2; "
                "done; "
                # Ensure git exists
                "command -v git >/dev/null 2>&1 || "
                "( apt-get update -qq 2>/dev/null && "
                "  apt-get install -y -qq git 2>/dev/null ) || "
                "true"
            ),
        )

        # Step 2: Clone repo
        await self.exec_as_agent(
            environment,
            command=(
                "git clone --depth 1 "
                "https://github.com/lazyFrogLOL/Harness_Engineering.git "
                "/home/user/harness-agent"
            ),
        )

        # Step 3: Install Python deps — only openai is required (tiktoken is optional)
        # openai is a pure Python package (py3-none-any wheel), installs fast
        await self.exec_as_root(
            environment,
            command=(
                # Fast paths first (no apt-get needed)
                "( pip3 install --break-system-packages -q openai 2>/dev/null ) || "
                "( pip install --break-system-packages -q openai 2>/dev/null ) || "
                "( python3 -m pip install --break-system-packages -q openai 2>/dev/null ) || "
                # Try ensurepip to bootstrap pip
                "( python3 -m ensurepip --break-system-packages 2>/dev/null && "
                "  python3 -m pip install --break-system-packages -q openai 2>/dev/null ) || "
                # Last resort: wait for dpkg lock, then apt-get install pip
                "( for i in $(seq 1 30); do "
                "    fuser /var/lib/dpkg/lock >/dev/null 2>&1 || break; "
                "    sleep 2; "
                "  done && "
                "  apt-get update -qq 2>/dev/null && "
                "  apt-get install -y -qq python3-pip 2>/dev/null && "
                "  pip3 install --break-system-packages -q openai 2>/dev/null ) || "
                "true"
            ),
        )

    @with_prompt_template
    async def run(
        self,
        instruction: str,
        environment: BaseEnvironment,
        context: AgentContext,
    ) -> None:
        """Run our harness with --profile terminal on the given task."""
        escaped = shlex.quote(instruction)

        # Build env vars string for the command
        env_vars = []
        for key in ("OPENAI_API_KEY", "OPENAI_BASE_URL", "HARNESS_MODEL"):
            val = os.environ.get(key)
            if val:
                env_vars.append(f"{key}={shlex.quote(val)}")

        # Force workspace to /app so agent writes outputs where tests expect them
        env_vars.append("HARNESS_WORKSPACE=/app")
        # Skip subdirectory creation — outputs must land directly in /app
        env_vars.append("HARNESS_FLAT_WORKSPACE=1")

        env_prefix = " ".join(env_vars)

        await self.exec_as_agent(
            environment,
            command=(
                f"cd /home/user/harness-agent && "
                f"{env_prefix} "
                f"python3 harness.py --profile terminal {escaped}"
            ),
        )

    def populate_context_post_run(self, context: AgentContext) -> None:
        """Called after run() completes. Could parse logs if needed."""
        pass
