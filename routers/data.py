from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader
from starlette.responses import FileResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get("/data", response_class=HTMLResponse)
async def data_page(request: Request, compe: str):
    return templates.TemplateResponse(
        "data.html",
        {"request": request, "macro_src": f"./{compe}/templates/macro.html"},
    )


@router.get("/data_download")
async def data_download(compe: str):
    file_path = f"../competitions/{compe}/data/data.zip"

    return FileResponse(
        path=file_path,
        filename="data.zip",
        media_type="application/zip",
    )
