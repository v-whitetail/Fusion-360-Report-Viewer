import adsk.core, adsk.fusion, adsk.cam
import os, zlib
from . import config as fileconfig
from . import fusion360utils as futil
def get_ui():
    app = adsk.core.Application.get()
    ui = app.userInterface
    return ui
def get_product():
    app = adsk.core.Application.get()
    product = app.activeProduct
    return product
def get_document():
    app = adsk.core.Application.get()
    document = app.activeDocument
    return document

# def try_native_body(body: adsk.fusion.BRepBody):
#     if native_body := body.nativeObject:
#         return native_body
#     else:
#         return body
# def try_native_face(face: adsk.fusion.BRepFace):
#     if native_face := face.nativeObject:
#         return native_face
#     else:
#         return face
# def try_native_occurrence(occurrence: adsk.fusion.Occurrence):
#     if native_occurrence := occurrence.nativeObject:
#         return native_occurrence
#     else:
#         return occurrence
def list_all_templates():
    return [
        os.path.splitext(file)[0]
        for file in os.listdir(fileconfig.templates_dir)
        if file.lower().endswith('.html')
    ]
def add_reports(component: adsk.fusion.Component, selected_reports: list[str]):
    for report in selected_reports:
        component.attributes.add( 'Report Group', report, '')
def remove_reports(component: adsk.fusion.Component, selected_reports: list[str]):
    for report in selected_reports:
        if attr := component.attributes.itemByName( 'Report Group', report):
            attr.deleteMe()
def save_image_options(filename: str):
    screenshot = adsk.core.SaveImageFileOptions.create(filename)
    screenshot.width, screenshot.height = fileconfig.screenshot_size
    screenshot.isAntiAliased = fileconfig.screenshot_anti_alias
    screenshot.isBackgroundTransparent = fileconfig.screenshot_transparency
    return screenshot

def part_id(body: adsk.fusion.BRepBody):
    body_name = body.name.encode()
    component_name = body.parentComponent.name.encode()
    document_name = body.parentComponent.parentDesign.parentDocument.name.encode()
    return f'{(zlib.crc32(body_name + component_name + document_name) & 0xffffffff):08x}'

def empty_temp_files():
    for file in os.listdir(fileconfig.screenshot_dir):
        try:
            os.remove(os.path.join(fileconfig.screenshot_dir,file))
        except Exception as e:
            futil.log(f'failed to remove {file}\nexception: {e}')