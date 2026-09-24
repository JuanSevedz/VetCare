from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import integrity_error_handler
from app.database.connection import engine
from app.routers.mascotas import router as mascotas_router


app = FastAPI(
    title="VetCare API",
    description="API para la gestión de una clínica veterinaria",
    version="1.0.0"
)


app.add_exception_handler(
    IntegrityError,
    integrity_error_handler
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "VetCare API"
    }


@app.get("/health/db")
def database_health_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar()

    return {
        "status": "ok",
        "database": "vetcare",
        "query_result": value
    }


app.include_router(mascotas_router)