import adsk.core, adsk.fusion, adsk.cam
import json
from ...lib import fusion360utils as futil
from ...lib.config import logger
from ...lib.config import project_data_dir
from ...lib.config import project_data_variables
from ...lib.selection_filters import *
from ...lib.Buffer import Builder
from ... import config

PALETTE_ID = config.sample_palette_id

CMD_ID = f'inputProjectData'
CMD_NAME = f'Create Project Data'
CMD_BESIDE_ID = f''
CMD_Description = f'''Create Project Data and Export to Reports

NOTE: This command primarily exists to be called when the document is saved but there is no project data found.
You should typically use Edit Project Data instead of this command.'''

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

    ui = get_ui()
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
    ui = get_ui()
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

    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.inputChanged, command_input_changed, local_handlers=local_handlers)
    futil.add_handler(args.command.executePreview, command_preview, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)

    inputs = args.command.commandInputs

    for variable_handle, variable_name in project_data_variables.items():
        inputs.addTextBoxCommandInput(
                f'{variable_handle}_input',
                f'{variable_name}',
                '',
                2,
                False,
                )

def command_execute(args: adsk.core.CommandEventArgs):

    document = get_document()
    scope_folder = document.dataFile.parentFolder
    project_folder = scope_folder.parentFolder
    project_data_file_name = project_folder.name + '.json'
    project_data_file = os.path.join(project_data_dir,project_data_file_name)

    futil.log(f'{CMD_NAME} Command Execute Event')
    inputs = args.command.commandInputs

    project_data = {}

    for variable_handle, variable_name in project_data_variables.items():
        project_data_input: adsk.core.TextBoxCommandInput = inputs.itemById(f'{variable_handle}_input')
        project_data[variable_name] = project_data_input.text


    with open(os.path.abspath(project_data_file),'w') as file:
        file.flush()
        file.write(json.dumps(project_data))

    buffer = Builder.build()
    with open(logger, 'a+') as log:
        log.write(buffer)

def command_preview(args: adsk.core.CommandEventArgs):
    inputs = args.command.commandInputs
    futil.log(f'{CMD_NAME} Command Preview Event')

def command_input_changed(args: adsk.core.InputChangedEventArgs):
    changed_input = args.input
    futil.log(f'{CMD_NAME} Input Changed Event fired from a change to {changed_input.id}')

def command_destroy(args: adsk.core.CommandEventArgs):
    global local_handlers
    local_handlers = []
    futil.log(f'{CMD_NAME} Command Destroy Event')

