# 🐾 VetCare

> Proyecto de Ingeniería de Software — desarrollo incremental mediante entregas parciales.

## 📌 Descripción

**VetCare** es un proyecto de software orientado a la gestión de los procesos de una clínica veterinaria. El sistema busca organizar y digitalizar la información y las operaciones principales relacionadas con pacientes veterinarios, propietarios, personal, citas y demás procesos definidos durante el desarrollo del proyecto.

Este repositorio documenta la evolución del proyecto mediante entregas parciales, incorporando progresivamente artefactos de análisis, diseño, modelado, prototipado e implementación.

## 🎯 Objetivo del proyecto

Diseñar y desarrollar una solución de software para apoyar la gestión de los procesos de una clínica veterinaria, aplicando principios, técnicas y artefactos propios de la Ingeniería de Software.

El desarrollo se realizará de forma incremental, manteniendo la trazabilidad entre requisitos, análisis, diseño, implementación y pruebas.

## 🏗️ Estado actual

**Fase:** Implementación incremental del backend.  
**Rama:** `EntregasParciales`

El proyecto cuenta con una base de datos PostgreSQL estructurada, una API desarrollada con FastAPI y una arquitectura organizada por capas.

### Módulos implementados

| Módulo | Funcionalidades | Estado |
|---|---|---|
| Autenticación | Inicio de sesión, generación y validación de tokens JWT | ✅ Implementado |
| Usuarios | Registro de propietarios, consulta de perfiles y control de acceso por roles | ✅ Implementado |
| Mascotas | Registro, consulta, actualización y eliminación de mascotas | ✅ Implementado |
| Citas | Agendamiento, consulta, modificación, cancelación y validación de horarios | ✅ Implementado |
| Pruebas | Pruebas unitarias y de integración | ✅ 13 aprobadas |

### Reglas de negocio implementadas para las citas

- Las citas deben programarse de lunes a sábado.
- El horario de atención es de 08:00 a 18:00.
- Las citas se programan en intervalos de 30 minutos.
- No se permiten fechas anteriores al día actual.
- Una mascota no puede tener dos citas activas en la misma fecha y hora.
- Un veterinario no puede atender dos citas activas en la misma fecha y hora.
- Las citas canceladas no bloquean la disponibilidad.
- Se controlan las transiciones permitidas entre estados: `Pendiente`, `Confirmada`, `Atendida` y `Cancelada`.

### Funcionalidades pendientes

- Gestión de historias clínicas y consultas.
- Registro y seguimiento de vacunas.
- Gestión de medicamentos y tratamientos.
- Recordatorios.
- Gastos y cuidados de mascotas.
- Solicitudes de seguimiento.
- Integración del frontend con la API.

### Artefactos disponibles

| Artefacto | Ubicación | Estado |
|---|---|---|
| Consulta sobre metodologías ágiles | [`ConsultaMetodologiasAgiles/`](./ConsultaMetodologiasAgiles/) | ✅ Disponible |
| Diagramas de contexto | [`docs/DiagramContexto/`](./docs/DiagramContexto/) | ✅ Disponible |
| Diagramas de casos de uso | [`docs/DiagramasCasosDeUso/`](./docs/DiagramasCasosDeUso/) | ✅ Disponible |
| Diagramas de secuencia | [`docs/Secuencia/`](./docs/Secuencia/) | ✅ Disponible |
| Diagramas de flujo | [`docs/DiagramasDeFlujo/`](./docs/DiagramasDeFlujo/) | ✅ Disponible |
| Diagrama de clases | [`docs/ClassDiagram/`](./docs/ClassDiagram/) | ✅ Disponible |
| Modelos de base de datos | [`docs/DB/`](./docs/DB/) | ✅ Disponible |
| Documento consolidado | [`docs/VetCare.pdf`](./docs/VetCare.pdf) | ✅ Disponible |
| Prototipo | [`Proto/vetcare.html`](./Proto/vetcare.html) | ✅ Disponible |

## 🧩 Artefactos de Ingeniería de Software

El proyecto contempla los siguientes artefactos:

- Requerimientos funcionales y no funcionales.
- Historias de usuario y especificación de casos de uso.
- Diagramas de contexto.
- Diagramas de casos de uso.
- Diagramas de secuencia.
- Diagramas de flujo.
- Diagrama de clases.
- Modelos de base de datos.
- Arquitectura y diseño del sistema.
- Prototipos e interfaces.
- Implementación.
- Pruebas y evidencias de validación.
- Documentación técnica y de usuario.

## 🏛️ Arquitectura de desarrollo

El backend utiliza una arquitectura por capas para separar responsabilidades y facilitar el mantenimiento y evolución del sistema.

### Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.11 | Lenguaje de programación |
| FastAPI | Framework para construcción de API REST |
| SQLAlchemy | Acceso y persistencia de datos |
| PostgreSQL 16 | Sistema gestor de bases de datos |
| Pydantic | Validación y estructuración de datos |
| JWT | Autenticación basada en tokens |
| Pytest | Pruebas automatizadas |

### Organización del backend

```text
app/
├── core/
│   ├── auth.py
│   ├── config.py
│   ├── exceptions.py
│   └── security.py
├── database/
│   ├── base.py
│   └── connection.py
├── models/
│   ├── cita.py
│   ├── mascota.py
│   └── usuario.py
├── repositories/
│   ├── cita_repository.py
│   ├── mascota_repository.py
│   └── usuario_repository.py
├── routers/
│   ├── auth.py
│   ├── citas.py
│   ├── mascotas.py
│   └── usuarios.py
├── schemas/
│   ├── auth.py
│   ├── cita.py
│   ├── mascota.py
│   └── usuario.py
├── services/
│   ├── auth_service.py
│   ├── cita_service.py
│   ├── mascota_service.py
│   └── usuario_service.py
└── main.py
```

### Responsabilidad de las capas

- **Core:** seguridad, autenticación, configuración y manejo de excepciones.
- **Database:** conexión y sesiones con PostgreSQL.
- **Models:** representación de las entidades del sistema.
- **Repositories:** operaciones de acceso y persistencia de datos.
- **Schemas:** validación de entradas y estructuración de respuestas.
- **Services:** implementación de reglas de negocio y procesamiento.
- **Routers:** exposición de endpoints HTTP.

### Flujo de comunicación

```text
Cliente HTTP
     │
     ▼
   Router
     │
     ▼
   Service
     │
     ▼
 Repository
     │
     ▼
 PostgreSQL
```

La autenticación utiliza tokens JWT y el control de acceso se realiza mediante roles:

- `ADMIN`
- `VETERINARIO`
- `PROPIETARIO`

## 🗄️ Base de datos

El sistema utiliza PostgreSQL como motor de base de datos relacional.

El modelo contempla 17 tablas:

1. `usuarios`
2. `propietarios`
3. `personal_veterinario`
4. `mascotas`
5. `alergias_mascota`
6. `condiciones_mascota`
7. `historias_clinicas`
8. `citas`
9. `consultas`
10. `sintomas_consulta`
11. `observaciones_consulta`
12. `medicamentos_formulados`
13. `vacunas`
14. `recordatorios`
15. `gastos`
16. `cuidados_rutina`
17. `solicitudes_seguimiento`

### Scripts de base de datos

Los scripts SQL se encuentran en `database/`:

| Archivo | Descripción |
|---|---|
| `01_create_database.sql` | Creación de la base de datos |
| `02_create_tables.sql` | Creación de tablas |
| `03_constraints.sql` | Claves primarias y foráneas |
| `04_constraints_integrity.sql` | Restricciones de integridad |
| `05_indexes.sql` | Índices de optimización y restricciones de unicidad |
| `06_test_data.sql` | Datos de prueba |
| `07_validation_queries.sql` | Consultas de validación |

Los scripts deben ejecutarse respetando su orden y teniendo en cuenta que el primero crea la base de datos.

## 🔄 Metodología y estrategia de desarrollo

El desarrollo seguirá un enfoque ágil e incremental, organizado en sprints.

Cada sprint debe producir un incremento verificable del sistema y mantener la trazabilidad:

```text
Requisito
    ↓
Historia de usuario / Caso de uso
    ↓
Modelo de diseño
    ↓
Implementación
    ↓
Prueba
    ↓
Incremento funcional
```

La intención no es desarrollar todo el backend y después todo el frontend de forma aislada, sino construir módulos funcionales completos de manera progresiva.

## 📅 Cronograma de desarrollo

El siguiente cronograma parte del estado actual del proyecto: documentación, UML, arquitectura, modelo de base de datos y prototipo ya desarrollados.

> Las semanas representan bloques de trabajo o sprints y podrán convertirse posteriormente en fechas concretas según el calendario académico y la disponibilidad del equipo.

| Sprint | Bloque | Objetivo | Actividades principales | Entregable |
|---|---|---|---|---|
| **Sprint 0** | Preparación técnica | Preparar el entorno de desarrollo | Repositorio, estructura de proyecto, Git, convenciones, tecnologías y variables de entorno | Proyecto configurado |
| **Sprint 1** | Base de datos | Convertir el modelo diseñado en una BD funcional | Crear esquema PostgreSQL, tablas, PK/FK, restricciones, datos iniciales y pruebas SQL | BD funcional |
| **Sprint 2** | Backend / API | Exponer la lógica del sistema mediante servicios | Estructura por capas, entidades, repositorios, servicios, routers y endpoints iniciales | API funcional |
| **Sprint 3** | Autenticación + mascotas | Construir el primer incremento funcional | Login, roles, usuarios, propietarios, registro de mascotas y consulta del perfil | MVP 1: usuario + mascotas |
| **Sprint 4** | Citas + historia clínica | Implementar el núcleo clínico | Agendamiento, gestión de citas, pacientes, consultas e historia clínica | MVP 2: atención clínica |
| **Sprint 5** | Salud preventiva | Implementar seguimiento de salud | Vacunas, medicamentos, tratamientos y recordatorios | MVP 3: seguimiento de salud |
| **Sprint 6** | Funcionalidades complementarias | Completar funcionalidades secundarias del prototipo | Gastos, cuidados/rutinas, solicitudes y orientación ante síntomas | MVP 4: funcionalidades complementarias |
| **Sprint 7** | Integración y pruebas | Validar VetCare como sistema integrado | Integración frontend-backend-BD, pruebas funcionales, integración, corrección de errores y validación de requisitos | Versión integrada |
| **Sprint 8** | Cierre y entrega | Preparar la versión final | Documentación técnica, documentación de usuario, evidencias, despliegue y presentación | Versión final |

### 🧭 Orden técnico de implementación

```text
1. Cierre del modelo de BD
        ↓
2. Implementación PostgreSQL
        ↓
3. Backend / API
        ↓
4. Integración BD ↔ Backend
        ↓
5. Frontend basado en el prototipo
        ↓
6. Integración Frontend ↔ Backend
        ↓
7. Pruebas
        ↓
8. Correcciones y despliegue
```

### 🔗 Incrementos funcionales

Cada sprint funcional deberá cerrar un flujo completo.

#### Incremento 1 — Usuarios y mascotas

```text
Propietario
    ↓
Autenticación
    ↓
Mascotas
    ↓
Registro / consulta / edición
```

#### Incremento 2 — Atención clínica

```text
Mascota
    ↓
Cita
    ↓
Veterinario
    ↓
Consulta
    ↓
Historia clínica
```

#### Incremento 3 — Seguimiento de salud

```text
Mascota
 ├── Vacunas
 ├── Medicamentos
 ├── Tratamientos
 └── Recordatorios
```

#### Incremento 4 — Gestión complementaria

```text
Mascota
 ├── Gastos
 ├── Cuidados / rutinas
 ├── Solicitudes
 └── Orientación
```

## 🚀 Ejecución del backend

### Requisitos

- Python 3.11 o superior.
- PostgreSQL 16.
- Entorno virtual de Python.

### 1. Clonar el repositorio

```bash
git clone https://github.com/JuanSevedz/VetCare.git
cd VetCare
```

Cambiar a la rama de desarrollo:

```bash
git checkout EntregasParciales
```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql+psycopg://usuario@localhost:5432/vetcare
JWT_SECRET_KEY=clave_secreta
```

Reemplazar los valores de ejemplo por las credenciales correspondientes al entorno local.

El archivo `.env` no debe subirse al repositorio.

### 5. Preparar la base de datos

Crear la base de datos PostgreSQL y ejecutar los scripts SQL ubicados en `database/`, respetando el orden establecido.

### 6. Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

### 7. Acceder a la documentación interactiva

Una vez iniciado el servidor:

| Recurso | Dirección |
|---|---|
| Swagger UI | `http://127.0.0.1:8000/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` |
| Health check | `http://127.0.0.1:8000/health` |
| Health check de BD | `http://127.0.0.1:8000/health/db` |

## 🔌 Endpoints implementados

La API expone actualmente los siguientes grupos de endpoints:

### Autenticación

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/auth/login` | Autenticación de usuarios y generación de token JWT |

### Usuarios

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/usuarios/` | Registro de propietario |
| GET | `/usuarios/me` | Consulta del perfil autenticado |
| GET | `/usuarios/` | Listado de usuarios (ADMIN) |
| GET | `/usuarios/{usuario_id}` | Consulta de usuario propio o por ADMIN |

### Mascotas

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/mascotas/` | Listar mascotas según permisos |
| GET | `/mascotas/{mascota_id}` | Consultar mascota |
| POST | `/mascotas/` | Registrar mascota |
| PUT | `/mascotas/{mascota_id}` | Actualizar mascota |
| DELETE | `/mascotas/{mascota_id}` | Eliminar mascota |

### Citas

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/citas/` | Listar citas según rol |
| GET | `/citas/{cita_id}` | Consultar cita |
| POST | `/citas/` | Registrar cita |
| PATCH | `/citas/{cita_id}` | Modificar cita |

Los permisos y restricciones de cada operación se validan en el backend. Para consultar los esquemas de entrada, respuestas y códigos HTTP, utilizar Swagger UI.

## 🧪 Estrategia de pruebas

Las pruebas se realizan progresivamente y no únicamente al final.

Se contemplan:

- Pruebas unitarias de reglas de negocio.
- Pruebas de integración entre capas.
- Validación de persistencia en PostgreSQL.
- Pruebas de endpoints del backend.
- Pruebas de autorización y control de acceso.
- Validación de flujos completos.
- Corrección y regresión de errores.

### Pruebas automatizadas actuales

El proyecto utiliza **Pytest**.

Las pruebas están organizadas en:

```text
tests/
├── conftest.py
├── test_api.py
└── test_citas.py
```

Actualmente se cuenta con **13 pruebas aprobadas**:

| Archivo | Tipo | Pruebas |
|---|---|---:|
| `test_citas.py` | Unitarias | 6 |
| `test_api.py` | Integración | 7 |
| **Total** | | **13** |

Para ejecutarlas:

```bash
PYTHONPATH=. pytest -v
```

Las pruebas de integración utilizan una base de datos independiente denominada `vetcare_test`, evitando modificar los datos de desarrollo.

Antes de ejecutar las pruebas, configurar la variable de entorno `TEST_DATABASE_URL` para apuntar a dicha base de datos.

## ✅ Criterio de finalización de cada sprint

Un sprint se considerará cerrado cuando:

1. La funcionalidad esté implementada.
2. Esté integrada con las capas correspondientes.
3. Existan pruebas o evidencias de funcionamiento.
4. Se verifique su correspondencia con los requisitos y UML.
5. Los cambios relevantes queden registrados en GitHub.

## 📁 Estructura del repositorio

```text
VetCare/
│
├── ConsultaMetodologiasAgiles/
│
├── Proto/
│   └── vetcare.html
│
├── docs/
│   ├── ClassDiagram/
│   ├── DB/
│   ├── DiagramContexto/
│   ├── DiagramasCasosDeUso/
│   ├── DiagramasDeFlujo/
│   ├── Secuencia/
│   └── VetCare.pdf
│
├── database/
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   ├── 03_constraints.sql
│   ├── 04_constraints_integrity.sql
│   ├── 05_indexes.sql
│   ├── 06_test_data.sql
│   └── 07_validation_queries.sql
│
├── app/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_citas.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

La estructura se actualizará conforme se incorporen nuevos componentes de implementación, pruebas y documentación.

## 👥 Equipo de trabajo

| Integrante | Código |
|---|---|
| **Dania Lizeth Guzmán Triviño** | `20221020061` |
| **Juan Sebastián Vega Díaz** | `20231020087` |
| **Johan Felipe Pinzon Garcia** | `20222020176` |

## 📌 Convención para futuras entregas

Cada nueva entrega deberá actualizar, como mínimo:

1. El estado actual del proyecto.
2. El cronograma cuando cambie la planificación.
3. Los artefactos disponibles.
4. La estructura del repositorio, cuando cambie.
5. La documentación asociada a los nuevos componentes.
6. Las evidencias de pruebas del incremento correspondiente.

## 📄 Documentación

La documentación consolidada disponible actualmente se encuentra en [`docs/VetCare.pdf`](./docs/VetCare.pdf).

Este README es un documento vivo. Su propósito es servir como punto central de documentación del proyecto y será actualizado en cada entrega parcial.