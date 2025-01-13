#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from pathlib import Path
from datetime import datetime as dtime
from lib.log_util import Log 

CONFIG_FILE_PATH = './projects_config.json'

def load_projects(config_path):
    try:
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")

        with open(config_file, 'r') as file:
            config_data = json.load(file)

        projects = config_data.get("projects", [])
        if not projects:
            raise ValueError("No projects found in the configuration file.")

        return projects

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = exc_tb.tb_frame.f_code.co_filename
        iMessage = f"Exception: {type(e).__name__}. Argument: {e.args}. File: {fname}, Line: {exc_tb.tb_lineno}"
        Log.c('LOAD-PROJECTS-EXCEPTION', iMessage)
        raise e

def parse_projects(projects):
    parsed_projects = []
    for project in projects:
        try:
            project_name = project.get("name")
            project_code = project.get("projectCode")
            server = project.get("server")
            version = project.get("version")
            url = project.get("url")
            payload = project.get("payload", {})
            uploads_path = project.get("uploadsPath")
            script_start = project.get("script_path_start")
            script_stop = project.get("script_path_stop")
            log_path = project.get("log_path")
            instances = project.get("instance", [])

            instance_details = [
                {
                    "api": instance.get("api"),
                    "host": instance.get("host"),
                    "port": instance.get("port"),
                    "tcpPort": instance.get("tcpPort", None),  
                } for instance in instances
            ]

            parsed_projects.append({
                "name": project_name,
                "url": url,
                "payload": payload,
                "uploadsPath": uploads_path,
                "scriptStart": script_start,
                "scriptStop": script_stop,
                "logPath": log_path,
                "instances": instance_details,
            })

        except Exception as e:
            Log.c("PARSE-PROJECT-ERROR", f"Error parsing project {project.get('name', 'Unknown')}: {str(e)}")

    return parsed_projects

try:
    # Load and parse projects
    projects = load_projects(CONFIG_FILE_PATH)
    CONFIG = parse_projects(projects) 

    for project in CONFIG:
        print(json.dumps(project, indent=4))

except Exception as e:
    Log.c("SCRIPT-ERROR", f"Error in script: {str(e)}")
