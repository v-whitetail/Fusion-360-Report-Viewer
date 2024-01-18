import adsk.core, adsk.fusion, adsk.cam
import zlib
from .config import *
from . import fusion360utils as futil

def get_app():
    return adsk.core.Application.get()

def get_ui():
    return get_app().userInterface

def get_product():
    return get_app().activeProduct

def get_document():
    return get_app().activeDocument

def list_all_templates():
    return [
        os.path.splitext(file)[0]
        for file in os.listdir(templates_dir)
        if file.lower().endswith('.html')
    ]

def add_reports(component: adsk.fusion.Component, selected_reports: list[str]):
    for report in selected_reports:
        component.attributes.add(
            groupName='Report Group',
            name=report,
            value=''
        )

def remove_reports(component: adsk.fusion.Component, selected_reports: list[str]):
    for report in selected_reports:
        if attr := component.attributes.itemByName(
                groupName='Report Group',
                name=report
        ):
            attr.deleteMe()

def save_image_options(filename: str):
    screenshot = adsk.core.SaveImageFileOptions.create(filename)
    screenshot.width, screenshot.height = screenshot_size
    screenshot.isAntiAliased = screenshot_anti_alias
    screenshot.isBackgroundTransparent = screenshot_transparency
    return screenshot


def part_id(occurrence: adsk.fusion.Occurrence):
    occurrence_name = occurrence.fullPathName.encode()
    bounding_box = occurrence.boundingBox
    min_point, max_point = bounding_box.minPoint, bounding_box.maxPoint
    bounds = sorted(min_point.vectorTo(max_point).asArray())
    ft, fw, fl = map(lambda x: str(int(x*64))[:2], bounds)
    return f'{ft}{fw}{fl}{(zlib.crc32(occurrence_name) & 0xffffffff):08x}'

def empty_temp_files():
    for file in os.listdir(screenshot_dir):
        try:
            os.remove(os.path.join(screenshot_dir,file))
        except Exception as e:
            futil.log(f'failed to remove {file}\nexception: {e}')

def get_project_data(document: adsk.core.Document):
    scope_folder = document.dataFile.parentFolder
    project_folder = scope_folder.parentFolder
    return os.path.join(project_data_dir, f'{project_folder.name}.json')
