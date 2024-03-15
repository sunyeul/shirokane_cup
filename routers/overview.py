from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
@router.get("/overview", response_class=HTMLResponse)
async def overview_page(request: Request):
    return templates.TemplateResponse(
        "overview.html",
        {
            "request": request,
            "macro_src": "macro.html",
        },
    )
