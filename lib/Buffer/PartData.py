import adsk.core, adsk.fusion, adsk.cam


def get(design: adsk.fusion.Design):
    
    variables_in_buffer = [
        "bod",
        "com",
        "mat",
        "app",
        "thi",
        "wid",
        "len",
        "des",
        "rep",
    ]

    buffer = {}
    buffer["headers"] = variables_in_buffer

    counter = 0
    for occurrence in design.rootComponent.allOccurrences:
        for body in occurrence.bRepBodies:

            if body.isVisible:
                counter += 1
                t, w, l = sorted(body.boundingBox.minPoint.vectorTo(body.boundingBox.maxPoint).asArray())
                
                variables = [
                    body.name,
                    body.parentComponent.name,
                    body.material.name,
                    body.appearance.name,
                    design.unitsManager.formatInternalValue(t,"in",False),
                    design.unitsManager.formatInternalValue(w,"in",False),
                    design.unitsManager.formatInternalValue(l,"in",False),
                    body.parentComponent.description,
                    get_report_groups(body.parentComponent),
                ]

                buffer[f'row{counter}'] = variables

    return buffer

def get_report_groups(component: adsk.fusion.Component):
    reports = []
    for attr in component.attributes:
        reports.append(attr.name)
    return reports

