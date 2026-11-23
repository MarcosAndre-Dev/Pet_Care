import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, pets, tutores

app = FastAPI(title="PetCare API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000", "http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tutores.router)
app.include_router(pets.router)


@app.exception_handler(Exception)
async def erro_inesperado(request: Request, exc: Exception):
    logging.exception("Erro não tratado")
    return JSONResponse(status_code=500, content={"detail": "Erro interno do servidor"})