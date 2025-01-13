import tornado.websocket
import tornado.ioloop
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from handler.allMethods import load_projects

class LogWebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def initialize(self):
        self.projects = load_projects('projects_config.json')
        self._is_open = False
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.last_position = 0
        self.script_dir = None
        self.script_path = None
        self.log_path = None

    async def open(self):
        project_name = self.get_query_argument('project_name', None)
        
        if not project_name:
            self.write_message(json.dumps({"error": "Project name not provided"}))
            self.close()
            return

        project = self.get_project_by_id(project_name)
        if project:
            self.script_path = project['script_path_start']
            self.script_dir =  "/".join(self.script_path.split('/')[:-1])
            self.log_path = project['log_path']
        else:
            self.write_message(json.dumps({"error": "Invalid Project ID"}))
            self.close()
            return

        self._is_open = True  
        await self.send_log_updates()

    def on_close(self):
        self._is_open = False

    def get_project_by_id(self, project_name):
        for project in self.projects:
            if str(project.get('name')) == project_name:
                return project
        return None

    def start_script(self):
        try:
            subprocess.Popen(
                ['bash', self.script_path], cwd=self.script_dir,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except Exception as e:
            print(f"Error starting script: {e}")

    async def send_log_updates(self):
        while self._is_open:
            new_lines = self.read_new_log_entries()
            if new_lines:
                self.write_message(json.dumps({"log": new_lines}))
            await tornado.gen.sleep(1)

    def read_new_log_entries(self):
        new_lines = []
        try:
            with open(self.log_path, 'r') as file:
                file.seek(self.last_position)  
                new_lines = file.readlines()  
                self.last_position = file.tell() 
        except Exception as e:
            print(f"Error reading log file: {e}")
        return new_lines

