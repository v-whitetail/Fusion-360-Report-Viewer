import adsk.core, adsk.fusion, adsk.cam

def get(design: adsk.fusion.Design):

    buffer = {}

    for parameter in design.userParameters:
        if parameter.comment != "":
            buffer[parameter.name] = parameter.comment

    return buffer
