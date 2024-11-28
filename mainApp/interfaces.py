from ._shared import constants
from . import app_constants

from fastapi import FastAPI, Form, Request, Response
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from .qoordinet_app import QoordiNetAppManager
webAppManager: QoordiNetAppManager

app = FastAPI()
templates = Jinja2Templates(directory=app_constants.HTML_TEMPLATE_DIRECTORY)
app.mount("/static", StaticFiles(directory=app_constants.HTML_STATIC_DIRECTORY), name="static")


@app.get("/")
def html_root(request: Request):
    return templates.TemplateResponse(app_constants.HTML_TEMPLATE_INDEX, {"request": request})


@app.get("/actions", response_class=HTMLResponse)
def html_actions(request: Request):
    return templates.TemplateResponse(app_constants.HTML_TEMPLATE_ACTIONS, {"request": request})


@app.get("/activities")
def get_activities(request: Request, response_class=JSONResponse):
    json_activities = webAppManager.activities_list()
    return json_activities


@app.post("/save_into_database", response_class=RedirectResponse)
async def save_into_database(request: Request, csv_file: UploadFile = File(...)):
    webAppManager.save_into_database(csv_file=csv_file, styleClass="qoordinet_table")
    return RedirectResponse(url="/", status_code=303)

@app.post("/build_database", response_class=RedirectResponse)
async def build_database(request: Request, csv_file: UploadFile = File(...)):
    webAppManager.build_database(csv_file=csv_file, styleClass="qoordinet_table")
    return RedirectResponse(url="/", status_code=303)


@app.delete("/delete_last")
async def delete_last(days: int | None = None):
    webAppManager.delete_last(days=days)
    return Response(status_code=200)
