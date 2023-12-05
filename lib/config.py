import os

server_port = '8000'
server_ip = '127.0.0.1'

local_user = os.path.expanduser("~")
config_file = os.path.abspath(__file__)
config_dir = os.path.dirname(os.path.realpath(__file__))

home_page_dir = os.path.join(config_dir, 'Home Page')
home_page = os.path.join(home_page_dir, 'index.html')

reports_dir = os.path.join(home_page_dir, 'Reports')
templates_dir = os.path.join(home_page_dir, 'Templates')
resources_dir = os.path.join(home_page_dir, 'Resources')
project_data_dir = os.path.join(home_page_dir, 'Project Data')

server_exe = os.path.join(home_page_dir, 'tcp_localhost.exe')

screenshot_size = 256, 256
screenshot_anti_alias = True
screenshot_transparency = True
screenshot_dir = os.path.join(resources_dir, 'screenshots')

logger = os.path.join(
        local_user,
        'AppData',
        'local',
        'temp',
        'project_data_f360.log',
        )

project_data_variables = {
        'addy': 'Project Address',
        }
