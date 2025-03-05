import random
import string
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.auth import get_current_user


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)


@app.get("/reports")
def get_reports(user: dict = Depends(get_current_user)):
    """
    Эмулирует генерацию отчета.
    """

    return {
        "user": user.get("preferred_username", "unknown"),
        "report_id": "".join(random.choices(string.ascii_uppercase + string.digits, k=8)),
        "description": "Fake usage report",
        "data": [random.randint(1, 100) for _ in range(10)],
    }
