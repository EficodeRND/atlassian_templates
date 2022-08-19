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

    project_url = f"{jira_url}/{response.json()['returnUrl']}"
    project_id = response.json()['projectId']

    payload = {
        "user": [jira_username]
    }

    response = requests.post(f"{jira_url}/rest/api/2/project/{project_key}/role/10002", json=payload, headers=HEADERS,
                             auth=authentication)
    if response.status_code != 200:
        raise Exception(f"Failed to add bot user as admin to project. {response.status_code}")

    return project_url, project_id


def copy_board_from_template(jira_url: str, project_key: str, project_name: str, board_ids: list, jira_username: str,
                             jira_token: str, project_id: str):

    log.info("Creating Jira boards %s", board_ids)

    authentication = HTTPBasicAuth(jira_username, jira_token)

    result = []
    for board_id in board_ids:
        board_url = f"{jira_url}/rest/greenhopper/1.0/rapidview/{board_id}/"
        response = requests.get(board_url, headers=HEADERS, auth=authentication)
        if response.status_code != 200:
            raise Exception(f"Failed to read board name {response.text}")

        board_name = f"{project_key} {response.json()['name']}"
        log.info("Creating board %s", board_name)
        payload = {
            "name": board_name
        }
        copy_board_url = f"{board_url}copy"
        response = requests.put(copy_board_url, json=payload, headers=HEADERS, auth=authentication)
        if response.status_code != 200:
            raise Exception(f"Failed to copy board {response.text}")
        result.append(board_name)

        board_id = response.json()['id']
        payload['id'] = board_id
        update_board_url = f"{jira_url}/rest/greenhopper/1.0/rapidviewconfig/name"
        response = requests.put(update_board_url, json=payload, headers=HEADERS, auth=authentication)
        if response.status_code != 200:
            raise Exception(f"Failed to rename board {response.text}")

        log.info("Creating filters")

        issuetype = "Epic"
        name = board_name.lower()
        if "bug" in name:
            issuetype = "Bug"
        elif "story" in name:
            issuetype = "Story"

        jql = f"Project = {project_key} AND Issuetype = {issuetype}"
        payload = {
            "jql": jql,
            "name": f"{project_key} {issuetype}",
            "description": f"Filter for {board_name}"
        }
        create_filter_url = f"{jira_url}/rest/api/2/filter"
        response = requests.post(create_filter_url, json=payload, headers=HEADERS, auth=authentication)
        filter_id = response.json()["id"]

        payload = {
            "type": "project",
            "projectId": project_id,
            "view": "true",
            "edit": "false"
        }
        response = requests.post(f"{jira_url}/rest/api/2/filter/{filter_id}/permission", json=payload, headers=HEADERS,
                                 auth=authentication)
        if response.status_code != 201:
            raise Exception(f"Failed to add view permissions to filter {response.status_code}")

        payload = {
            "type": "projectRole",
            "projectId": project_id,
            "projectRoleId": "10002",
            "view": "true",
            "edit": "true"
        }
        response = requests.post(f"{jira_url}/rest/api/2/filter/{filter_id}/permission", json=payload, headers=HEADERS,
                                 auth=authentication)
        if response.status_code != 201:
            raise Exception(f"Failed to add edit permissions to filter {response.text}")

        payload = {
            "id": board_id,
            "savedFilterId": filter_id
        }
        response = requests.put(f"{jira_url}/rest/greenhopper/1.0/rapidviewconfig/filter", json=payload, headers=HEADERS, auth=authentication)

        if response.status_code != 200:
            raise Exception(f"Failed to update filter to board {response.status_code}")

    return result




