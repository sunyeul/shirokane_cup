from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from jinja2 import FileSystemLoader
from database import get_db
from models import Competition


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get(
    "/competitions",
    response_class=HTMLResponse,
)
async def top_page(request: Request):
    competition_links = []

    db = next(get_db())
    competitions = db.query(Competition).all()

    for compe in competitions:
        competition_link = {}
        competition_link["href"] = f"/competitions/{compe.name}/overview"
        competition_link["title"] = compe.title

        competition_links.append(competition_link)

    return templates.TemplateResponse(
        "competitions.html",
        {"request": request, "competition_links": competition_links},
    )
