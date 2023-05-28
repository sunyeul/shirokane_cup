from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get("/submit", response_class=HTMLResponse)
def submit_page(request: Request, compe: str):
    return templates.TemplateResponse(
        "submit.html", {"request": request, "compe": compe}
    )
