import adsk.core, adsk.fusion, adsk.cam
import os, subprocess
from ...lib import fusion360utils as futil
from ...lib.config import logger

app = adsk.core.Application.get()
ui = app.userInterface

CMD_ID = f'openLocalhostLogFile'
CMD_NAME = 'Open Log File'
CMD_BESIDE_ID = f''
CMD_Description = (
    f'Open the Log File in the Default Text Editor'
    f'\n\n'
    f'The log file a temporary text file which shows all the data '
    f'exported from Fusion 360 to another process. This is useful '
    f'for understanding the exact layout of the design data before '
    f'it is processed into a report, and it is generally useful '
    f'or debugging. \n\n If a piece of data needs to be exported to '
    f'a report but does not show in the log file, the code for this '
    f'AddIn located in the "Buffer" module may need to be adjusted '
    f'to include it.'
)

WORKSPACE_ID = f'FusionSolidEnvironment'

TAB_ID = f'customReportsTab'
TAB_NAME = f'CUSTOM REPORTS'

PANEL_ID = f'customProjectData'
PANEL_NAME = f'PROJECT DATA'
PANEL_AFTER = f''

IS_PROMOTED = False

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

    if not os.path.exists(logger):
        with open(logger, 'w+') as file:
            file.write('')

    os.startfile(logger)

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
