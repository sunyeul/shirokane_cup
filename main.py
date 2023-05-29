from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader

from routers import (
    login_router,
    competitions_router,
    overview_router,
    data_router,
    leaderboard_router,
    mysub_router,
    submit_router,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="./templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@app.get("/", response_class=HTMLResponse)
async def top_page(request: Request):
    return templates.TemplateResponse("top_page.html", {"request": request})


app.include_router(login_router)
app.include_router(competitions_router)
app.include_router(overview_router, prefix="/competitions/{compe}")
app.include_router(data_router, prefix="/competitions/{compe}")
app.include_router(leaderboard_router, prefix="/competitions/{compe}")
app.include_router(mysub_router, prefix="/competitions/{compe}")
app.include_router(submit_router, prefix="/competitions/{compe}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080, reload=False)
