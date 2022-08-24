#!/usr/bin/env python

import os
import json
import logging as log
import sys

from services import jira_service
from utils.validators import get_parameter

root = log.getLogger()
root.setLevel(log.DEBUG)
log_handler = log.StreamHandler(sys.stdout)
log_handler.setLevel(log.DEBUG)
formatter = log.Formatter('%(asctime)s %(levelname)s (%(filename)s:%(lineno)d) - %(message)s')
log_handler.setFormatter(formatter)
root.addHandler(log_handler)


if __name__ == '__main__':

    jira_url = get_parameter('JIRA_URL', True)
    project_key = get_parameter('PROJECT_KEY', True)
    project_name = get_parameter('PROJECT_NAME', True)
    project_lead = get_parameter('PROJECT_LEAD', False)
    jira_project_type = get_parameter('JIRA_PROJECT_TYPE', True)
    template_project_id = get_parameter('TEMPLATE_PROJECT_ID', True)
    template_board_ids = get_parameter('TEMPLATE_BOARD_IDS', False)
    jira_username = get_parameter('JIRA_USERNAME', True)
    jira_token = get_parameter('JIRA_TOKEN', True)

    if project_lead is None:
        project_lead = jira_username

    project_url, project_id = jira_service.create_project_from_template(jira_url=jira_url,
                                                                        project_key=project_key,
                                                                        project_name=project_name,
                                                                        project_lead=project_lead,
                                                                        template_project_id=template_project_id,
                                                                        jira_username=jira_username,
                                                                        jira_token=jira_token)

    if jira_project_type == "JIRA_BUSINESS_PROJECT":
        if template_board_ids is None or len(template_board_ids) <= 0:
            raise Exception("Template board ids not defined")
        template_board_ids = "".join(template_board_ids.split())
        board_ids = template_board_ids.split(',')
        project_url = jira_service.copy_board_from_template(jira_url=jira_url,
                                                            project_key=project_key,
                                                            project_name=project_name,
                                                            board_ids=board_ids,
                                                            jira_username=jira_username,
                                                            jira_token=jira_token,
                                                            project_id=project_id)

    result = {'result': {
        'projectKey': project_key,
        'projectName': project_name,
        'url': project_url
    }}

    with open(os.environ['RESULT_FILE'], 'w', encoding="utf8") as target_file:
        target_file.write(json.dumps(result))

    log.info("...DONE")
