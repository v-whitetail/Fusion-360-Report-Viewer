import threading
import subprocess
from .config import *
from .report_viewer_utils import *
from . import fusion360utils as futil

global tcp_thread

def run_exe(ip, port, target_dir):
    subprocess.Popen(
        [server_exe, ip, port, target_dir],
        creationflags=subprocess.CREATE_NO_WINDOW,
        )

def start():
    if not (os.path.exists(reports_dir) and os.path.exists(templates_dir)):
        try:
            os.makedirs(reports_dir)
            os.makedirs(templates_dir)
        except OSError as error:
            futil.log(
                f'Creation of {reports_dir} and {templates_dir} '
                f'failed due to: {error}'
            )


    global tcp_thread
    futil.log(format((server_ip,server_port,home_page_dir)))
    tcp_thread = threading.Thread(
        target=run_exe,
        args=(
            server_ip,
            server_port,
            home_page_dir
        )
    )
    tcp_thread.start()

def stop():
    global tcp_thread
    process_name = 'tcp_localhost.exe'

    try:
        tasks = subprocess.check_output(
            args=['tasklist'],
            shell=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        futil.log(
            f'An error occurred while trying to list tasks: {e}'
        )
        return

    for line in tasks.splitlines():
        if process_name in line:
            pid = int(line.split()[1])
            try:
                subprocess.check_call(
                    args=['taskkill', '/F', '/PID', str(pid)],
                    shell=True
                )
                futil.log(
                    f'Process {process_name} (PID {pid}) has been terminated.'
                )
            except subprocess.CalledProcessError as e:
                futil.log(
                    f'An error occurred while trying to kill {process_name}: {e}'
                )

    tcp_thread.join()
