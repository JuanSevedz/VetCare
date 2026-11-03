-- ============================================================
-- VetCare
-- Restricciones del módulo de historias clínicas y consultas
-- ============================================================


-- ============================================================
-- 1. UNA HISTORIA CLÍNICA POR MASCOTA
-- ============================================================

CREATE UNIQUE INDEX IF NOT EXISTS
    uq_historias_clinicas_mascota
ON historias_clinicas (id_mascota);


-- ============================================================
-- 2. UNA CONSULTA POR CITA
-- ============================================================

CREATE UNIQUE INDEX IF NOT EXISTS
    uq_consultas_cita
ON consultas (id_cita);


-- ============================================================
-- 3. VERIFICACIÓN
-- ============================================================

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename IN (
    'historias_clinicas',
    'consultas'
)
ORDER BY tablename, indexname;