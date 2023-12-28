from ._shared import constants
from . import app_constants

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


webAppManager = None

app = FastAPI()
templates = Jinja2Templates(directory=app_constants.HTML_TEMPLATE_DIRECTORY)
app.mount("/static", StaticFiles(directory=app_constants.HTML_STATIC_DIRECTORY), name="static")


@app.get("/")
def read_root(request: Request):
    return RedirectResponse(url=f"/docs")

@app.get("/form", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse(app_constants.HTML_TEMPLATE_FORM, {"request": request})

@app.post("/display", response_class=HTMLResponse)
async def display_data(request: Request, tab_separated: str = Form(...)):
    data = webAppManager.process_data(tab_separated)
    return templates.TemplateResponse(app_constants.HTML_TEMPLATE_TABLE, {"request": request, "data": data})
