import logging as log

import requests
from requests.auth import HTTPBasicAuth

HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


def create_empty_workspace(confluence_url: str, project_key: str, project_name: str, confluence_username: str, confluence_token: str, category: str):
    log.info("Creating empty Confluence space")

    authentication = HTTPBasicAuth(confluence_username, confluence_token)

    payload = {
        "key": project_key,
        "name": project_name,
        "description": {
            "plain": {
                "value": "This is an example space",
                "representation": "plain"
            }
        },
        "metadata": {}
    }

    url = f"{confluence_url}/rest/api/space"
    response = requests.post(url, json=payload, headers=HEADERS, auth=authentication)
    if response.status_code != 200:
        raise Exception(f"Space creation failed: {response.text}")

    payload = {
        "children":
        [
            {"key": project_key, "type": "space"}
        ]
    }

    url = f"{confluence_url}/rest/refinedtheme/2.0/category/move-children?newKey={category}"
    response = requests.put(url, json=payload, headers=HEADERS, auth=authentication)
    log.info(response.text)

    return f"{confluence_url}/rest/space"
