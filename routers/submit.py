from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader

from auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get("/submit", response_class=HTMLResponse)
async def submit_page(request: Request, compe: str):
    try:
        _ = await get_current_user(request)
    except:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse(
        "submit.html", {"request": request, "macro_src": "./" + compe + "/macro.html"}
    )
