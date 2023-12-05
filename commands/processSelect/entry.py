import adsk.core, adsk.fusion, adsk.cam
from ... import config
from ...lib import fusion360utils as futil
from ...lib.selection_filters import *

PALETTE_ID = config.sample_palette_id

CMD_ID = f'processSelect'
CMD_NAME = 'Select By Processing Station'
CMD_BESIDE_ID = f''
CMD_Description = 'Select Every Body with the Specified Processing Station'

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

    for template in list_all_templates():
        inputs.addBoolValueInput(
                f'{template}_input',
                f'{template}',
                True,
                )

def command_execute(args: adsk.core.CommandEventArgs):

    futil.log(f'{CMD_NAME} Command Execute Event')
    inputs = args.command.commandInputs

    selected_templates = [
        selected_template.name
        for template in list_all_templates()
        if (selected_template := inputs.itemById(f'{template}_input'))
           and selected_template.value
    ]

    ui = get_ui()
    design = adsk.fusion.Design.cast(get_product())
    
    design.activateRootComponent()
    occurrences = (
        occurrence
        for occurrence in design.rootComponent.allOccurrences
        for template in selected_templates
        if occurrence.isValid
            and (component := occurrence.component)
            and component.isValid
            and component.attributes.itemByName('Report Group', template)
    )
    for occurrence in occurrences:
        ui.activeSelections.add(occurrence)

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
