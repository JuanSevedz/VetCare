-- ============================================================
-- VetCare
-- Sprint 1 - Paso 6
-- Datos de prueba
-- ============================================================

-- ============================================================
-- 1. USUARIOS
-- ============================================================

INSERT INTO usuarios (
    id,
    nombre,
    correo,
    contrasena,
    telefono
)
VALUES
(
    'USR001',
    'Carlos Rodríguez',
    'carlos.rodriguez@vetcare.test',
    'hash_demo_001',
    '3001234567'
),
(
    'USR002',
    'Laura Martínez',
    'laura.martinez@vetcare.test',
    'hash_demo_002',
    '3017654321'
),
(
    'USR003',
    'Ana Gómez',
    'ana.gomez@vetcare.test',
    'hash_demo_003',
    '3109876543'
);

-- ============================================================
-- 2. PROPIETARIOS
-- ============================================================

INSERT INTO propietarios (
    id_usuario,
    direccion
)
VALUES
(
    'USR001',
    'Calle 45 # 12-30, Bogotá'
),
(
    'USR003',
    'Carrera 18 # 72-15, Bogotá'
);

-- ============================================================
-- 3. PERSONAL VETERINARIO
-- ============================================================

INSERT INTO personal_veterinario (
    id_usuario,
    especialidad,
    numero_licencia
)
VALUES
(
    'USR002',
    'Medicina veterinaria general',
    'LIC-VET-001'
);

-- ============================================================
-- 4. MASCOTAS
-- ============================================================

INSERT INTO mascotas (
    id,
    id_propietario,
    nombre,
    especie,
    raza,
    sexo,
    fecha_nacimiento,
    peso,
    microchip
)
VALUES
(
    'PET001',
    'USR001',
    'Max',
    'Perro',
    'Golden Retriever',
    'Macho',
    '2021-05-15',
    28.5,
    '985141000001234'
),
(
    'PET002',
    'USR003',
    'Luna',
    'Gato',
    'Siamés',
    'Hembra',
    '2022-08-20',
    4.2,
    NULL
);

-- ============================================================
-- 5. ALERGIAS
-- ============================================================

INSERT INTO alergias_mascota (
    id,
    id_mascota,
    alergia
)
VALUES
(
    'ALG001',
    'PET001',
    'Polen'
);

-- ============================================================
-- 6. CONDICIONES
-- ============================================================

INSERT INTO condiciones_mascota (
    id,
    id_mascota,
    condicion
)
VALUES
(
    'CON001',
    'PET001',
    'Dermatitis alérgica'
);

-- ============================================================
-- 7. HISTORIAS CLÍNICAS
-- ============================================================

INSERT INTO historias_clinicas (
    id,
    id_mascota,
    fecha_creacion
)
VALUES
(
    'HC001',
    'PET001',
    '2026-09-01'
),
(
    'HC002',
    'PET002',
    '2026-09-05'
);

-- ============================================================
-- 8. CITAS
-- ============================================================

INSERT INTO citas (
    id,
    id_mascota,
    id_veterinario,
    fecha,
    hora,
    motivo,
    estado
)
VALUES
(
    'CIT001',
    'PET001',
    'USR002',
    '2026-09-20',
    '09:00',
    'Control general y revisión dermatológica',
    'Atendida'
),
(
    'CIT002',
    'PET002',
    'USR002',
    '2026-09-28',
    '15:30',
    'Vacunación anual',
    'Confirmada'
);

-- ============================================================
-- 9. CONSULTAS
-- ============================================================

INSERT INTO consultas (
    id,
    id_historia_clinica,
    id_veterinario,
    id_cita,
    fecha,
    motivo,
    diagnostico,
    tratamiento
)
VALUES
(
    'CONS001',
    'HC001',
    'USR002',
    'CIT001',
    '2026-09-20',
    'Control general y revisión dermatológica',
    'Dermatitis alérgica leve',
    'Tratamiento tópico y control en 15 días'
);

-- ============================================================
-- 10. SÍNTOMAS
-- ============================================================

INSERT INTO sintomas_consulta (
    id,
    id_consulta,
    sintoma
)
VALUES
(
    'SINT001',
    'CONS001',
    'Enrojecimiento de la piel'
),
(
    'SINT002',
    'CONS001',
    'Rascado frecuente'
);

-- ============================================================
-- 11. OBSERVACIONES
-- ============================================================

INSERT INTO observaciones_consulta (
    id,
    id_consulta,
    observacion
)
VALUES
(
    'OBS001',
    'CONS001',
    'La mascota presenta buen estado general y apetito normal'
),
(
    'OBS002',
    'CONS001',
    'Se recomienda seguimiento dermatológico'
);

-- ============================================================
-- 12. MEDICAMENTOS FORMULADOS
-- ============================================================

INSERT INTO medicamentos_formulados (
    id,
    id_consulta,
    nombre,
    dosis,
    frecuencia,
    duracion,
    fecha_inicio,
    fecha_fin,
    estado
)
VALUES
(
    'MED001',
    'CONS001',
    'Crema dermatológica veterinaria',
    'Aplicación tópica',
    '2 veces al día',
    '15 días',
    '2026-09-20',
    '2026-10-05',
    'Activo'
);

-- ============================================================
-- 13. VACUNAS
-- ============================================================

INSERT INTO vacunas (
    id,
    id_mascota,
    id_veterinario,
    nombre,
    fecha_aplicacion,
    fecha_proxima,
    lote,
    estado
)
VALUES
(
    'VAC001',
    'PET001',
    'USR002',
    'Vacuna antirrábica',
    '2026-09-20',
    '2027-09-20',
    'LOTE-RAB-2026-01',
    'Aplicada'
);

-- ============================================================
-- 14. RECORDATORIOS
-- ============================================================

INSERT INTO recordatorios (
    id,
    id_mascota,
    categoria,
    fecha,
    descripcion,
    estado
)
VALUES
(
    'REC001',
    'PET001',
    'Vacunación',
    '2027-09-20',
    'Recordatorio de vacuna antirrábica',
    'Pendiente'
);

-- ============================================================
-- 15. GASTOS
-- ============================================================

INSERT INTO gastos (
    id,
    id_mascota,
    fecha,
    categoria,
    descripcion,
    valor
)
VALUES
(
    'GAS001',
    'PET001',
    '2026-09-20',
    'Consulta',
    'Consulta veterinaria general',
    85000
),
(
    'GAS002',
    'PET001',
    '2026-09-20',
    'Medicamentos',
    'Tratamiento dermatológico',
    45000
);

-- ============================================================
-- 16. CUIDADOS Y RUTINAS
-- ============================================================

INSERT INTO cuidados_rutina (
    id,
    id_mascota,
    tipo,
    frecuencia,
    horario,
    notas
)
VALUES
(
    'CUI001',
    'PET001',
    'Alimentación',
    '2 veces al día',
    '08:00 y 18:00',
    'Mantener horarios constantes'
),
(
    'CUI002',
    'PET001',
    'Ejercicio',
    'Diario',
    '17:00',
    'Caminata de aproximadamente 30 minutos'
);

-- ============================================================
-- 17. SOLICITUDES DE SEGUIMIENTO
-- ============================================================

INSERT INTO solicitudes_seguimiento (
    id,
    id_propietario,
    id_mascota,
    fecha,
    descripcion,
    estado
)
VALUES
(
    'SOL001',
    'USR001',
    'PET001',
    '2026-09-22',
    'Solicitar seguimiento de la evolución de la dermatitis',
    'Pendiente'
);