from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import integrity_error_handler
from app.database.connection import engine

from app.routers.mascotas import router as mascotas_router
from app.routers.usuarios import router as usuarios_router
from app.routers.auth import router as auth_router
from app.routers.citas import router as citas_router

from app.routers.historias_clinicas import (
    router as historias_clinicas_router,
)

from app.routers.consultas import (
    router as consultas_router,
)
from app.routers.medicamentos import router as medicamentos_router
from app.routers.vacunas import router as vacunas_router
from app.routers.recordatorios import router as recordatorios_router
from app.routers.gastos import router as gastos_router


app = FastAPI(
    title="VetCare API",
    description="API para la gestión de una clínica veterinaria",
    version="1.0.0",
)


app.add_exception_handler(
    IntegrityError,
    integrity_error_handler,
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "VetCare API",
    }


@app.get("/health/db")
def database_health_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar()

    return {
        "status": "ok",
        "database": "vetcare",
        "query_result": value,
    }


app.include_router(mascotas_router)
app.include_router(usuarios_router)
app.include_router(auth_router)
app.include_router(citas_router)
app.include_router(historias_clinicas_router)
app.include_router(consultas_router)
app.include_router(medicamentos_router)
app.include_router(vacunas_router)
app.include_router(recordatorios_router)
app.include_router(gastos_router)