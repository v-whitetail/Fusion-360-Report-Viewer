import adsk.core, adsk.fusion, adsk.cam
import os, json
from Builder import Buffer, BufferKey, BufferValue, BufferItem
from ..config import project_data_dir
from ..report_viewer_utils import get_ui, get_project_data
from .. import fusion360utils as futil

def get(document: adsk.core.Document):
    
    scope_folder = document.dataFile.parentFolder
    project_folder = scope_folder.parentFolder

    project_data_key = BufferKey('projedata')
    project_data_value = BufferValue([
        BufferItem(BufferKey('proj'), BufferValue(project_folder.name)),
        BufferItem(BufferKey('scop'), BufferValue(scope_folder.name)),
        BufferItem(BufferKey('auth'), BufferValue(document.dataFile.createdBy.displayName)),
        BufferItem(BufferKey('vers'), BufferValue(version := str(document.dataFile.versionNumber))),
        BufferItem(BufferKey('file'), BufferValue(document.name.removesuffix(f'v{version}'))),
    ])

    try:
        with open(os.path.abspath(get_project_data(document)), 'r') as file:
            metadata = json.loads(file.read())
            buffer.update(metadata)
    except IOError as e:
        futil.log(f'{e}')
        get_ui().commandDefinitions.itemById('inputProjectData').execute()

    return buffer
