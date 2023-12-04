import os

server_port = '8000'
server_ip = '127.0.0.1'

local_user = os.path.expanduser("~")
config_file = os.path.abspath(__file__)
config_folder = os.path.dirname(os.path.realpath(__file__))

home_folder = os.path.join( config_folder,'Home Page' )
home_page = os.path.join( home_folder, 'index.html')

reports = os.path.join( home_folder, 'Reports')
templates = os.path.join( home_folder, 'Templates')
project_data = os.path.join( home_folder, 'ProjectData')

projectdata = os.path.join( home_folder, 'projectdata')
server_exe = os.path.join( home_folder, 'tcp_localhost.exe')
report_home_folder = os.path.join( home_folder, 'fusion_home_folder.exe')
home_page_home_folder = os.path.join( home_folder, 'fusion_home_folder.exe')

logger = os.path.join(
        local_user,
        'AppData',
        'local',
        'temp',
        'projectdata_f360.log',
        )

project_data_variables = {
        'addy': 'Project Address',
        }
