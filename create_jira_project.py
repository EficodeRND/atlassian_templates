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

    project_key = get_parameter('PROJECT_KEY', True)
    project_name = get_parameter('PROJECT_NAME', True)
    board_type = get_parameter('BOARD_TYPE', True)
    jira_url = get_parameter('JIRA_URL', True)
    board_type = get_parameter('BOARD_TYPE', True)

    project_url = jira_service.create_project(jira_url=jira_url,
                                              project_key=project_key,
                                              project_name=project_name,
                                              board_type=board_type)

    result = {'result': {
        'projectKey': project_key,
        'projectName': project_name,
        'boardType': board_type,
        'url': project_url
    }}

    with open(os.environ['RESULT_FILE'], 'w', encoding="utf8") as target_file:
        target_file.write(json.dumps(result))

    log.info("...DONE")
