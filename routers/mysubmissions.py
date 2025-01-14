from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader

from auth import get_current_user
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

from crud import read_my_submissions


@router.get("/mysubmissions", response_class=HTMLResponse)
async def mysub_page(request: Request, db=Depends(get_db)):
    try:
        user = await get_current_user(request, db)
    except:
        return RedirectResponse(url="/login", status_code=302)

    my_submissions = read_my_submissions(username=user.username)

    return templates.TemplateResponse(
        "mysubmissions.html",
        {
            "request": request,
            "tables": my_submissions,
            "macro_src": "macro.html",
        },
    )
