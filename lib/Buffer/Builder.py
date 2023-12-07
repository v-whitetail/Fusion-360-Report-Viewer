import adsk.core, adsk.fusion, adsk.cam
import json
from . import UserParameters, PartData, ProjectData
from ..report_viewer_utils import get_document, get_product


def build():
    design = adsk.fusion.Design.cast(get_product())
    
    buffer = {
        'projdata': ProjectData.get(get_document()),
        'userdata': UserParameters.get(design),
        'partdata': PartData.get(design),
    }

    return json.dumps(buffer, indent=True)
