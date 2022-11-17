import logging as log
import requests
from requests.auth import HTTPBasicAuth

HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


def create_confluence_workspace(confluence_url: str, project_key: str, project_name: str, confluence_username: str, confluence_token: str, category: str, user_group: str, template_space_key: str, project_lead: str):
    log.info("Creating empty Confluence space")

    authentication = HTTPBasicAuth(confluence_username, confluence_token)


# Create new workspace

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
    log.info(response.json())
    new_space_id = response.json()['id']
    new_space_page_id = response.json()['homepage']['id']

# Move space to correct category

    payload = {
        "children":
        [
            {"key": project_key, "type": "space"}
        ]
    }

    url = f"{confluence_url}/rest/refinedtheme/2.0/category/move-children?newKey={category}"
    response = requests.put(url, json=payload, headers=HEADERS, auth=authentication)
    log.info(response)
    if response.status_code != 200:
        raise Exception(f"Failed to set category: {response.text}")


# Set permissions for project

    payload = {
        "jsonrpc": "2.0",
        "method": "addPermissionToSpace",
        "params":
        ["VIEWSPACE", user_group, project_key],
        "id": 12345
    }

    url = f"{confluence_url}/rpc/json-rpc/confluenceservice-v2"
    response = requests.post(url, json=payload, headers=HEADERS, auth=authentication)
    log.info(response.text)

    payload = {
        "jsonrpc": "2.0",
        "method": "addPermissionToSpace",
        "params":
            ["SETSPACEPERMISSIONS", project_lead, project_key],
        "id": 12345
    }

    url = f"{confluence_url}/rpc/json-rpc/confluenceservice-v2"
    response = requests.post(url, json=payload, headers=HEADERS, auth=authentication)
    log.info(response.text)

# Copy template page hierarchy to the new project

    url = f"{confluence_url}/rest/api/content?spaceKey={template_space_key}"
    response = requests.get(url, headers=HEADERS, auth=authentication)
    template_page_id = response.json()['results'][0]['id']

    payload = {
        "copyAttachments": "true",
        "copyLabels": "true",
        "copyPermissions": "true",
        "destinationPageId": new_space_page_id,
        "originalPageId": template_page_id,
        "titleOptions": {"prefix": "", "search": "", "replace": ""}
    }

    url = f"{confluence_url}/rest/page-hierarchy/copy"
    response = requests.post(url, json=payload, headers=HEADERS, auth=authentication)
    if response.status_code != 200:
        raise Exception(f"Failed to copy page hierarchy: {response.text}")

    url = f"{confluence_url}/rest/api/content?spaceKey={project_key}"
    response = requests.get(url, headers=HEADERS, auth=authentication)
    home_page_id = response.json()['results'][0]['id']
    log.info(f"home page id:{home_page_id}")
    template_page_id = response.json()['results'][1]['id']
    log.info(f"template page id after move:{template_page_id}")

    payload = {
        "name": project_name,
        "homepage": {
            "id": template_page_id
        }
    }

    url = f"{confluence_url}/rest/api/space/{project_key}"
    response = requests.put(url, json=payload, headers=HEADERS, auth=authentication)
    log.info(response.json())

    return f"{confluence_url}/rest/space"


