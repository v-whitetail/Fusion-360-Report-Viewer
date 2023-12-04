import adsk.core, adsk.fusion, adsk.cam
from ... import config
from ...lib import fusion360utils as futil
from ...lib.selection_filters import *

PALETTE_ID = config.sample_palette_id

CMD_ID = f'processRemove'
CMD_NAME = 'Remove Processing Station'
CMD_BESIDE_ID = f''
CMD_Description = 'Removes a Procession station from a BRepBody'

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
            f'process_remove_input',
            f'Selection',
            f'Select Bodies to Add to Processing Station',
            )
    selection.setSelectionLimits(0,0)
    selection.clearSelectionFilter()
    selection.addSelectionFilter('Occurrences')

    for template in list_all_templates():
        inputs.addBoolValueInput(
                f'{template}_input',
                f'{template}',
                True,
                )

def command_execute(args: adsk.core.CommandEventArgs):

    futil.log(f'{CMD_NAME} Command Execute Event')
    inputs = args.command.commandInputs

    selected_templates: list[str] = []
    for template in list_all_templates():

        selected_template: adsk.core.BoolValueCommandInput = inputs.itemById(f'{template}_input')
        if selected_template.value:
            selected_templates.append((selected_template.name))

    selection_input: adsk.core.SelectionCommandInput = inputs.itemById(f'process_remove_input')

    entities = (
            selection_input.selection(i).entity
            for i in range(selection_input.selectionCount)
            )
    components = (
            occurrence.component
            for entity in entities
            if isinstance(occurrence := entity, adsk.fusion.Occurrence)
            )

    for c in components:
        remove_reports(c,selected_templates)
    
def command_preview(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} Command Preview Event')

def command_input_changed(args: adsk.core.InputChangedEventArgs):
    changed_input = args.input
    futil.log(f'{CMD_NAME} Input Changed Event fired from a change to {changed_input.id}')

def command_destroy(args: adsk.core.CommandEventArgs):
    global local_handlers
    local_handlers = []
    futil.log(f'{CMD_NAME} Command Destroy Event')
