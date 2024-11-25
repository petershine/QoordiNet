from ._shared import constants

APP_NAME = "QoordiNet"
APP_CONFIGURATION = "mainApp/app_configuration.json"
LOG_FILE_NAME = f"{APP_NAME}.log"
LOG_FILE_PATH = f"{constants.MOUNTED_ROOT}/{LOG_FILE_NAME}"

SQLITE_PATH = f"sqlite:///{constants.MOUNTED_ROOT}/{APP_NAME}.db"

PORT_NUMBER = 50002
HTML_TEMPLATE_DIRECTORY = "mainApp/templates"
HTML_TEMPLATE_INDEX = "index.html"
HTML_TEMPLATE_ACTIONS = "actions.html"

HTML_STATIC_DIRECTORY = "mainApp/static"