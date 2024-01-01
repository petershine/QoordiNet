from ._shared import constants

APP_NAME = "QoordiNet"
LOG_FILE_NAME = f"{APP_NAME}.log"
LOG_FILE_PATH = f"{constants.MOUNTED_ROOT}/{LOG_FILE_NAME}"

PORT_NUMBER = 8083
HTML_TEMPLATE_DIRECTORY = "mainApp/templates"
HTML_TEMPLATE_PROCESS_CSV = "process_csv.html"
HTML_TEMPLATE_DISPLAY_CSV = "display_csv.html"
HTML_TEMPLATE_DISPLAY_TSV = "display_tsv.html"

HTML_STATIC_DIRECTORY = "mainApp/static"