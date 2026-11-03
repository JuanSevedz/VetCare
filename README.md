# 🐾 VetCare

> Proyecto de Ingeniería de Software — desarrollo incremental mediante entregas parciales.

## 📌 Descripción

**VetCare** es un proyecto de software orientado a la gestión de los procesos de una clínica veterinaria. El sistema busca organizar y digitalizar la información y las operaciones principales relacionadas con pacientes veterinarios, propietarios, personal, citas, atención clínica y seguimiento de la salud de las mascotas.

Este repositorio documenta la evolución del proyecto mediante entregas parciales, incorporando progresivamente artefactos de análisis, diseño, modelado, prototipado, implementación y pruebas.

## 🎯 Objetivo del proyecto

Diseñar y desarrollar una solución de software para apoyar la gestión de los procesos de una clínica veterinaria, aplicando principios, técnicas y artefactos propios de la Ingeniería de Software.

El desarrollo se realiza de forma incremental, manteniendo la trazabilidad entre requisitos, análisis, diseño, implementación y pruebas.

## 🏗️ Estado actual

**Fase:** Implementación y validación funcional del backend.  
**Rama de desarrollo:** `EntregasParciales`

VetCare cuenta con una API REST desarrollada con FastAPI, persistencia en PostgreSQL y una arquitectura organizada por capas. Se han implementado los principales módulos funcionales del backend y se han realizado pruebas unitarias y de integración.

### Módulos implementados

| Módulo | Funcionalidades | Estado |
|---|---|---|
| Autenticación | Inicio de sesión, generación y validación de tokens JWT | ✅ Implementado |
| Usuarios | Registro, consulta de perfiles y control de acceso según roles | ✅ Implementado |
| Mascotas | Registro, consulta, actualización y eliminación | ✅ Implementado |
| Citas | Agendamiento, consulta, modificación, cancelación y validación de disponibilidad | ✅ Implementado |
| Historias clínicas | Gestión de historias clínicas asociadas a las mascotas | ✅ Implementado |
| Consultas | Registro y gestión de consultas veterinarias | ✅ Implementado |
| Vacunas | Registro y seguimiento de vacunas | ✅ Implementado |
| Medicamentos | Formulación y seguimiento de medicamentos | ✅ Implementado |
| Recordatorios | Gestión de recordatorios asociados a las mascotas | ✅ Implementado |
| Gastos | Registro y consulta de gastos | ✅ Implementado |
| Cuidados y rutinas | Registro y gestión de cuidados de las mascotas | ✅ Implementado |
| Solicitudes de seguimiento | Registro y gestión de solicitudes | ✅ Implementado |

### Validación del backend

| Elemento | Resultado |
|---|---|
| Framework de pruebas | Pytest |
| Base de datos de pruebas | PostgreSQL (`vetcare_test`) |
| Pruebas aprobadas | 208 |
| Pruebas fallidas | 0 |
| Resultado de ejecución | ✅ 208/208 aprobadas |

### Reglas de negocio implementadas para las citas

- Las citas deben programarse de lunes a sábado.
- El horario de atención es de 08:00 a 18:00.
- Las citas se programan en intervalos de 30 minutos.
- No se permiten fechas anteriores al día actual.
- Una mascota no puede tener dos citas activas en la misma fecha y hora.
- Un veterinario no puede atender dos citas activas en la misma fecha y hora.
- Las citas canceladas no bloquean la disponibilidad.
- Se controlan las transiciones permitidas entre estados: `Pendiente`, `Confirmada`, `Atendida` y `Cancelada`.

### Actividades pendientes

- Integración del frontend con la API.
- Auditoría de instalación de la base de datos desde un entorno limpio.
- Verificación de correspondencia entre modelos SQLAlchemy y restricciones PostgreSQL.
- Revisión de seguridad y configuración del entorno.
- Documentación técnica y de usuario.
- Validación final e integración completa del sistema.

> **Nota:** La auditoría final de instalación, correspondencia de modelos y restricciones, y seguridad queda pendiente para su realización en otro entorno de desarrollo. Las 208 pruebas aprobadas corresponden a la última ejecución registrada del conjunto automatizado.

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
│   ├── ...
├── repositories/
│   ├── ...
├── routers/
│   ├── ...
├── schemas/
│   ├── ...
├── services/
│   ├── ...
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

### Integridad de los datos

La base de datos contempla diferentes mecanismos para mantener la consistencia de la información:

- Claves primarias y foráneas.
- Restricciones de obligatoriedad mediante `NOT NULL`.
- Restricciones de unicidad mediante `UNIQUE`.
- Validaciones de dominio mediante `CHECK`.
- Índices para optimizar consultas.
- Restricciones de integridad referencial entre mascotas, propietarios y solicitudes de seguimiento.

Se incorporaron validaciones para evitar registros inconsistentes, como valores de gastos no positivos, estados no permitidos y asociaciones incorrectas entre mascotas y propietarios.

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
| `08_clinical_constraints.sql` | Restricciones e índices relacionados con la integridad de los datos clínicos |

Los scripts deben ejecutarse respetando sus dependencias y el orden establecido. El primero crea la base de datos y los siguientes construyen progresivamente su estructura y restricciones.

> La ejecución completa de los scripts desde una instalación limpia queda pendiente de la auditoría final.

## 🔄 Metodología y estrategia de desarrollo

El desarrollo sigue un enfoque ágil e incremental, organizado en sprints.

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

El siguiente cronograma parte del estado del proyecto: documentación, UML, arquitectura, modelo de base de datos y prototipo desarrollados.

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

### Estado de avance

Los incrementos de implementación del backend contemplados en los sprints de autenticación, usuarios, mascotas, citas, atención clínica, seguimiento de salud y funcionalidades complementarias cuentan con desarrollo funcional y pruebas automatizadas.

La integración del frontend, la auditoría técnica final y el cierre general del proyecto permanecen pendientes.

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

El archivo `.env` no debe subirse al repositorio ni compartirse públicamente.

### 5. Preparar la base de datos

Crear la base de datos PostgreSQL y ejecutar los scripts SQL ubicados en `database/`, respetando sus dependencias y el orden establecido.

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

## 🔌 API REST y endpoints

La API REST de VetCare está desarrollada con FastAPI y organizada mediante routers, servicios, repositorios, modelos y esquemas de validación.

Los endpoints se encuentran agrupados en los siguientes módulos:

- Autenticación y usuarios.
- Mascotas.
- Citas.
- Historias clínicas.
- Consultas veterinarias.
- Vacunas.
- Medicamentos.
- Recordatorios.
- Gastos.
- Cuidados y rutinas.
- Solicitudes de seguimiento.

Las operaciones implementan validaciones de datos, reglas de negocio y controles de acceso según el rol del usuario.

Para consultar el listado actualizado de rutas, parámetros, esquemas de entrada, respuestas y códigos HTTP, se puede acceder a la documentación interactiva de FastAPI:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

## 🧪 Estrategia de pruebas

Las pruebas se realizan progresivamente durante el desarrollo para verificar el comportamiento de los módulos, la integración entre capas y la persistencia de la información.

Se contemplan:

- Pruebas unitarias de reglas de negocio.
- Pruebas de integración entre capas.
- Validación de persistencia en PostgreSQL.
- Pruebas de endpoints del backend.
- Pruebas de autorización y control de acceso.
- Validación de flujos funcionales.
- Pruebas de regresión.

### Pruebas automatizadas

El proyecto utiliza **Pytest** para ejecutar las pruebas automatizadas.

**Última ejecución registrada:**

| Resultado | Cantidad |
|---|---:|
| Pruebas aprobadas | 208 |
| Pruebas fallidas | 0 |
| Total | 208 |

**Resultado: 100 % de las pruebas ejecutadas fueron aprobadas.**

### Ejecución de las pruebas

Las pruebas de integración utilizan una base de datos independiente denominada `vetcare_test`, evitando modificar los datos de desarrollo.

Para ejecutarlas, activar el entorno virtual y ejecutar:

```bash
TEST_DATABASE_URL="postgresql+psycopg://usuario@localhost/vetcare_test" PYTHONPATH=. pytest -v
```

Se debe reemplazar `usuario` por el usuario local de PostgreSQL que tenga permisos sobre la base de datos de pruebas.

La configuración de `TEST_DATABASE_URL` se realiza para la ejecución del comando y no requiere modificar el archivo `.env` del proyecto.

> Los resultados corresponden a la última ejecución registrada. La auditoría de instalación limpia, correspondencia entre modelos y restricciones de base de datos, y revisión de seguridad quedan pendientes.

## ✅ Criterio de finalización de cada sprint

Un sprint se considerará cerrado cuando:

1. La funcionalidad esté implementada.
2. Esté integrada con las capas correspondientes.
3. Existan pruebas o evidencias de funcionamiento.
4. Se verifique su correspondencia con los requisitos y UML.
5. Los cambios relevantes queden registrados en GitHub.
6. Las pruebas automatizadas correspondientes al incremento se ejecuten satisfactoriamente.
7. La documentación del repositorio refleje los cambios implementados.

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
│   ├── 07_validation_queries.sql
│   └── 08_clinical_constraints.sql
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
│   └── ...
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