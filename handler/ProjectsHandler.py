import json
import tornado

from handler.allMethods import load_projects, start_all_projects, stop_all_projects

class ProjectHandler(tornado.web.RequestHandler):
    async def post(self):
        data = json.loads(self.request.body)
        action = data.get('action')
        config_file = data.get('config_file', 'projects_config.json')

        if action == "start":
            start_all_projects(config_file)
            self.write({"message": "Starting all projects."})
        elif action == "stop":
            stop_all_projects(config_file)
            self.write({"message": "Stopping all projects."})
        else:
            self.write({"error": "Invalid action."})

    async def get(self):
        projects = load_projects('projects_config.json')
        self.write({"projects": projects})