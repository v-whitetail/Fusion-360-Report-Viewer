import adsk.core, adsk.fusion, adsk.cam

#from .addImage import entry as addImage
from .addImageBatch import entry as addImageBatch
from .startServer import entry as startServer
from .stopServer import entry as stopServer
from .openBrowser import entry as openBrowser
from .openLogFile import entry as openLogFile
from .openHomeFolder import entry as openHomeFolder
from .emptyTempFiles import entry as emptyTempFiles
from .processAdd import entry as processAdd
from .processRemove import entry as processRemove
from .processSelect import entry as processSelect
from .processCleanup import entry as processCleanup
from .editProjectData import entry as editProjectData
from .inputProjectData import entry as inputProjectData

commands = [
    startServer,
    stopServer,
    openBrowser,
    processAdd,
    processRemove,
    processSelect,
    processCleanup,
    editProjectData,
    openHomeFolder,
    openLogFile,
    inputProjectData,
    addImageBatch, #    addImage,
    emptyTempFiles,
]


def start():
    for command in commands:
        command.start()


def stop():
    for command in commands:
        command.stop()
