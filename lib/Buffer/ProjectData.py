import adsk.core, adsk.fusion, adsk.cam
#from .........................................home.v import adsk

import os
import json
from ..config import projectdata

def get( app: adsk.core.Application):
    
    ui = app.userInterface
    document = app.activeDocument
    scope_folder = document.dataFile.parentFolder
    project_folder = scope_folder.parentFolder
    project_data_file_name = project_folder.name + '.json'
    project_data_file = os.path.join(projectdata,project_data_file_name)

    variable_names = [
        "file",
        "vers",
        "auth",
        "scop",
        "proj",
    ]

    variable_vals = [
        document.name.removesuffix("v{}".format(document.dataFile.versionNumber)),
        document.dataFile.versionNumber,
        document.dataFile.createdBy.displayName,
        scope_folder.name,
        project_folder.name,
    ]

    buffer = {}

    for name, value in zip(variable_names, variable_vals):
        buffer[name] = value

    try:
        with open(os.path.abspath(project_data_file),'r') as file:
            metadata = json.loads(file.read())
            buffer.update(metadata)

    except:
        with open(os.path.abspath(project_data_file),'w') as file:
            ui.commandDefinitions.itemById('inputProjectData').execute()

    return buffer


