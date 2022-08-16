import logging as log

import requests
from requests.auth import HTTPBasicAuth

HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


def create_project(jira_url: str, project_key: str, project_name: str, board_type: str):
    log.info("Creating Jira project")

    # Should return link to the project?
    return f"{jira_url}/{project_key}"


def create_project_from_template(jira_url: str, project_key: str, project_name: str, project_lead: str,
                                 template_project_id: int, jira_username: str, jira_token: str):
    log.info("Creating Jira project")

    authentication = HTTPBasicAuth(jira_username, jira_token)

    payload = {
        "key": project_key,
        "name": project_name,
        "projectTypeKey": "software",
        "description": "This project was created by rest api",
        "lead": project_lead,
        "assigneeType": "PROJECT_LEAD"
    }

    url = f"{jira_url}/rest/project-templates/1.0/createshared/{template_project_id}"
    response = requests.post(url, json=payload, headers=HEADERS, auth=authentication)
    if response.status_code != 200:
        raise Exception(f"Project creation failed {response.text}")

    return f"{jira_url}/{response.json()['returnUrl']}"


def copy_board_from_template(jira_url: str, project_key: str, board_ids: list, jira_username: str, jira_token: str):

    log.info("Creating Jira boards %s", board_ids)

    authentication = HTTPBasicAuth(jira_username, jira_token)

    for board_id in board_ids:
        board_url = f"{jira_url}/rest/greenhopper/1.0/rapidview/{board_id}/"
        response = requests.get(board_url, headers=HEADERS, auth=authentication)
        if response.status_code != 200:
            raise Exception(f"Reading board name failed {response.text}")

        board_name = f"{project_key} {response.json()['name']}"
        log.info("Creating board %s", board_name)
        payload = {
            "name": board_name
        }
        copy_board_url = f"{board_url}copy"
        response = requests.put(copy_board_url, json=payload, headers=HEADERS, auth=authentication)
        if response.status_code != 200:
            raise Exception(f"Board creation failed {response.text}")

        board_id = response.json()['id']
        payload['id'] = board_id
        update_board_url = f"{jira_url}/rest/greenhopper/1.0/rapidviewconfig/name"
        response = requests.put(update_board_url, json=payload, headers=HEADERS, auth=authentication)
        return response.text





