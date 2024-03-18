from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from jinja2 import FileSystemLoader
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database import get_db
from models import User, Post, Comment
from auth import get_current_user
from crud import insert_discussion, insert_comment
from markdown2 import markdown

router = APIRouter()
templates = Jinja2Templates(directory="templates/")
templates.env.loader = FileSystemLoader(["./templates"])


# helper function to read posts from database
def read_posts(db: Session):
    return (
        db.query(
            Post,
            User.display_name.label("user_name"),
            func.count(Comment.id).label("comment_count"),
        )
        .join(User, Post.user_id == User.id)
        .outerjoin(Comment, Post.id == Comment.post_id)
        .group_by(Post.id, User.display_name)
        .order_by(desc(Post.created_at))
        .all()
    )


@router.get("/discussion", response_class=HTMLResponse)
async def discussion_page(request: Request, db: Session = Depends(get_db)):
    # get posts from database
    posts = read_posts(db)
    return templates.TemplateResponse(
        "discussion.html",
        {
            "request": request,
            "macro_src": "macro.html",
            "posts": posts,
        },
    )


@router.get("/discussion/new", response_class=HTMLResponse)
async def discussion_new_page(request: Request, db: Session = Depends(get_db)):
    try:
        user = await get_current_user(request, db)
    except:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse(
        "discussion_new.html",
        {"request": request, "macro_src": "macro.html", "user": user},
    )


@router.get("/discussion/{post_id}", response_class=HTMLResponse)
async def discussion_post_page(
    request: Request, post_id: int, db: Session = Depends(get_db)
):
    # get post from database
    post = db.query(Post).filter(Post.id == post_id).first()

    post.content = markdown(post.content)

    return templates.TemplateResponse(
        "discussion_post.html",
        {"request": request, "macro_src": "macro.html", "post": post},
    )


@router.post("/new_discussion", response_class=HTMLResponse)
async def add_new_discussion(
    title: str = Form(),
    content: str = Form(),
    user_id: int = Form(),
):
    insert_discussion(user_id=user_id, title=title, content=content)
    return RedirectResponse(url="/discussion", status_code=302)


@router.post("/discussion/{post_id}/add-comment", response_class=HTMLResponse)
async def add_new_comment(
    post_id: int,
    user_id: int = Form(),
    content: str = Form(),
):
    insert_comment(
        content=content,
        user_id=user_id,
        post_id=post_id,
    )
    return RedirectResponse(url=f"/discussion/{post_id}", status_code=302)
