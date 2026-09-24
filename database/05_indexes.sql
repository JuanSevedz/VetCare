-- ============================================================
-- VetCare
-- Sprint 1 - Paso 5
-- Índices
-- ============================================================

-- ============================================================
-- ÍNDICES SOBRE CLAVES FORÁNEAS
-- ============================================================

CREATE INDEX idx_mascotas_propietario
ON mascotas(id_propietario);

CREATE INDEX idx_alergias_mascota
ON alergias_mascota(id_mascota);

CREATE INDEX idx_condiciones_mascota
ON condiciones_mascota(id_mascota);

CREATE INDEX idx_historias_mascota
ON historias_clinicas(id_mascota);

CREATE INDEX idx_citas_mascota
ON citas(id_mascota);

CREATE INDEX idx_citas_veterinario
ON citas(id_veterinario);

CREATE INDEX idx_consultas_historia
ON consultas(id_historia_clinica);

CREATE INDEX idx_consultas_veterinario
ON consultas(id_veterinario);

CREATE INDEX idx_consultas_cita
ON consultas(id_cita);

CREATE INDEX idx_sintomas_consulta
ON sintomas_consulta(id_consulta);

CREATE INDEX idx_observaciones_consulta
ON observaciones_consulta(id_consulta);

CREATE INDEX idx_medicamentos_consulta
ON medicamentos_formulados(id_consulta);

CREATE INDEX idx_vacunas_mascota
ON vacunas(id_mascota);

CREATE INDEX idx_vacunas_veterinario
ON vacunas(id_veterinario);

CREATE INDEX idx_recordatorios_mascota
ON recordatorios(id_mascota);

CREATE INDEX idx_gastos_mascota
ON gastos(id_mascota);

CREATE INDEX idx_cuidados_mascota
ON cuidados_rutina(id_mascota);

CREATE INDEX idx_solicitudes_propietario
ON solicitudes_seguimiento(id_propietario);

CREATE INDEX idx_solicitudes_mascota
ON solicitudes_seguimiento(id_mascota);

-- Citas por fecha
CREATE INDEX idx_citas_fecha
ON citas(fecha);

-- Recordatorios por fecha
CREATE INDEX idx_recordatorios_fecha
ON recordatorios(fecha);

-- Gastos por fecha
CREATE INDEX idx_gastos_fecha
ON gastos(fecha);

-- Vacunas por fecha
CREATE INDEX idx_vacunas_fecha
ON vacunas(fecha_aplicacion);

-- Consultas por fecha
CREATE INDEX idx_consultas_fecha
ON consultas(fecha);