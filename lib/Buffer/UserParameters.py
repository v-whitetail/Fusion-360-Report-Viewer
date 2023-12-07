import adsk.core, adsk.fusion, adsk.cam

def get(design: adsk.fusion.Design):

    buffer = {
        parameter.name: parameter.comment
        for parameter in design.userParameters
        if parameter.comment is not None
    }

    return buffer
