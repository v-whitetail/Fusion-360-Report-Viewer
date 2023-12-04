import adsk.core, adsk.fusion, adsk.cam
#from .........................................home.v import adsk

import json
from . import UserParameters, PartData, ProjectData

def build():
    app = adsk.core.Application.get()
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    ui = app.userInterface
    
    buffer = {}
    buffer["projdata"] = ProjectData.get(app)
    buffer["userdata"] = UserParameters.get(design)
    buffer["partdata"] = PartData.get(design)

    return json.dumps(buffer,indent=True)
