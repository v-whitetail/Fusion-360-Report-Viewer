import adsk.core, adsk.fusion, adsk.cam
from math import floor
from ..report_viewer_utils import part_id, get_ui, list_all_templates

def get(design: adsk.fusion.Design):
    
    variables_in_buffer = [
        "~occ",
        "~com",
        "~mat",
        "~app",
        "~thi",
        "~wid",
        "~len",
        "~des",
        "~rep",
    ]

    buffer = {'headers': variables_in_buffer}

    parts = {}

    for occurrence in design.rootComponent.allOccurrences:

        t, w, l = get_size(occurrence)

        variables = [
            occurrence.name,
            occurrence.component.name,
            occurrence.component.material.name,
            occurrence.component.material.appearance.name,
            format_units(design, t),
            format_units(design, w),
            format_units(design, l),
            occurrence.component.description,
            get_report_groups(occurrence.component),
        ]

        parts[f'{part_id(occurrence)}'] = variables

    buffer['parts'] = parts

    return buffer

def get_size(entity: adsk.fusion.BRepBody | adsk.fusion.Occurrence | adsk.fusion.Component):
    bounding_box = entity.boundingBox
    min_point, max_point = bounding_box.minPoint, bounding_box.maxPoint
    return sorted(min_point.vectorTo(max_point).asArray())

def get_report_groups(entity: adsk.fusion.Component | adsk.fusion.Occurrence | adsk.fusion.BRepBody):
    if isinstance(entity, adsk.fusion.Occurrence):
        component = entity.component
    elif isinstance(entity, adsk.fusion.BRepBody):
        component = entity.parentComponent
    else:
        component = entity
    return [
        attribute.name
        for attribute in component.attributes
        if attribute.groupName == 'Report Group'
    ]

def listed_report_groups(design: adsk.fusion.Design):
    return list(
        set([
            report
            for component in design.allComponents
            for report in get_report_groups(component)
        ])
    )
def format_units(design: adsk.fusion.Design, measurement: float):
    value_as_str = design.unitsManager.formatInternalValue(
        measurement,
        'in',
        False
    )
    numerator, denominator = get_best_approximate(value_as_str)
    prefix_int = floor(numerator / denominator)
    if prefix_int <= 0:
        return f'{numerator}/{denominator}'
    numerator -= denominator * prefix_int
    if numerator == 0:
        return f'{prefix_int}'
    return f'{prefix_int} {numerator}/{denominator}'

def get_best_approximate(value: str):
    value_float = float(value)
    return  min(
        (
            (round(value_float * denominator), denominator)
            for denominator in [2, 4, 8, 16]
        ),
        key=lambda f: abs(value_float - f[0]/f[1])
    )

def check_report_groups(design: adsk.fusion.Design):
    listed_reports = listed_report_groups(design)
    available_templates = list_all_templates()
    unavailable_templates = [
        report
        for report in listed_reports
        if report not in available_templates
    ]
    if 0 < len(unavailable_templates):
        get_ui().messageBox(
            f'This design contains some report group(s) with no corresponding template.\n'
            f'{unavailable_templates} will (all) be ignored.'
        )