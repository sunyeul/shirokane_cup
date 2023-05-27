from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader

from overview import router as overview_router
from data import router as data_router
from leaderboard import router as leaderboard_router
from mysubmission import router as mysub_router
from submit import router as submit_router
from submitresult import router as submit_result_router

import os


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="./templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@app.get("/", response_class=HTMLResponse)
async def top_page(request: Request):
    competition_links = [
        {"href": f"{compe}/overview", "name": compe}
        for compe in os.listdir("./competitions")
    ]
    return templates.TemplateResponse(
        "index.html", {"request": request, "competition_links": competition_links}
    )


app.include_router(overview_router, prefix="/{compe}")
app.include_router(data_router, prefix="/{compe}")
app.include_router(leaderboard_router, prefix="/{compe}")
app.include_router(mysub_router, prefix="/{compe}")
app.include_router(submit_router, prefix="/{compe}")
app.include_router(submit_result_router, prefix="/{compe}")
