import tornado.websocket
import json
import requests
import psutil
import socket
from handler.allMethods import load_projects
from util.log_util import Log

class StatusWebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True
    
    def initialize(self):
        self.projects = load_projects('projects_config.json')
        self._is_open = False
        self.previous_status = None 
        self.previous_ram_info = None

    def open(self):
        self._is_open = True
        self.send_status_update()
        self.send_periodic_updates()

    def on_close(self):
        self._is_open = False
        
    def check_ram(self):
        memory = psutil.virtual_memory()
        total_ram = memory.total / (1024 ** 3)  
        used_ram = memory.used / (1024 ** 3)   
        available_ram = memory.available / (1024 ** 3)  
        ram_info = {
            'total_ram': total_ram,
            'used_ram': used_ram,
            'available_ram': available_ram
        }

        return ram_info

    def send_status_update(self):
        if self._is_open: 
            status = self.check_all_projects_status()
            ram_info = self.check_ram()
            if status != self.previous_status and ram_info != self.previous_ram_info:
                try:
                    result = {"project_status": status, "ram_info": ram_info}
                    self.write_message(json.dumps(result))
                    self.previous_status = status 
                    self.previous_ram_info = ram_info
                except tornado.websocket.WebSocketClosedError:
                    Log.i("WebSocket is closed. Unable to send the message.")
                    self._is_open = False  
    def check_database_status(self):
        database_status = []
        for projects in self.projects:
            project_name = projects['name']
            
    def check_all_projects_status(self):
        all_projects_status = []

        for project in self.projects:
            project_name = project['name']
            project_url = project['url']
            project_host = project['instance'][0]['host']
            project_header = project['payload']
            project_ports = [instance['port'] for instance in project['instance']]

            project_status = {
                'name': project_name,
                'status': self.check_application_status(project_url, project_header),
                'ports_status': self.check_ports_status(project_host, project_ports)
            }
            all_projects_status.append(project_status)

        return all_projects_status

    def check_application_status(self, url,header):
        try:
            response = requests.get(url, headers=header, timeout=5)
            if response.status_code == 200:
                return "active"
            else:
                return "inActive"
        except requests.ConnectionError:
            return "inActive"
        except requests.Timeout:
            return "inActive"

    def check_ports_status(self, host, ports):
        ports_status = {}
        for port in ports:
            port_engaged = False
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                try:
                    s.connect((host, port))
                    port_engaged = True
                except (socket.timeout, ConnectionRefusedError):
                    port_engaged = False

            ports_status[port] = 'engaged' if port_engaged else 'not engaged'

        return ports_status

    def send_periodic_updates(self):
        if self._is_open:
            self.send_status_update()
            tornado.ioloop.IOLoop.current().call_later(1, self.send_periodic_updates)
