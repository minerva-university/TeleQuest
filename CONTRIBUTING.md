# CONTRIBUTING.md

Thank you for your interest in contributing to TeleQuest. This document will guide you through the process of setting up your development environment and submitting a pull request.

## Table of Contents
- [CONTRIBUTING.md](#contributingmd)
  - [Table of Contents](#table-of-contents)
  - [Setting Up Your Development Environment](#setting-up-your-development-environment)
    - [Requirements](#requirements)
    - [Getting Started](#getting-started)
  - [Setting up your dev environment for Python](#setting-up-your-dev-environment-for-python)
  - [Working on the main application](#working-on-the-main-application)
  - [Working on the Web App](#working-on-the-web-app)
  - [Committing Changes](#committing-changes)
  - [Code Style](#code-style)
  - [Code: Python](#code-python)
  - [Submitting a Pull Request](#submitting-a-pull-request)
  - [Approving a Pull Request](#approving-a-pull-request)
  - [Merging a Pull Request](#merging-a-pull-request)
  - [Deployment](#deployment)
    - [Local deployment](#local-deployment)

## Setting Up Your Development Environment

### Requirements

Before you start contributing, make sure you have the following tools installed:

1. **VS Code**: We recommend using [Visual Studio Code (VS Code)](https://code.visualstudio.com/) as your code editor. It offers a rich set of extensions and integrated terminal which will make development smoother.
2. [Black Formatter Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) for VSCode.
3. [Prettier Extension](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) for VSCode.

4. **Git**: This is essential for source code management. If you don't have Git installed, you can download and install it from [Git's official site](https://git-scm.com/).

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
## Setting up your dev environment for Python

2. **Installing Python**:

   - **Windows**:
     1. Download Python version 3.11 from [Python's official site](https://www.python.org/downloads/release/python-3116/).
     2. Run the installer. Ensure that you check the option to add Python to PATH.
   - **Mac**:
     ```bash
     brew install python@3.11
     ```
   - **Linux (Ubuntu)**:
     ```bash
     sudo apt-get update
     sudo apt-get install python3.11 python3-pip
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

4. **Activate the virtual environment**:

   You will be doing this most of the time before working on the Python code.

   - **Windows**:
     ```bash
     .\.venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source .venv/bin/activate
     ```

5. **Installing Dependencies**:
   
   With the virtual environment activated, install the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```
Recommended: We will be using a Python-Telegram-API wrapper or package called [python-telegram-bot](https://python-telegram-bot.org/). You can [read the documentation](https://docs.python-telegram-bot.org/en/v20.6/) to get a better understanding of how to use it.


## Working on the main application

If you want to get started with working on the Telegram bot, the AI or the database, follow these steps:

1. **Change to the directory**: For example for the bot
   
   ```bash
   cd bot
   ```



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

3. Push the changes to your branch:

   ```bash
   git push origin username/feature-name
   ```


## Code Style

For Javascript and React, please use the [Prettier Extension](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) for VSCode. Ensure it autoformats when you save a file.

For Python, use the [Black Formatter Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) for VSCode. Ensure it autoformats when you save a file. Files that are not properly formatted will not pass the pull request tests.

Use [type hints](https://www.pythontutorial.net/python-basics/python-type-hints/) with Python as much as possible without sacrificing code readability. Most of the code will be in Python and type hints often make debugging easier.

We will be using `mypy` for static type checking. The `py-requirements.txt` contains all requirements for all the Python files and is needed by `mypy`. You may have multiple virtual environments for different subfolders, but do keep one at the root folder with all requirements for Python installed. (Or bet that your PR won't pass all checks the first time).

You can use the [Pylance Language Server](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) for VSCode to catch type errors easily and utilise type hints better. It also has other features you can read about there.

## Code: Python

As mentioned before, we're using type hints with Python. This helps us catch many potential errors early, but we need to be disciplined.

1. Installing a third-party library should be done only when you really need to, and it's not in the Python standard library.
2. If you are installing a new library (adding to our requirements), from the root directory (where `requirements.txt` is located), run 
  ```bash
  pip3 freeze > requirements.txt
  ``` 
to update our requirements.

1. Try to define all types you think need to be defined. It may help to have a separate file containing only types. Look at [telegram_types.py](./bot/telegram_types.py) as an example.

## Submitting a Pull Request

1. Navigate to the main repository you forked.
2. Click on "Pull requests" and then the "New Pull Request" button.
3. Select your branch from the dropdown and submit your pull request.
4. On the right side of the screen, request a review from someone on the team.
5. **IMPORTANT**: Please ensure that your Pull request gets at least one additional review before merging. This is to ensure that we have a second set of eyes on the code before merging it into the main branch.

## Approving a Pull Request

1. Go to the Pull request link.
2. If you were previously added a reviewer, you can click on "Add your review" at the top.
3. If you do not see this, go to the last commit.
4. On the right side of the screen, click on "Review changes".
5. Add a comment and select either "Comment", "Request changes" or "Approve".
6. _Do not_ approve a PR for which all checks have not passed, if any.
7. **Do not** merge the pull request after approving.

## Merging a Pull Request

1. Merging should be done to the `dev` branch only. We only merge to the `main` branch when we are ready to deploy a new version of the project.
2. Only merge pull requests authored by you. Your approver should not merge your pull request.

## Deployment

Both frontend and backend of the project are deployed on Heroku. The `main` branch is automatically deployed to Heroku automatically when a new commit is pushed to it.

### Local deployment

You can run the bot and frontend locally in Docker containers by building the docker image and running it. This depends on having specific environment variables defined in a `.env` file in the root directory. 

**Before running this locally, you should have a `.env` file in the root directory with correct API keys. Use the `.env.example` to determine which variables are required for the bot to run properly. If you do not have this file, the docker file will not build so be sure to create a .env**

For the purposes of testing, you can create the `.env` file with mock variables, this will allow the docker image to build, and also run the frontend and backend. However, the backend will not be able to connect to any of the external services like the Telegram API, MongoDB database, etc, because it requires the correct API keys. You will still be able to see the pretty frontend locally and watch a demo of how the bot works.

After copying the `.env` to the project's root directory, you can build the docker image and run it.
You can do this by running:
```bash
docker build --no-cache -t telequest:latest .
docker-compose up -d 
```

This should build and run the docker images for the bot and frontend. You can then access the frontend at `localhost:3000` and the bot cannot be accessed via a web browser, instead verify that it is running by testing on one of your telegram groups. You can access the local TeleQuest here: https://t.me/localTelequest_bot

---

Please ensure you follow these steps carefully. If you have any issues or questions, feel free to reach out. Thank you for your contributions!