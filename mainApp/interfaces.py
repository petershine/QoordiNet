from ._shared import constants
from . import app_constants

from fastapi import FastAPI, Form, Request
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


webAppManager = None

app = FastAPI()
templates = Jinja2Templates(directory=app_constants.HTML_TEMPLATE_DIRECTORY)
app.mount("/static", StaticFiles(directory=app_constants.HTML_STATIC_DIRECTORY), name="static")


@app.get("/")
def read_root(request: Request):
    #return RedirectResponse(url=f"/process_csv")
    html_activities_table = webAppManager.activities_table(styleClass="csv_table")
    return templates.TemplateResponse(app_constants.HTML_TEMPLATE_DISPLAY_CSV, {"request": request, "html_table": html_activities_table})


@app.get("/process_csv", response_class=HTMLResponse)
def read_process_csv(request: Request):
    return templates.TemplateResponse(app_constants.HTML_TEMPLATE_PROCESS_CSV, {"request": request})

@app.post("/display_csv")
async def display_csv(request: Request, csv_file: UploadFile = File(...), shouldDisplayRaw: bool = Form(False), shouldSaveIntoDatabase: bool = Form(False), numberOfDays: int = Form(1)):
    if shouldSaveIntoDatabase:
        webAppManager.save_into_database(csv_file=csv_file, styleClass="csv_table", numberOfDays=numberOfDays)
        return RedirectResponse(url="/", status_code=303)
        
    html_csv_table = webAppManager.html_table(csv_file=csv_file, shouldDisplayRaw=shouldDisplayRaw, styleClass="csv_table", numberOfDays=numberOfDays)
    return templates.TemplateResponse(app_constants.HTML_TEMPLATE_DISPLAY_CSV, {"request": request, "html_table": html_csv_table})
    
@app.post("/build_database", response_class=RedirectResponse)
async def build_database(request: Request, csv_file: UploadFile = File(...)):
    webAppManager.build_database(csv_file=csv_file, styleClass="csv_table")
    return RedirectResponse(url="/", status_code=303)


@app.post("/display_tsv", response_class=HTMLResponse)
async def display_data(request: Request, tab_separated: str = Form(...)):
    data = webAppManager.process_data(tab_separated)
    return templates.TemplateResponse(app_constants.HTML_TEMPLATE_DISPLAY_TSV, {"request": request, "data": data})
