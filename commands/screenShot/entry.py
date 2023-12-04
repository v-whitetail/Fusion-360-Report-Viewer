import adsk.core, adsk.fusion, adsk.cam
from ... import config
from ...lib import fusion360utils as futil
from ...lib.config import home_folder as home_folder
from ...lib.selection_filters import *

PALETTE_ID = config.sample_palette_id

CMD_ID = f'screenShot'
CMD_NAME = 'Screen Shot'
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
COMMON_ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'commonResources', '')

local_handlers = []

def start():
    ui = get_ui()
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)
    futil.add_handler(cmd_def.commandCreated, command_created)
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    prep_environment = ui.workspaces.itemById(f'MfgWorkingModelEnv')
    toolbar_tab = workspace.toolbarTabs.itemById(TAB_ID)

    if toolbar_tab is None:
        toolbar_tab = workspace.toolbarTabs.add(TAB_ID, TAB_NAME)
        toolbar_tab = prep_environment.toolbarTabs.add(TAB_ID, TAB_NAME)

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

def command_execute(args: adsk.core.CommandEventArgs):

    futil.log(f'{CMD_NAME} Command Execute Event')
    inputs = args.command.commandInputs

    activate_part_labels()

    design = adsk.fusion.Design.cast(get_product())
    root_component = design.rootComponent

    dedup_2(root_component)
    unjoin(root_component)
    face_plant_3(root_component)
    screenshot()




def face_plant_3(root: adsk.fusion.Component):
    move_features = root.features.moveFeatures
    origin = adsk.core.Matrix3D.create()
    positions = [
        occurrence
        for occurrence in root.allOccurrences
    ]
    for pos in positions:
        pos.transform2 = origin




def get_norms(root: adsk.fusion.Component):
    flat = adsk.core.SurfaceTypes.PlaneSurfaceType
    faces_per_body = (
        (
            [
                try_native_face(face)
                for face in body.faces
                if face.isValid and face.geometry.surfaceType is flat
            ],
            try_native_body(body)
        )
        for occurrences in root.allOccurrences
        for body in occurrences.bRepBodies
        if body.isValid
    )
    max_face_per_body = (
        (
            max(faces, key=lambda face: face.area),
            body
        )
        for faces, body in faces_per_body
    )
    return (
        (
            face.evaluator.getNormalAtPoint(face.centroid),
            face.centroid,
            body
        )
        for face, body in max_face_per_body
    )





def command_preview(args: adsk.core.CommandEventArgs):
    inputs = args.command.commandInputs
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

def activate_part_labels():
    ui = get_ui()

    cam_environment = ui.workspaces.itemById(f'CAMEnvironment')
    prep_environment = ui.workspaces.itemById(f'MfgWorkingModelEnv')

    if not ui.activeWorkspace == cam_environment:
        cam_environment.activate()

    cam_model: adsk.cam.CAM = get_document().products.itemByProductType('CAMProductType')

    labels_model = cam_model.manufacturingModels.itemByName(f'Part Labels')
    if labels_model:
        labels_model = labels_model[0]
    else:
        input = cam_model.manufacturingModels.createInput()
        input.name = f'Part Labels'
        labels_model = cam_model.manufacturingModels.add(input)
        labels_model.activate()    
    labels_model.activate()
   
    ui.activeSelections.add(labels_model.occurrence)
    if not ui.activeWorkspace == prep_environment:
        prep_environment.activate()

def dedup(root: adsk.fusion.Component):
    remove_features = root.features.removeFeatures
    unique_components, duplicates = [], []
    for occurrence in root.occurrences:
        if occurrence.component not in unique_components:
            unique_components.append(occurrence.component)
        else:
            duplicates.append(occurrence)
    for occurrence in duplicates:
        remove_features.add(occurrence)
    for component in unique_components:
        dedup(component)

def dedup_2(root: adsk.fusion.Component):
    unique_components, duplicates = [], []
    for occurrence in root.occurrences:
        if occurrence.component not in unique_components:
            unique_components.append(occurrence.component)
        else:
            duplicates.append(occurrence)
    for occurrence in duplicates:
        occurrence.deleteMe()
    for component in unique_components:
        dedup(component)
def unjoin(root: adsk.fusion.Component):
    for joint in root.allJoints:
        joint.deleteMe()

def face_plant(root: adsk.fusion.Component):
    move_features = root.features.moveFeatures
    flat = adsk.core.SurfaceTypes.PlaneSurfaceType
    faces_per_body = (
        [
            face
            for face in body.faces
            if face.isValid
               and face.geometry.surfaceType is flat
        ]
        for body in root.bRepBodies
        if body.isValid
    )
    max_face_per_body = (
        max(faces, key=lambda face: face.area)
        for faces in faces_per_body
    )
    normals_per_body = (
        (
            face.evaluator.getNormalAtPoint(face.centroid),
            face.centroid,
            face.body
        )
        for face in max_face_per_body
    )
    component_origins = (
        occurrence.component.originConstructionPoint
        for occurrence in root.allOccurrences
    )
    value = adsk.core.ValueInput.createByReal
    down = adsk.core.Vector3D.create(0.0, 0.0, -1.0)
    for (r, normal), centroid, body in normals_per_body:
        if r:
            target = adsk.core.ObjectCollection.create()
            target.add(body)
            translate = move_features.createInput2(target)
            translate.defineAsTranslateXYZ(
                value(-centroid.x),
                value(-centroid.y),
                value(-centroid.z),
                True)
            move_features.add(translate)
            angle = adsk.core.Matrix3D.create()
            if abs(normal.dotProduct(down)) < 0.9:
                angle.setToRotateTo(normal, down)
                rotate = move_features.createInput2(target)
                rotate.defineAsFreeMove(angle)
                move_features.add(rotate)

    components = (
        occurrence.component
        for occurrence in root.occurrences
        if occurrence.component.isValid
           and occurrence.component.id != root.id
    )
    for component in components:
        face_plant(component)

def screenshot():
    view = adsk.core.Application.get().activeViewport
    view.fit()
    image_sheet = adsk.core.SaveImageFileOptions.create('capture.png')
    image_sheet.filename = os.path.join(home_folder,'capture.png')
    image_sheet.width = 256
    image_sheet.height = 256
    image_sheet.isAntiAliased = False
    image_sheet.isBackgroundTransparent = True
    view.saveAsImageFileWithOptions(image_sheet)
