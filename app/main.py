from fastapi import FastAPI
from app.api.routes import router
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from app.core.logger import setup_logging

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup inicial
    setup_logging() #desenvolver logging
    print("Aplicação iniciada. Logging configurado.")
    # Aqui pode ir a inicialização do DB (init_db) se necessário
    yield
    # Ações de finalização
    print("Aplicação finalizada.")

app = FastAPI(
    title="Capitão IA",
    description="API para o Capitão IA",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Capitão IA"}

