import os
import subprocess

def get_commands():
    sh_files = [i for i in os.listdir('./commands') if i.endswith('.sh')]
    return {command.replace('_', ' ').title().split('.')[0]:command for command in sh_files}

def run_sh(sh_file):
    subprocess.Popen(["/bin/bash", f"./commands/{sh_file}"], close_fds = True)