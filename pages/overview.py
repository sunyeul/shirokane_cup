from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get("/", response_class=HTMLResponse)
@router.get("/overview", response_class=HTMLResponse)
async def overview_page(request: Request, compe: str):
    return templates.TemplateResponse(
        "overview.html",
        {"request": request, "macro_src": "./" + compe + "/macro.html"},
    )
