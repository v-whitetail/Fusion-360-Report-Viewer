import adsk.core, adsk.fusion, adsk.cam
import os
import threading
import subprocess
from . import config
from . import fusion360utils as futil

app = adsk.core.Application.get()
ui = app.userInterface

home_page = config.home_page
home_page_dir = config.home_page_dir

reports = config.reports_dir
templates = config.templates_dir

local_user = config.local_user
server_exe = config.server_exe

server_ip = config.server_ip
server_port = config.server_port

global tcp_thread

def run_exe(server_ip,server_port,home_page_dir):
    subprocess.Popen(
        [server_exe, server_ip, server_port, home_page_dir],
        creationflags=subprocess.CREATE_NO_WINDOW,
        )

def start():
    if not (os.path.exists(reports) and os.path.exists(templates)):
        try:
            os.makedirs(reports)
            os.makedirs(templates)
        except OSError as error:
            futil.log(f"Creation of the directory {reports} and {templates} failed due to: {error}")


    global tcp_thread
    futil.log(format((server_ip,server_port,home_page_dir)))
    tcp_thread = threading.Thread(target=run_exe, args=(server_ip,server_port,home_page_dir))
    tcp_thread.start()

def stop():
    global tcp_thread
    process_name = 'tcp_localhost.exe'

    try:
        tasks = subprocess.check_output(['tasklist'], shell=True, text=True)
    except subprocess.CalledProcessError as e:
        futil.log(f"An error occurred while trying to list tasks: {e}")
        return

    for line in tasks.splitlines():
        if process_name in line:
            pid = int(line.split()[1])

            try:
                subprocess.check_call(['taskkill', '/F', '/PID', str(pid)], shell=True)
                futil.log(f"Process {process_name} (PID {pid}) has been terminated.")
            except subprocess.CalledProcessError as e:
                futil.log(f"An error occurred while trying to kill {process_name}: {e}")

    tcp_thread.join()
