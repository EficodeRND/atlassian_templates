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
    confluence_url = get_parameter('CONFLUENCE_URL', True)              # Confluence URL address
    project_key = get_parameter('PROJECT_KEY', True)                    # Project/space key
    project_name = get_parameter('PROJECT_NAME', True)                  # Project/space name
    confluence_username = get_parameter('CONFLUENCE_USERNAME', True)    # Confluence username for user that will create a space
    confluence_token = get_parameter('CONFLUENCE_TOKEN', True)          # Confluence personal access token (PAT) that will be used to authenticate
    category = get_parameter('CATEGORY', True)                          # Category for the space
    user_group = get_parameter('USER_GROUP', True)                       # name of the user group for permissions

    workspace_url = confluence_service.create_empty_workspace(confluence_url=confluence_url, project_key=project_key,
                                                              project_name=project_name,
                                                              confluence_username=confluence_username,
                                                              confluence_token=confluence_token,
                                                              category=category,
                                                              user_group=user_group)
