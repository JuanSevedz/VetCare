# 🐾 VetCare

> Proyecto de Ingeniería de Software — desarrollo incremental mediante entregas parciales.

## 📌 Descripción

**VetCare** es un proyecto de software orientado a la gestión de los procesos de una clínica veterinaria. El sistema busca organizar y digitalizar la información y las operaciones principales relacionadas con pacientes veterinarios, propietarios, personal, citas y demás procesos definidos durante el desarrollo del proyecto.

Este repositorio documenta la evolución del proyecto mediante **entregas parciales**, incorporando progresivamente artefactos de análisis, diseño, modelado, prototipado e implementación.

## 🎯 Objetivo del proyecto

Diseñar y desarrollar una solución de software para apoyar la gestión de los procesos de una clínica veterinaria, aplicando principios, técnicas y artefactos propios de la **Ingeniería de Software**.

El desarrollo se realizará de forma incremental, manteniendo la trazabilidad entre requisitos, análisis, diseño, implementación y pruebas.

## 🏗️ Estado actual

**Fase:** Transición de análisis y diseño hacia implementación incremental  
**Rama:** `EntregasParciales`

El repositorio organiza la documentación y los artefactos de ingeniería en `docs/`, mientras que el prototipo se encuentra en `Proto/`.

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

- Requerimientos funcionales y no funcionales.
- Historias de usuario y/o especificación de casos de uso.
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

La implementación seguirá una arquitectura por capas, manteniendo separación de responsabilidades:

```text
Frontend
   │
   │ HTTP / JSON
   ▼
Backend / API
   │
   ├── Controllers
   ├── Services
   ├── Security
   └── Repositories
   │
   ▼
PostgreSQL
```

El prototipo existente se utilizará como referencia para la construcción del frontend real. La implementación progresará desde la base de datos hacia la API y posteriormente hacia la integración de las interfaces con los servicios.

## 🔄 Metodología y estrategia de desarrollo

El desarrollo seguirá un **enfoque ágil e incremental**, organizado en sprints.

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

La intención no es desarrollar todo el backend y después todo el frontend de forma aislada, sino construir **módulos funcionales completos de manera progresiva**.

## 📅 Cronograma de desarrollo

El siguiente cronograma parte del estado actual del proyecto: documentación, UML, arquitectura, modelo de base de datos y prototipo ya desarrollados.

> **Nota:** las semanas representan bloques de trabajo/sprints y podrán convertirse posteriormente en fechas concretas según el calendario académico y la disponibilidad del equipo.

| Sprint | Bloque | Objetivo | Actividades principales | Entregable |
|---|---|---|---|---|
| **Sprint 0** | Preparación técnica | Preparar el entorno de desarrollo | Repositorio, estructura de proyecto, Git, convenciones, tecnologías, variables de entorno | Proyecto configurado |
| **Sprint 1** | Base de datos | Convertir el modelo diseñado en una BD funcional | Crear esquema PostgreSQL, tablas, PK/FK, restricciones, datos iniciales y pruebas SQL | BD funcional |
| **Sprint 2** | Backend / API | Exponer la lógica del sistema mediante servicios | Estructura por capas, entidades, repositorios, servicios, controladores y endpoints iniciales | API funcional |
| **Sprint 3** | Autenticación + mascotas | Construir el primer incremento funcional | Login, roles, usuarios, propietarios, registro de mascotas y consulta del perfil | MVP 1: usuario + mascotas |
| **Sprint 4** | Citas + historia clínica | Implementar el núcleo clínico | Agendamiento, gestión de citas, pacientes, consultas e historia clínica | MVP 2: atención clínica |
| **Sprint 5** | Salud preventiva | Implementar seguimiento de salud | Vacunas, medicamentos, tratamientos y recordatorios | MVP 3: seguimiento de salud |
| **Sprint 6** | Funcionalidades complementarias | Completar funcionalidades secundarias del prototipo | Gastos, cuidados/rutinas, estado de solicitudes y orientación ante síntomas | MVP 4: funcionalidades complementarias |
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

## ✅ Criterio de finalización de cada sprint

Un sprint se considerará cerrado cuando:

1. La funcionalidad esté implementada.
2. Esté integrada con las capas correspondientes.
3. Existan pruebas o evidencias de funcionamiento.
4. Se verifique su correspondencia con los requisitos y UML.
5. Los cambios relevantes queden registrados en GitHub.

## 🧪 Estrategia de pruebas

Las pruebas se realizarán progresivamente y no únicamente al final.

Se contemplan:

- Pruebas de funcionalidades individuales.
- Pruebas de integración entre capas.
- Validación de persistencia en PostgreSQL.
- Pruebas de endpoints del backend.
- Pruebas de interfaz.
- Validación de flujos completos.
- Corrección y regresión de errores.

## 📁 Estructura actual del repositorio

```text
VetCare/
├── ConsultaMetodologiasAgiles/
│   └── ConsultaMetodologiasAgiles.pdf
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

1. El **estado actual** del proyecto.
2. El **cronograma** cuando cambie la planificación.
3. Los **artefactos disponibles**.
4. La **estructura del repositorio**, cuando cambie.
5. La documentación asociada a los nuevos componentes.
6. Las evidencias de pruebas del incremento correspondiente.

## 📄 Documentación

La documentación consolidada disponible actualmente se encuentra en [`docs/VetCare.pdf`](./docs/VetCare.pdf).

> **Nota:** Este README es un documento vivo. Su propósito es servir como punto central de documentación del proyecto y será actualizado en cada entrega parcial.
