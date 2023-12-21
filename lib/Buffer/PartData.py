import adsk.core, adsk.fusion, adsk.cam
from ..report_viewer_utils import id_part, get_size, format_units
from Builder import Buffer, BufferKey, BufferValue, BufferItem

def get(design: adsk.fusion.Design):

    header_key = BufferKey('headers')
    header_data = BufferValue([
        "bod",
        "com",
        "mat",
        "app",
        "thi",
        "wid",
        "len",
        "des",
        "rep",
    ])
    headers = BufferItem(header_key, header_data)
    visible_bodies = [
        body
        for occurrence in design.rootComponent.allOccurrences
        for body in occurrence.bRepBodies
        if body.isVisible and occurrence.isLightBulbOn
    ]
    parts_key = BufferKey('parts')
    parts_value = BufferValue([
        BufferItem.from_body(body)
        for body in visible_bodies
    ])
    parts = BufferItem(parts_key, parts_value)
    part_data_key = BufferKey('partdata')
    part_data_value = BufferValue([headers, parts])
    return BufferItem(part_data_key, part_data_value)
