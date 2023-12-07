import adsk.core, adsk.fusion, adsk.cam
from ..report_viewer_utils import part_id

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

    buffer = {'headers': variables_in_buffer}

    visible_bodies = [
        body
        for occurrence in design.rootComponent.allOccurrences
        for body in occurrence.bRepBodies
        if body.isVisible and occurrence.isLightBulbOn
    ]

    for body in visible_bodies:

        t, w, l = get_size(body)

        variables = [
            body.name,
            body.parentComponent.name,
            body.material.name,
            body.appearance.name,
            format_units(design, t),
            format_units(design, w),
            format_units(design, l),
            body.parentComponent.description,
            get_report_groups(body.parentComponent),
        ]

        buffer[f'{part_id(body)}'] = variables

    return buffer

def get_size(body: adsk.fusion.BRepBody):
    bounding_box = body.boundingBox
    min_point, max_point = bounding_box.minPoint, bounding_box.maxPoint
    return sorted(min_point.vectorTo(max_point).asArray())

def get_report_groups(component: adsk.fusion.Component):
    return [
        attribute.name
        for attribute in component.attributes
        if attribute.groupName == 'Report Group'
    ]

def format_units(design: adsk.fusion.Design, measurement: float):
    return design.unitsManager.formatInternalValue(
        measurement,
        'in',
        False
    )
