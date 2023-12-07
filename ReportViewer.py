import adsk.core, adsk.fusion, adsk.cam
from . import commands
from .lib import live_server
from .lib import fusion360utils as futil
from .lib.config import logger
from .lib.Buffer import Builder
from .lib.report_viewer_utils import empty_temp_files

app = adsk.core.Application.get()
ui = app.userInterface

handlers = []
update_reports = True

def run(context):
    try:
        live_server.start()
        commands.start()

        on_document_saved = DocumentSavedHandler()
        app.documentSaved.add(on_document_saved)
        handlers.append(on_document_saved)
        empty_temp_files()

    except:
        futil.handle_error('run')
        live_server.stop()


def stop(context):
    try:
        live_server.stop()
        futil.clear_handlers()
        commands.stop()
        empty_temp_files()

    except:
        futil.handle_error('stop')
        live_server.stop()


class DocumentSavedHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        if update_reports:
            buffer = Builder.build()
            with open(logger, 'a+') as log:
                log.write(buffer)
