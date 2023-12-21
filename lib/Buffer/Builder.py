import adsk.core, adsk.fusion, adsk.cam
import json
from . import UserParameters, PartData, ProjectData
from ..report_viewer_utils import *
from typing import Optional, Union, List


def build():
    design = adsk.fusion.Design.cast(get_product())
    
    buffer = {
        'projdata': ProjectData.get(get_document()),
        'userdata': UserParameters.get(design),
        'partdata': PartData.get(design),
    }

    return json.dumps(buffer, indent=True)

class BufferKey:
    def __init__(self, key: Optional[str]):
        self.key = key
    def serialize(self):
        return self.key or ''

class BufferValue:
    def __init__(self, value: Optional[Union[str, List[str], 'BufferItem', List['BufferItem']]]):
        if isinstance(value, List):
            self.value = [ BufferValue(item) for item in value ]
        else:
            self.value = value
    def serialize(self):
        if isinstance(self.value, str):
            return self.value
        elif isinstance(self.value, List):
            items = ['[']
            items.extend([item.serialize() for item in self.value])
            items.extend([']'])
            '\n'.join(items)
        elif isinstance(self.value, BufferItem):
            return self.value.serialize()
        else:
            return ''

class BufferItem:
    def __init__(self, key: BufferKey, value: BufferValue):
        self.key = key
        self.value = value
    def serialize(self):
        return ': '.join((
            self.key.serialize(),
            self.value.serialize(),
        ))
    @staticmethod
    def from_body(body: adsk.fusion.BRepBody):
        design = adsk.fusion.Design.cast(get_product())
        t, w, l = get_size(body)
        part_id = BufferKey(id_part(body))
        part_data = BufferValue([
            body.name,
            body.parentComponent.name,
            body.material.name,
            body.appearance.name,
            format_units(design, t),
            format_units(design, w),
            format_units(design, l),
            body.parentComponent.description,
            get_report_groups(body.parentComponent),
        ])
        return BufferItem(part_id, part_data)

class Buffer:
    def __init__(self, title: str, data: Optional[Union[BufferItem, List[BufferItem]]]):
        self.title = title
        self.data = data
    def serialize(self):
        if isinstance(self.data, BufferItem):
            return '\n~~\n'.join((
                self.title,
                self.data.serialize(),
            ))
        elif isinstance(self.data, List) and all(isinstance(item, BufferItem) for item in self.data):
            data = '\n\n'.join([ item.serialize() for item in self.data ])
            return '\n~~\n'.join((
                self.title,
                data
            ))
        else:
            return '\n~~\n'.join((
                self.title,
                'empty buffer'
            ))