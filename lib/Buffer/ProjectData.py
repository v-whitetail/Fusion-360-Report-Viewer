import adsk.core, adsk.fusion, adsk.cam
import os, json
from ..config import project_data_dir
from ..report_viewer_utils import get_ui, get_project_data
from .. import fusion360utils as futil

def get(document: adsk.core.Document):
    
    scope_folder = document.dataFile.parentFolder
    project_number, project_name = separate_by_delimiter(scope_folder.parentFolder.name, '-')

    buffer = {
        'PROJ': project_name,
        'NUMB': project_number,
        'SCOP': scope_folder.name,
        'AUTH': document.dataFile.createdBy.displayName,
        'VERS': format(version := document.dataFile.versionNumber),
        'FILE': document.name.removesuffix(f'v{version}'),
    }

    try:
        with open(os.path.abspath(get_project_data(document)), 'r') as file:
            metadata = json.loads(file.read())
            buffer.update(metadata)
    except IOError as e:
        futil.log(f'{e}')
        get_ui().commandDefinitions.itemById('inputProjectData').execute()

    return buffer

def separate_by_delimiter(folder_name: str, delimiter: str):
    if delimiter in folder_name:
        number, name = folder_name.split(delimiter, 1)
        return str(number).strip(), str(name).strip()
    else:
        return '', folder_name