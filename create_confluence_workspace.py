#!/usr/bin/env python

from asyncio import protocols
import os
import json
import logging as log
import sys

from services import confluence_service
from utils.validators import get_parameter

root = log.getLogger()
root.setLevel(log.DEBUG)
log_handler = log.StreamHandler(sys.stdout)
log_handler.setLevel(log.DEBUG)
formatter = log.Formatter('%(asctime)s %(levelname)s (%(filename)s:%(lineno)d) - %(message)s')
log_handler.setFormatter(formatter)
root.addHandler(log_handler)

if __name__ == '__main__':
    confluence_url = get_parameter('CONFLUENCE_URL')                    # Confluence URL address
    project_key = get_parameter('PROJECT_KEY')                          # Project/space key
    project_name = get_parameter('PROJECT_NAME')                        # Project/space name
    project_lead = get_parameter("PROJECT_LEAD")                        # Project lead Confluence username
    confluence_username = get_parameter('CONFLUENCE_USERNAME')          # Confluence username for user that will create a space
    confluence_token = get_parameter('CONFLUENCE_TOKEN')                # Confluence personal access token (PAT) that will be used to authenticate
    category = get_parameter('CATEGORY')                                # Category for the space
    user_group = get_parameter('USER_GROUP')                            # name of the user group for permissions
    template_space_key = get_parameter('TEMPLATE_SPACE_KEY', False)     # ID for template space

    workspace_url = confluence_service.create_confluence_workspace(confluence_url=confluence_url, project_key=project_key,
                                                                   project_name=project_name,
                                                                   confluence_username=confluence_username,
                                                                   confluence_token=confluence_token,
                                                                   category=category,
                                                                   user_group=user_group,
                                                                   template_space_key=template_space_key,
                                                                   project_lead=project_lead)
