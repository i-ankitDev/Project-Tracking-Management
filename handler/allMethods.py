from concurrent.futures import ThreadPoolExecutor
import json
import subprocess


def load_projects(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config['projects']


def start_instance(self,project):
    if 'script_path_start' in project:
        script_path = project['script_path_start']
        script_dir = "/".join(script_path.split('/')[:-1])
        print(f"Starting {project['name']} in a new terminal by running script at {script_path}")
        result = []
        try:
            log_path = project['log_path']
            try:
                subprocess.Popen(['bash', script_path], cwd=script_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                raise Exception
        except Exception as e:
            print(f"Failed to start {project['name']} in a new terminal: {e}")
    else:
        print(f"No script defined for {project['name']}.")

def stop_instance(self,project):
    if 'script_path_stop' in project:
        script_path = project['script_path_stop']
        script_dir = "/".join(script_path.split('/')[:-1])
        print(f"Stopping {project['name']} in a new terminal by running script at {script_path}")

        try:
            subprocess.Popen([
                'x-terminal-emulator', '-e', f'cd {script_dir} && bash {script_path}'
            ])
        except Exception as e:
            print(f"Failed to stop {project['name']} in a new terminal: {e}")
    else:
        print(f"No script defined for {project['name']}.")

# Function to start all projects
def start_all_projects(config_file):
    projects = load_projects(config_file)
    with ThreadPoolExecutor() as executor:
        for project in projects:
            executor.submit(start_instance, project)

# Function to stop all projects
def stop_all_projects(config_file):
    projects = load_projects(config_file)
    with ThreadPoolExecutor() as executor:
        for project in projects:
            executor.submit(stop_instance, project)
