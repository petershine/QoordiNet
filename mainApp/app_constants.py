from ._shared import constants

APP_NAME = "QoordiNet"
LOG_FILE_NAME = f"{APP_NAME}.log"
LOG_FILE_PATH = f"{constants.MOUNTED_ROOT}/{LOG_FILE_NAME}"

SQLITE_PATH = f"sqlite:///{constants.MOUNTED_ROOT}/{APP_NAME}.db"

PORT_NUMBER = 50002
HTML_TEMPLATE_DIRECTORY = "mainApp/templates"
HTML_TEMPLATE_ACTIVITIES = "activities.html"
HTML_TEMPLATE_PROCESS_CSV = "process_csv.html"
HTML_TEMPLATE_DISPLAY_CSV = "display_csv.html"
HTML_TEMPLATE_DISPLAY_TSV = "display_tsv.html"

HTML_STATIC_DIRECTORY = "mainApp/static"