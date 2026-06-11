from fastapi.middleware.cors import CORSMiddleware
import os
import json


def setup_cors_middleware(app) :
    """Настройка CORS middleware"""

    # Получаем разрешенные origins из .env
    cors_origins_str = os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://localhost:5173"]')
    cors_origins = json.loads(cors_origins_str)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time"]
    )

    return app