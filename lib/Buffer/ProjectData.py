import adsk.core, adsk.fusion, adsk.cam
import os, json
from ..config import project_data_dir
from ..report_viewer_utils import get_ui
from .. import fusion360utils as futil

def get(document: adsk.core.Document):
    
    scope_folder = document.dataFile.parentFolder
    project_folder = scope_folder.parentFolder
    project_data = os.path.join(
        project_data_dir,
        f'{project_folder.name}.json'
    )

    buffer = {
        'proj': project_folder.name,
        'scop': scope_folder.name,
        'auth': document.dataFile.createdBy.displayName,
        'vers': (version := document.dataFile.versionNumber),
        'file': document.name.removesuffix(f'v{version}'),
    }

    try:
        with open(os.path.abspath(project_data), 'r') as file:
            metadata = json.loads(file.read())
            buffer.update(metadata)
    except IOError as e:
        futil.log(f'{e}')
        get_ui().commandDefinitions.itemById('inputProjectData').execute()

    return buffer
