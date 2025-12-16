from fastapi import FastAPI
from app.api.v1.users import router as users_router
from app.api.v1.question import router as question_router
from app.api.v1.auth import router as auth_router
from app.api.v1.answer import router as answers_router
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

app = FastAPI(title="Amanda Ferreira API", version="1.0.0")

origins = [
    "http://localhost",
    "http://localhost:4200",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CoopCoepMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
        response.headers["Cross-Origin-Embedder-Policy"] = "unsafe-none"
        return response


@app.get("/")
def root():
    return {"message": "API funcionando!"}

# Rotas agrupadas
app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(question_router, prefix="/api/v1", tags=["questions"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(answers_router, prefix="/api/v1", tags=["answer"])
