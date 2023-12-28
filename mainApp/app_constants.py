from ._shared import constants

APP_NAME = "QoordiNet"
LOG_FILE_NAME = f"{APP_NAME}.log"
LOG_FILE_PATH = f"{constants.MOUNTED_ROOT}/{LOG_FILE_NAME}"

PORT_NUMBER = 8083
HTML_TEMPLATE_DIRECTORY = "mainApp/templates"
HTML_TEMPLATE_FORM = "form.html"
HTML_TEMPLATE_TABLE = "table.html"
HTML_TEMPLATE_UPLOAD = "upload.html"
HTML_TEMPLATE_DISPLAY_CSV = "display_csv.html"

HTML_STATIC_DIRECTORY = "mainApp/static"