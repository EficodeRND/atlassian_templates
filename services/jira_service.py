import logging as log


def create_project(jira_url: str, project_key: str, project_name: str, board_type: str):
    log.info("Creating Jira project")

    # Should return link to the project?
    return f"{jira_url}/{project_key}"
