import os
import subprocess
import json
import importlib

def get_commands():
    sh_files = [i for i in os.listdir('./commands') if i.endswith('.sh')]
    return {command.replace('_', ' ').title().split('.')[0]:command for command in sh_files}

def get_maintenance_commands(file_dir):
    return [i+"_maintenance" for i in get_json_dot_seperated(file_dir).maintenance.keys()]

def run_sh(sh_file):
    subprocess.Popen(["/bin/bash", f"./commands/{sh_file}"], close_fds = True)

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def get_json_dot_seperated(file_dir):
    with open(file_dir, 'r') as file:
        data = json.load(file)
    return dotdict(data)

def read_json_data(file_dir):
    with open(file_dir, 'r') as file:
        data = json.load(file)
    return data

def dump_json_data(file_dir, data):
    with open(file_dir, 'w') as file:
        json.dump(data, file)

def scan_url_file(app_name):
    module = importlib.import_module(f"{app_name}.urls")
    urls = getattr(module, "urlpatterns")
    return [(url.pattern.regex.pattern, url.name) for url in urls]