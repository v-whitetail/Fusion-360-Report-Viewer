import adsk.core
import os
from ...lib import live_server
from ...lib import fusion360utils as futil
from ...lib.config import server_ip, server_port, home_page_dir, config_file

app = adsk.core.Application.get()
ui = app.userInterface

CMD_ID = 'startLocalhostServer'
CMD_NAME = 'Start Server'
CMD_BESIDE_ID = ''
CMD_Description = (
    f'Launch a Localhost Server'
    f'\n\n'
    f'Launch a server on your pc to host your report files. '
    f'This allows you to view your reports in your internet browser '
    f'as live documents. The browser view will automatically refresh '
    f'whenever a document in your Home Folder is modified. \n\n The '
    f'current configuration will launch a localhost server with the '
    f'IP address {server_ip} on port {server_port} hosting '
    f'{home_page_dir}. Each of these settings can be configured '
    f'individually at {config_file}'
)

WORKSPACE_ID = 'FusionSolidEnvironment'

TAB_ID = 'customReportsTab'
TAB_NAME = 'CUSTOM REPORTS'

PANEL_ID = 'reportBrowser'
PANEL_NAME = 'REPORT BROWSER'
PANEL_AFTER = ''

IS_PROMOTED = True

ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

local_handlers = []
def start():
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)
    futil.add_handler(cmd_def.commandCreated, command_created)
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    toolbar_tab = workspace.toolbarTabs.itemById(TAB_ID)
    if toolbar_tab is None:
        toolbar_tab = workspace.toolbarTabs.add(TAB_ID, TAB_NAME)
    panel = toolbar_tab.toolbarPanels.itemById(PANEL_ID)
    if panel is None:
        panel = toolbar_tab.toolbarPanels.add(PANEL_ID, PANEL_NAME, PANEL_AFTER, False)

    control = panel.controls.addCommand(cmd_def, CMD_BESIDE_ID, False)
    control.isPromoted = IS_PROMOTED

def stop():
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    if command_control:
        command_control.deleteMe()

    if command_definition:
        command_definition.deleteMe()

def command_created(args: adsk.core.CommandCreatedEventArgs):
    futil.log(f'{CMD_NAME} Command Created Event')

    live_server.start()

    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)

def command_execute(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} Command Execute Event')

def command_preview(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} Command Preview Event')

def command_input_changed(args: adsk.core.InputChangedEventArgs):
    changed_input = args.input
    futil.log(f'{CMD_NAME} Input Changed Event fired from a change to {changed_input.id}')

def command_validate_input(args: adsk.core.ValidateInputsEventArgs):
    futil.log(f'{CMD_NAME} Validate Input Event')
        
def command_destroy(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} Command Destroy Event')
    global local_handlers
    local_handlers = []
