import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
 
from app.api.endpoints import planner, game, quiz
 
app = FastAPI(title="Finwise")
 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
 
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
 
 
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
 
 
app.include_router(planner.router, prefix="/api/planner", tags=["planner"])
app.include_router(game.router,    prefix="/api/game",    tags=["game"])
app.include_router(quiz.router,    prefix="/api/quiz",    tags=["quiz"])