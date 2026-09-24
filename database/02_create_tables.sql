-- ============================================================
-- VetCare
-- Sprint 1 - Paso 2
-- Creación de tablas
-- ============================================================

-- ============================================================
-- 1. USUARIOS
-- ============================================================

CREATE TABLE usuarios (
    id VARCHAR(50),
    nombre VARCHAR(100),
    correo VARCHAR(150),
    contrasena VARCHAR(255),
    telefono VARCHAR(30)
);


-- ============================================================
-- 2. PROPIETARIOS
-- ============================================================

CREATE TABLE propietarios (
    id_usuario VARCHAR(50),
    direccion VARCHAR(200)
);


-- ============================================================
-- 3. PERSONAL VETERINARIO
-- ============================================================

CREATE TABLE personal_veterinario (
    id_usuario VARCHAR(50),
    especialidad VARCHAR(100),
    numero_licencia VARCHAR(100)
);


-- ============================================================
-- 4. MASCOTAS
-- ============================================================

CREATE TABLE mascotas (
    id VARCHAR(50),
    id_propietario VARCHAR(50),
    nombre VARCHAR(100),
    especie VARCHAR(50),
    raza VARCHAR(100),
    sexo VARCHAR(30),
    fecha_nacimiento DATE,
    peso FLOAT,
    microchip VARCHAR(100)
);


-- ============================================================
-- 5. ALERGIAS DE MASCOTA
-- ============================================================

CREATE TABLE alergias_mascota (
    id VARCHAR(50),
    id_mascota VARCHAR(50),
    alergia VARCHAR(200)
);


-- ============================================================
-- 6. CONDICIONES DE MASCOTA
-- ============================================================

CREATE TABLE condiciones_mascota (
    id VARCHAR(50),
    id_mascota VARCHAR(50),
    condicion VARCHAR(200)
);


-- ============================================================
-- 7. HISTORIAS CLÍNICAS
-- ============================================================

CREATE TABLE historias_clinicas (
    id VARCHAR(50),
    id_mascota VARCHAR(50),
    fecha_creacion DATE
);


-- ============================================================
-- 8. CITAS
-- ============================================================

CREATE TABLE citas (
    id VARCHAR(50),
    id_mascota VARCHAR(50),
    id_veterinario VARCHAR(50),
    fecha DATE,
    hora VARCHAR(20),
    motivo VARCHAR(300),
    estado VARCHAR(50)
);


-- ============================================================
-- 9. CONSULTAS
-- ============================================================

CREATE TABLE consultas (
    id VARCHAR(50),
    id_historia_clinica VARCHAR(50),
    id_veterinario VARCHAR(50),
    id_cita VARCHAR(50),
    fecha DATE,
    motivo VARCHAR(300),
    diagnostico VARCHAR(500),
    tratamiento VARCHAR(500)
);


-- ============================================================
-- 10. SÍNTOMAS DE CONSULTA
-- ============================================================

CREATE TABLE sintomas_consulta (
    id VARCHAR(50),
    id_consulta VARCHAR(50),
    sintoma VARCHAR(200)
);


-- ============================================================
-- 11. OBSERVACIONES DE CONSULTA
-- ============================================================

CREATE TABLE observaciones_consulta (
    id VARCHAR(50),
    id_consulta VARCHAR(50),
    observacion VARCHAR(500)
);


-- ============================================================
-- 12. MEDICAMENTOS FORMULADOS
-- ============================================================

CREATE TABLE medicamentos_formulados (
    id VARCHAR(50),
    id_consulta VARCHAR(50),
    nombre VARCHAR(150),
    dosis VARCHAR(100),
    frecuencia VARCHAR(100),
    duracion VARCHAR(100),
    fecha_inicio DATE,
    fecha_fin DATE,
    estado VARCHAR(50)
);


-- ============================================================
-- 13. VACUNAS
-- ============================================================

CREATE TABLE vacunas (
    id VARCHAR(50),
    id_mascota VARCHAR(50),
    id_veterinario VARCHAR(50),
    nombre VARCHAR(150),
    fecha_aplicacion DATE,
    fecha_proxima DATE,
    lote VARCHAR(100),
    estado VARCHAR(50)
);


-- ============================================================
-- 14. RECORDATORIOS
-- ============================================================

CREATE TABLE recordatorios (
    id VARCHAR(50),
    id_mascota VARCHAR(50),
    categoria VARCHAR(100),
    fecha DATE,
    descripcion VARCHAR(300),
    estado VARCHAR(50)
);


-- ============================================================
-- 15. GASTOS
-- ============================================================

CREATE TABLE gastos (
    id VARCHAR(50),
    id_mascota VARCHAR(50),
    fecha DATE,
    categoria VARCHAR(100),
    descripcion VARCHAR(300),
    valor FLOAT
);


-- ============================================================
-- 16. CUIDADOS Y RUTINAS
-- ============================================================

CREATE TABLE cuidados_rutina (
    id VARCHAR(50),
    id_mascota VARCHAR(50),
    tipo VARCHAR(100),
    frecuencia VARCHAR(100),
    horario VARCHAR(50),
    notas VARCHAR(500)
);


-- ============================================================
-- 17. SOLICITUDES DE SEGUIMIENTO
-- ============================================================

CREATE TABLE solicitudes_seguimiento (
    id VARCHAR(50),
    id_propietario VARCHAR(50),
    id_mascota VARCHAR(50),
    fecha DATE,
    descripcion VARCHAR(500),
    estado VARCHAR(50)
);