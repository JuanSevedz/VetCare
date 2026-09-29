-- ============================================================
-- VetCare
-- Sprint 1 - Paso 4
-- Restricciones de integridad
-- ============================================================

-- ============================================================
-- 1. CAMPOS OBLIGATORIOS
-- ============================================================

ALTER TABLE usuarios
    ALTER COLUMN nombre SET NOT NULL,
    ALTER COLUMN correo SET NOT NULL,
    ALTER COLUMN contrasena SET NOT NULL;

ALTER TABLE propietarios
    ALTER COLUMN id_usuario SET NOT NULL;

ALTER TABLE personal_veterinario
    ALTER COLUMN id_usuario SET NOT NULL,
    ALTER COLUMN especialidad SET NOT NULL,
    ALTER COLUMN numero_licencia SET NOT NULL;

ALTER TABLE mascotas
    ALTER COLUMN id_propietario SET NOT NULL,
    ALTER COLUMN nombre SET NOT NULL,
    ALTER COLUMN especie SET NOT NULL;

ALTER TABLE alergias_mascota
    ALTER COLUMN id_mascota SET NOT NULL,
    ALTER COLUMN alergia SET NOT NULL;

ALTER TABLE condiciones_mascota
    ALTER COLUMN id_mascota SET NOT NULL,
    ALTER COLUMN condicion SET NOT NULL;

ALTER TABLE historias_clinicas
    ALTER COLUMN id_mascota SET NOT NULL,
    ALTER COLUMN fecha_creacion SET NOT NULL;

ALTER TABLE citas
    ALTER COLUMN id_mascota SET NOT NULL,
    ALTER COLUMN id_veterinario SET NOT NULL,
    ALTER COLUMN fecha SET NOT NULL,
    ALTER COLUMN hora SET NOT NULL,
    ALTER COLUMN motivo SET NOT NULL,
    ALTER COLUMN estado SET NOT NULL;

ALTER TABLE consultas
    ALTER COLUMN id_historia_clinica SET NOT NULL,
    ALTER COLUMN id_veterinario SET NOT NULL,
    ALTER COLUMN id_cita SET NOT NULL,
    ALTER COLUMN fecha SET NOT NULL,
    ALTER COLUMN motivo SET NOT NULL,
    ALTER COLUMN diagnostico SET NOT NULL,
    ALTER COLUMN tratamiento SET NOT NULL;

ALTER TABLE sintomas_consulta
    ALTER COLUMN id_consulta SET NOT NULL,
    ALTER COLUMN sintoma SET NOT NULL;

ALTER TABLE observaciones_consulta
    ALTER COLUMN id_consulta SET NOT NULL,
    ALTER COLUMN observacion SET NOT NULL;

ALTER TABLE medicamentos_formulados
    ALTER COLUMN id_consulta SET NOT NULL,
    ALTER COLUMN nombre SET NOT NULL,
    ALTER COLUMN dosis SET NOT NULL,
    ALTER COLUMN frecuencia SET NOT NULL,
    ALTER COLUMN duracion SET NOT NULL,
    ALTER COLUMN fecha_inicio SET NOT NULL,
    ALTER COLUMN fecha_fin SET NOT NULL,
    ALTER COLUMN estado SET NOT NULL;

ALTER TABLE vacunas
    ALTER COLUMN id_mascota SET NOT NULL,
    ALTER COLUMN id_veterinario SET NOT NULL,
    ALTER COLUMN nombre SET NOT NULL,
    ALTER COLUMN fecha_aplicacion SET NOT NULL,
    ALTER COLUMN estado SET NOT NULL;

ALTER TABLE recordatorios
    ALTER COLUMN id_mascota SET NOT NULL,
    ALTER COLUMN categoria SET NOT NULL,
    ALTER COLUMN fecha SET NOT NULL,
    ALTER COLUMN descripcion SET NOT NULL,
    ALTER COLUMN estado SET NOT NULL;

ALTER TABLE gastos
    ALTER COLUMN id_mascota SET NOT NULL,
    ALTER COLUMN fecha SET NOT NULL,
    ALTER COLUMN categoria SET NOT NULL,
    ALTER COLUMN descripcion SET NOT NULL,
    ALTER COLUMN valor SET NOT NULL;

ALTER TABLE cuidados_rutina
    ALTER COLUMN id_mascota SET NOT NULL,
    ALTER COLUMN tipo SET NOT NULL,
    ALTER COLUMN frecuencia SET NOT NULL;

ALTER TABLE solicitudes_seguimiento
    ALTER COLUMN id_propietario SET NOT NULL,
    ALTER COLUMN id_mascota SET NOT NULL,
    ALTER COLUMN fecha SET NOT NULL,
    ALTER COLUMN descripcion SET NOT NULL,
    ALTER COLUMN estado SET NOT NULL;

-- ============================================================
-- 2. RESTRICCIONES UNIQUE
-- ============================================================

ALTER TABLE usuarios
    ADD CONSTRAINT uq_usuarios_correo UNIQUE (correo);

ALTER TABLE personal_veterinario
    ADD CONSTRAINT uq_personal_veterinario_licencia
    UNIQUE (numero_licencia);

-- ============================================================
-- 3. RESTRICCIONES CHECK
-- ============================================================

ALTER TABLE mascotas
    ADD CONSTRAINT chk_mascotas_peso
    CHECK (peso IS NULL OR peso > 0);

ALTER TABLE mascotas
    ADD CONSTRAINT chk_mascotas_sexo
    CHECK (sexo IS NULL OR sexo IN ('Macho', 'Hembra'));

ALTER TABLE gastos
    ADD CONSTRAINT chk_gastos_valor
    CHECK (valor >= 0);

ALTER TABLE medicamentos_formulados
    ADD CONSTRAINT chk_medicamentos_fechas
    CHECK (
        fecha_fin IS NULL
        OR fecha_inicio IS NULL
        OR fecha_fin >= fecha_inicio
    );

ALTER TABLE citas
    ADD CONSTRAINT chk_citas_estado
    CHECK (
        estado IN ('Pendiente', 'Confirmada', 'Atendida', 'Cancelada')
    );

ALTER TABLE medicamentos_formulados
    ADD CONSTRAINT chk_medicamentos_estado
    CHECK (
        estado IN ('Activo', 'Finalizado', 'Suspendido')
    );

ALTER TABLE recordatorios
    ADD CONSTRAINT chk_recordatorios_estado
    CHECK (
        estado IN ('Pendiente', 'Completado', 'Cancelado')
    );

ALTER TABLE vacunas
    ADD CONSTRAINT chk_vacunas_estado
    CHECK (
        estado IN ('Aplicada', 'Pendiente')
    );

ALTER TABLE solicitudes_seguimiento
    ADD CONSTRAINT chk_solicitudes_estado
    CHECK (
        estado IN ('Pendiente', 'En proceso', 'Atendida', 'Cancelada')
    );
