# CONTRIBUTING.md

Thank you for your interest in contributing to TeleQuest. This document will guide you through the process of setting up your development environment and submitting a pull request.

## Table of Contents
- [CONTRIBUTING.md](#contributingmd)
	- [Table of Contents](#table-of-contents)
	- [Setting Up Your Development Environment](#setting-up-your-development-environment)
		- [Requirements](#requirements)
		- [Getting Started](#getting-started)
	- [Working on the Bot](#working-on-the-bot)
	- [Working on the Web App](#working-on-the-web-app)
	- [Committing Changes](#committing-changes)
	- [Submitting a Pull Request](#submitting-a-pull-request)

## Setting Up Your Development Environment

### Requirements

Before you start contributing, make sure you have the following tools installed:

1. **VS Code**: We recommend using [Visual Studio Code (VS Code)](https://code.visualstudio.com/) as your code editor. It offers a rich set of extensions and integrated terminal which will make development smoother.

2. **Git**: This is essential for source code management. If you don't have Git installed, you can download and install it from [Git's official site](https://git-scm.com/).

### Getting Started

1. **Clone the Repository**: Clone the main repository to your local machine. We're avoiding forks to streamline the contribution process.

    ```bash
    git clone https://github.com/minerva-university/TeleQuest.git
    cd telequest
    ```

2. **Switch to the Development Branch**: Before you start making changes, ensure you're on the `dev` branch and have the latest updates. If you are already on the dev branch you don't need to run this first command. Please ensure that you pull from the dev branchh before creating a new branch.

    ```bash
    git switch dev
    git pull origin dev
    ```

3. **Create a New Branch for Your Work**:

   It's a good practice to create a new branch for each new feature or bugfix. This keeps your changes organized and separated from the main development branch. For this project, we're keeping the branch naming convention as username/feature-name. For example, if your username is `johndoe` and you're working on a feature to add a new command, you would name your branch `johndoe/add-new-command`.

   ```bash
   git checkout -b username/feature-name
   ```

## Working on the Bot

If you want to get started with working on the Telegram bot, follow these steps:

1. **Change to the Bot Directory**:
   
   ```bash
   cd bot
   ```

2. **Installing Python**:

   - **Windows**:
     1. Download the latest version of Python from [Python's official site](https://www.python.org/downloads/windows/).
     2. Run the installer. Ensure that you check the option to add Python to PATH.
   - **Mac**:
     ```bash
     brew install python
     ```
   - **Linux (Ubuntu)**:
     ```bash
     sudo apt-get update
     sudo apt-get install python3 python3-pip
     ```

3. **Setting up a Virtual Environment**:

   First, install `virtualenv` if it's not already installed:

   ```bash
   pip install virtualenv
   ```

   Now, create a virtual environment named `.venv`:

   ```bash
   python3 -m venv .venv
   ```

   Activate the virtual environment:

   - **Windows**:
     ```bash
     .\.venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Installing Dependencies**:
   
   With the virtual environment activated, install the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```
Recommended: We will be using a Python-Telegram-API wrapper or package called [python-telegram-bot](https://python-telegram-bot.org/). You can [read the documentation](https://docs.python-telegram-bot.org/en/v20.6/) to get a better understanding of how to use it.

## Working on the Web App

1. **Change to the Web App Directory**:

   ```bash
   cd web
   ```

2. **Installing Node.js and npm**:

   - **Windows**: Download and install from [Node.js official site](https://nodejs.org/).
   - **Mac**:
     ```bash
     brew install node
     ```
   - **Linux (Ubuntu)**:
     ```bash
     sudo apt-get update
     sudo apt-get install nodejs npm
     ```

3. **Installing JavaScript Dependencies**:

   ```bash
   npm install
   ```

## Committing Changes

1. Create a new branch:

   ```bash
   git checkout -b username/feature-name
   ```

2. Make your changes and then commit them:

   ```bash
   git add .
   git commit -m "YOUR COMMIT MESSAGE HERE"
   ```

3. Push the changes to your fork:

   ```bash
   git push origin username/feature-name
   ```

## Submitting a Pull Request

1. Navigate to the main repository you forked.
2. Click on "Pull requests" and then the "New Pull Request" button.
3. Select your branch from the dropdown and submit your pull request.
4. On the right side of the screen, request a review from someone on the team.
5. Send a link to the Telequest Pull Requests group chat and tag the person(s) you assigned as a reviewer.
6. **IMPORTANT**: Please ensure that your Pull request gets at least one additional review before merging. This is to ensure that we have a second set of eyes on the code before merging it into the main branch.
7. Merging should be done to the `dev` branch only. We only merge to the `main` branch when we are ready to deploy a new version of the project.

---

Please ensure you follow these steps carefully. If you have any issues or questions, feel free to reach out. Thank you for your contributions!