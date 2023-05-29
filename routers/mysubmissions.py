from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader

from auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])

from compe_db import read_compe_submission_tbl


@router.get("/mysubmissions", response_class=HTMLResponse)
async def mysub_page(request: Request, compe: str):
    try:
        user = await get_current_user(request)
    except:
        return RedirectResponse(url="/login", status_code=302)

    submission_tbl = read_compe_submission_tbl(compe)
    my_submissions = (
        submission_tbl.query(f"username == '{user.username}'")
        .sort_values("upload_date", ascending=False)[
            ["description", "score", "last_submission", "upload_date"]
        ]
        .rename(
            columns={
                "description": "Description",
                "score": "Score",
                "last_submission": "Last Submission",
                "upload_date": "Upload Date",
            },
        )
    )

    return templates.TemplateResponse(
        "mysubmissions.html",
        {
            "request": request,
            "tables": my_submissions,
            "macro_src": "./" + compe + "/macro.html",
        },
    )
