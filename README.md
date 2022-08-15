# Atlassian templates

This repository contains scripts for managing Atlassian tools from the command line or by utilising the Sprout


## Running from the command line

Create virtual environment to the root od the code repository, activate it and install the dependencies
```
python3.9 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Instructions how to run specific template can be found below

## Available templates

### Create Jira project
Allows creating project from the command line

```
PROJECT_KEY=TSTPRJ PROJECT_NAME="Test project" BOARD_TYPE=Scrum JIRA_URL=https://jira.rootdemo.eficode.io/ RESULT_FILE=$HOME/tmp/jiratst.json ./create_jira_project.py
```

### Create Jira project from project template
Allows creating project from the command line

```
PROJECT_KEY=TSTPRJ PROJECT_NAME="Test project" PROJECT_LEAD="username" TEMPLATE_PROJECT_ID="12300" JIRA_USERNAME="username" JIRA_TOKEN="token" JIRA_URL=https://jira.rootdemo.eficode.io/ RESULT_FILE=$HOME/tmp/jiratst.json ./create_jira_project_from_template.py
```