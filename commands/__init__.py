import adsk.core, adsk.fusion, adsk.cam

from .stopServer import entry as stopServer
from .processAdd import entry as processAdd
from .openBrowser import entry as openBrowser
from .openLogFile import entry as openLogFile
from .startServer import entry as startServer
from .processRemove import entry as processRemove
from .processSelect import entry as processSelect
from .addImageBatch import entry as addImageBatch
from .emptyTempFiles import entry as emptyTempFiles
from .openHomeFolder import entry as openHomeFolder
from .editProjectData import entry as editProjectData
from .inputProjectData import entry as inputProjectData

commands = [
    openBrowser,
    startServer,
    stopServer,
    processAdd,
    processSelect,
    processRemove,
    editProjectData,
    openHomeFolder,
    openLogFile,
    inputProjectData,
    addImageBatch,
    emptyTempFiles,
]


def start():
    for command in commands:
        command.start()


def stop():
    for command in commands:
        command.stop()
