import adsk.core, adsk.fusion, adsk.cam
#from .........................................home.v import adsk

import os
import json

def get( app: adsk.core.Application):
    
    ui = app.userInterface
    document = app.activeDocument
    scope_folder = document.dataFile.parentFolder
    project_folder = scope_folder.parentFolder
    
    tempfile_path = os.path.join(os.path.expanduser("~"),"AppData\\Local\\Temp\\projectdata.json")
    project_data_file_name = "projectdata.json"

    delimiter = "\t"
    newline = "\n"

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
    
    project_data_file_id = get_metadata(project_folder,project_data_file_name)
    
    if project_data_file_id == None:
        input_data = input_metadata_popup(ui,project_folder,project_data_file_name,tempfile_path)
        buffer.update(input_data)
    
    else:
        project_folder.dataFiles.itemById(project_data_file_id).download(tempfile_path,handler=None)
        
        with open(tempfile_path, 'r') as file:
            json.loads(file.read())

    return buffer



def get_metadata(project_folder: adsk.core.DataFolder, project_data_file_name: str):

    for item in project_folder.dataFiles:
        if item.name == project_data_file_name:
            return item.id
        
    return None



def input_metadata_popup(
        ui: adsk.core.UserInterface,
        project_folder: adsk.core.DataFolder,
        project_data_file_name: str,
        tempfile_path: str
    ):
        title = 'Project Requires {}'.format(project_data_file_name)
        prompt = 'Input Project Address:'.format(project_data_file_name)
        defaultValue = ''
        address, result = ui.inputBox(prompt,title,defaultValue)
        input_metadata = {}
        
        if result == True:
            raise Exception("closed")
        else:
            input_metadata["addy"] = address
    
            # write metadata temp file
            with open(tempfile_path, 'w') as file:
                file.flush()
                file.write(json.dumps(input_metadata))
    
            # try to upload to temp file
            project_folder.uploadFile(tempfile_path)

            return input_metadata
