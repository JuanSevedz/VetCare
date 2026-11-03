from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Importación de modelos para registrar sus tablas en Base.metadata
from app.models.usuario import Usuario
from app.models.mascota import Mascota
from app.models.cita import Cita
from app.models.historia_clinica import HistoriaClinica
from app.models.consulta import Consulta
from app.models.sintoma_consulta import SintomaConsulta
from app.models.observacion_consulta import ObservacionConsulta