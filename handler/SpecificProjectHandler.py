import json
import tornado

from handler.allMethods import load_projects, start_instance, stop_instance
from handler.baseHandler import BaseHandler
from util.log_util import Log

class SpecificProjectHandler(BaseHandler):
    
    async def post(self):
        data = json.loads(self.request.body)
        project_name = data.get('project_name')
        action = data.get('action')
        projects = load_projects('projects_config.json')
        project = next((p for p in projects if p['name'] == project_name), None)

        if project is None:
            Log.i(f"Project not found: {project_name}")
            self.set_status(404)
            self.write({"error": "Project not found."})
            return

        if action == "start":
            start_instance(self,project)
            self.write({"message": f"Starting {project_name}."})
        elif action == "stop":
            stop_instance(self,project)
            self.write({"message": f"Stopping {project_name}."})
        else:
            self.write({"error": "Invalid action."})
