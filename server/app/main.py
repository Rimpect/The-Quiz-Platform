from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base
from app.routers import (
    users_router,
    quizzes_router,
    questions_router,
    answers_router,
    quiz_results_router,
    auth_router
)

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quiz API",
    description="API для системы квизов",
    version="1.0.0"
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статические файлы (для загрузок)
if not os.path.exists("static/uploads"):
    os.makedirs("static/uploads")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение роутеров
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(quizzes_router)
app.include_router(questions_router)
app.include_router(answers_router)
app.include_router(quiz_results_router)

@app.get("/")
def root():
    return {
        "message": "Quiz API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}