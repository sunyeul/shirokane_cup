from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader
from starlette.responses import FileResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./data"])


@router.get("/data", response_class=HTMLResponse)
async def data_page(request: Request):
    return templates.TemplateResponse(
        "data.html",
        {
            "request": request,
            "macro_src": "macro.html"
        },
    )


@router.get("/data_download")
async def data_download():
    file_path = f"./competition_data/data.zip"

    return FileResponse(
        path=file_path,
        filename="data.zip",
        media_type="application/zip",
    )
