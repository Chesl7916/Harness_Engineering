# 🛠️ Harness_Engineering - Build apps with guided automation

[![Download Harness_Engineering](https://img.shields.io/badge/Download-Harness_Engineering-2ea44f?style=for-the-badge&logo=github)](https://github.com/Chesl7916/Harness_Engineering)

## 📥 Download

Visit this page to download and run the project on Windows:

[https://github.com/Chesl7916/Harness_Engineering](https://github.com/Chesl7916/Harness_Engineering)

## 🧭 What this project does

Harness_Engineering is a teaching project that shows how a multi-agent app can work from start to finish. You give it one task, and it can move through planning, code writing, browser testing, review, and fixes without you guiding each step.

It is built with plain Python and an OpenAI-style API. It does not need an agent SDK. That makes it easier to study and easier to connect to different model providers.

Use it when you want to:

- turn one short idea into a working app
- see how an autonomous build loop works
- test a simple app in a browser
- learn how product planning and coding can fit into one flow

## 🪟 Windows setup

Follow these steps on Windows:

1. Open the download page:
   [https://github.com/Chesl7916/Harness_Engineering](https://github.com/Chesl7916/Harness_Engineering)

2. Download the project files.

3. Install Python 3.10 or newer if it is not already on your PC.

4. Open File Explorer and find the project folder.

5. Open PowerShell in that folder.

6. Install the required Python packages:

   pip install -r requirements.txt

7. If you want browser testing, install Chromium for Playwright:

   python -m playwright install chromium

8. Copy the example environment file:

   copy .env.template .env

9. Open `.env` in Notepad and add your API key.

10. Run the app with a short task:

    python harness.py "Build a Pomodoro timer with start, pause, reset buttons. Single HTML file."

## 🧰 What you need

Use a Windows PC with:

- Windows 10 or Windows 11
- Python 3.10 or newer
- Internet access
- An API key from a model provider that works with OpenAI-style requests
- About 2 GB of free disk space
- Chromium if you want browser tests

## 🚀 First run

The first run can take a while because the app may:

- plan the task
- write files
- open a browser for testing
- review the result
- make changes and test again

For best results, give it a clear goal with a single app or page. Short tasks are easier to finish in one run.

Example prompts:

- Build a habit tracker with daily checkboxes
- Build a note app with search and tags
- Build a calculator with a clean layout
- Build a simple study timer with sound alert

## 🔑 Set up your API key

Harness_Engineering needs an API key to talk to a model provider.

1. Open the `.env` file.
2. Add your key in the field shown in the template.
3. Save the file.
4. Run the project again.

Keep the key private and do not share it in chat, screenshots, or public posts.

## 🧪 Browser testing

The project can test the app in Chromium through Playwright.

Use browser testing when you want to check:

- button clicks
- form input
- page layout
- popup behavior
- basic page flow

If browser testing is not set up, the project can still write code, but the test loop may be limited.

## 📚 How it works

The app follows a simple loop:

1. Take your task
2. Turn it into a plan
3. Set acceptance rules
4. Write the app
5. Open the result in a browser
6. Score the result
7. Fix problems
8. Repeat until the task is done

This mirrors the design ideas from the Anthropic article and shows them in runnable code.

## 🧩 Main parts

- `harness.py` — starts the workflow
- planning step — turns your idea into a build plan
- acceptance step — defines what counts as done
- coding step — writes the app files
- test step — checks the app in a browser
- review step — compares the result to the goal
- iteration step — makes fixes and runs again

## 📝 Good task examples

Use tasks that are:

- clear
- short
- focused on one app
- easy to test in a browser
- possible in a single HTML file or a small set of files

Good examples:

- a landing page with a contact form
- a todo list with filters
- a timer with start and stop controls
- a simple game with score tracking
- a chart page that loads sample data

Harder tasks:

- large business systems
- many connected pages
- login flows with backend accounts
- apps that need a database
- tasks with vague goals

## 🧯 Common Windows fixes

If PowerShell says Python is not found:

- install Python from python.org
- check the box that adds Python to PATH
- open a new PowerShell window

If `pip install` fails:

- upgrade pip with `python -m pip install --upgrade pip`
- try the command again

If Playwright browser setup fails:

- run `python -m playwright install chromium` again
- check your internet connection
- restart PowerShell and retry

If the app cannot use your API key:

- open `.env`
- confirm the key is pasted in the right field
- save the file
- run the command again

## 📄 Project focus

This repository is built for learning and testing. It is not a full product framework. It shows how an autonomous build loop can work in code, with a clear path from a user request to a browser-tested result

## 🔗 Topic tags

- agent
- harness-engineering
- tutorial