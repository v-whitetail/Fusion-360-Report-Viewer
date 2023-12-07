import adsk.core, adsk.fusion, adsk.cam
from ... import config
from ...lib.report_viewer_utils import *

PALETTE_ID = config.sample_palette_id

CMD_ID = f'addImage'
CMD_NAME = 'Add Image'
CMD_BESIDE_ID = f''
CMD_Description = 'Manually Associate an Image with a Processing Stations'

WORKSPACE_ID = f'FusionSolidEnvironment'

TAB_ID = f'customReportsTab'
TAB_NAME = f'CUSTOM REPORTS'

PANEL_ID = f'processingStations'
PANEL_NAME = f'PROCESSING STATIONS'
PANEL_AFTER = f''

IS_PROMOTED = True

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
    selection = inputs.addSelectionInput(
        f'image_add_input_body',
        f'Selection',
        f'Select a Body to Add an Image to',
    )
    selection.setSelectionLimits(1,1)
    selection.clearSelectionFilter()
    selection.addSelectionFilter(adsk.core.SelectionCommandInput.Bodies)

def command_execute(args: adsk.core.CommandEventArgs):

    futil.log(f'{CMD_NAME} Command Execute Event')
    inputs = args.command.commandInputs

    selection_input = inputs.itemById(f'image_add_input_body')

    if ((body := selection_input.selection(0).entity)
            and isinstance(body, adsk.fusion.BRepBody)):
        file_name = os.path.join(
            screenshot_dir,
            f'user-{part_id(body)}.png'
        )
        viewport = adsk.core.Application.get().activeViewport
        viewport.fit()
        get_ui().activeSelections.removeByEntity(body)
        viewport.saveAsImageFileWithOptions(save_image_options(file_name))

def command_preview(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} Command Preview Event')

def command_input_changed(args: adsk.core.InputChangedEventArgs):
    changed_input = args.input
    futil.log(f'{CMD_NAME} Input Changed Event fired from a change to {changed_input.id}')

def command_validate_input(args: adsk.core.ValidateInputsEventArgs):
    futil.log(f'{CMD_NAME} Validate Input Event')

def command_destroy(args: adsk.core.CommandEventArgs):
    global local_handlers
    local_handlers = []
    futil.log(f'{CMD_NAME} Command Destroy Event')
