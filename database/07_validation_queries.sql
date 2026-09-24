-- ============================================================
-- VetCare
-- Sprint 1 - Paso 7
-- Consultas de validación
-- ============================================================


-- ============================================================
-- 1. USUARIOS Y PROPIETARIOS
-- ============================================================

SELECT
    u.id,
    u.nombre,
    u.correo,
    p.direccion
FROM usuarios u
INNER JOIN propietarios p
    ON u.id = p.id_usuario;


-- ============================================================
-- 2. MASCOTAS Y SUS PROPIETARIOS
-- ============================================================

SELECT
    m.id AS id_mascota,
    m.nombre AS mascota,
    m.especie,
    m.raza,
    m.sexo,
    m.peso,
    u.nombre AS propietario
FROM mascotas m
INNER JOIN propietarios p
    ON m.id_propietario = p.id_usuario
INNER JOIN usuarios u
    ON p.id_usuario = u.id;


-- ============================================================
-- 3. HISTORIAS CLÍNICAS DE LAS MASCOTAS
-- ============================================================

SELECT
    m.nombre AS mascota,
    hc.id AS historia_clinica,
    hc.fecha_creacion
FROM historias_clinicas hc
INNER JOIN mascotas m
    ON hc.id_mascota = m.id;


-- ============================================================
-- 4. CITAS CON MASCOTA Y VETERINARIO
-- ============================================================

SELECT
    c.id AS id_cita,
    m.nombre AS mascota,
    u.nombre AS veterinario,
    c.fecha,
    c.hora,
    c.motivo,
    c.estado
FROM citas c
INNER JOIN mascotas m
    ON c.id_mascota = m.id
INNER JOIN personal_veterinario pv
    ON c.id_veterinario = pv.id_usuario
INNER JOIN usuarios u
    ON pv.id_usuario = u.id;


-- ============================================================
-- 5. CONSULTAS CLÍNICAS COMPLETAS
-- ============================================================

SELECT
    co.id AS id_consulta,
    m.nombre AS mascota,
    u.nombre AS veterinario,
    co.fecha,
    co.motivo,
    co.diagnostico,
    co.tratamiento
FROM consultas co
INNER JOIN historias_clinicas hc
    ON co.id_historia_clinica = hc.id
INNER JOIN mascotas m
    ON hc.id_mascota = m.id
INNER JOIN personal_veterinario pv
    ON co.id_veterinario = pv.id_usuario
INNER JOIN usuarios u
    ON pv.id_usuario = u.id;


-- ============================================================
-- 6. SÍNTOMAS DE LAS CONSULTAS
-- ============================================================

SELECT
    co.id AS id_consulta,
    m.nombre AS mascota,
    sc.sintoma
FROM sintomas_consulta sc
INNER JOIN consultas co
    ON sc.id_consulta = co.id
INNER JOIN historias_clinicas hc
    ON co.id_historia_clinica = hc.id
INNER JOIN mascotas m
    ON hc.id_mascota = m.id
ORDER BY co.id;


-- ============================================================
-- 7. OBSERVACIONES DE LAS CONSULTAS
-- ============================================================

SELECT
    co.id AS id_consulta,
    m.nombre AS mascota,
    oc.observacion
FROM observaciones_consulta oc
INNER JOIN consultas co
    ON oc.id_consulta = co.id
INNER JOIN historias_clinicas hc
    ON co.id_historia_clinica = hc.id
INNER JOIN mascotas m
    ON hc.id_mascota = m.id
ORDER BY co.id;


-- ============================================================
-- 8. MEDICAMENTOS FORMULADOS
-- ============================================================

SELECT
    co.id AS id_consulta,
    m.nombre AS mascota,
    mf.nombre AS medicamento,
    mf.dosis,
    mf.frecuencia,
    mf.duracion,
    mf.fecha_inicio,
    mf.fecha_fin,
    mf.estado
FROM medicamentos_formulados mf
INNER JOIN consultas co
    ON mf.id_consulta = co.id
INNER JOIN historias_clinicas hc
    ON co.id_historia_clinica = hc.id
INNER JOIN mascotas m
    ON hc.id_mascota = m.id
ORDER BY mf.fecha_inicio;


-- ============================================================
-- 9. VACUNAS
-- ============================================================

SELECT
    v.id AS id_vacuna,
    m.nombre AS mascota,
    u.nombre AS veterinario,
    v.nombre AS vacuna,
    v.fecha_aplicacion,
    v.fecha_proxima,
    v.lote,
    v.estado
FROM vacunas v
INNER JOIN mascotas m
    ON v.id_mascota = m.id
INNER JOIN personal_veterinario pv
    ON v.id_veterinario = pv.id_usuario
INNER JOIN usuarios u
    ON pv.id_usuario = u.id
ORDER BY v.fecha_aplicacion;


-- ============================================================
-- 10. RECORDATORIOS
-- ============================================================

SELECT
    r.id AS id_recordatorio,
    m.nombre AS mascota,
    r.categoria,
    r.fecha,
    r.descripcion,
    r.estado
FROM recordatorios r
INNER JOIN mascotas m
    ON r.id_mascota = m.id
ORDER BY r.fecha;


-- ============================================================
-- 11. GASTOS DE LAS MASCOTAS
-- ============================================================

SELECT
    g.id AS id_gasto,
    m.nombre AS mascota,
    g.fecha,
    g.categoria,
    g.descripcion,
    g.valor
FROM gastos g
INNER JOIN mascotas m
    ON g.id_mascota = m.id
ORDER BY g.fecha;


-- ============================================================
-- 12. TOTAL DE GASTOS POR MASCOTA
-- ============================================================

SELECT
    m.id AS id_mascota,
    m.nombre AS mascota,
    COALESCE(SUM(g.valor), 0) AS total_gastos
FROM mascotas m
LEFT JOIN gastos g
    ON g.id_mascota = m.id
GROUP BY m.id, m.nombre
ORDER BY m.nombre;


-- ============================================================
-- 13. CUIDADOS Y RUTINAS
-- ============================================================

SELECT
    cr.id AS id_cuidado,
    m.nombre AS mascota,
    cr.tipo,
    cr.frecuencia,
    cr.horario,
    cr.notas
FROM cuidados_rutina cr
INNER JOIN mascotas m
    ON cr.id_mascota = m.id
ORDER BY m.nombre;


-- ============================================================
-- 14. SOLICITUDES DE SEGUIMIENTO
-- ============================================================

SELECT
    ss.id AS id_solicitud,
    u.nombre AS propietario,
    m.nombre AS mascota,
    ss.fecha,
    ss.descripcion,
    ss.estado
FROM solicitudes_seguimiento ss
INNER JOIN propietarios p
    ON ss.id_propietario = p.id_usuario
INNER JOIN usuarios u
    ON p.id_usuario = u.id
INNER JOIN mascotas m
    ON ss.id_mascota = m.id
ORDER BY ss.fecha;


-- ============================================================
-- 15. INFORMACIÓN GENERAL DE UNA MASCOTA
-- ============================================================

SELECT
    m.id,
    m.nombre AS mascota,
    m.especie,
    m.raza,
    m.sexo,
    m.fecha_nacimiento,
    m.peso,
    m.microchip,
    u.nombre AS propietario,
    u.correo AS correo_propietario,
    u.telefono AS telefono_propietario
FROM mascotas m
INNER JOIN propietarios p
    ON m.id_propietario = p.id_usuario
INNER JOIN usuarios u
    ON p.id_usuario = u.id
WHERE m.id = 'PET001';


-- ============================================================
-- 16. RESUMEN CLÍNICO DE UNA MASCOTA
-- ============================================================

SELECT
    m.nombre AS mascota,
    hc.id AS historia_clinica,
    co.id AS consulta,
    co.fecha,
    co.motivo,
    co.diagnostico,
    co.tratamiento
FROM mascotas m
INNER JOIN historias_clinicas hc
    ON hc.id_mascota = m.id
INNER JOIN consultas co
    ON co.id_historia_clinica = hc.id
WHERE m.id = 'PET001'
ORDER BY co.fecha DESC;


-- ============================================================
-- 17. CANTIDAD DE CONSULTAS POR MASCOTA
-- ============================================================

SELECT
    m.id,
    m.nombre AS mascota,
    COUNT(co.id) AS cantidad_consultas
FROM mascotas m
LEFT JOIN historias_clinicas hc
    ON hc.id_mascota = m.id
LEFT JOIN consultas co
    ON co.id_historia_clinica = hc.id
GROUP BY m.id, m.nombre
ORDER BY cantidad_consultas DESC;


-- ============================================================
-- 18. CANTIDAD DE CITAS POR VETERINARIO
-- ============================================================

SELECT
    u.nombre AS veterinario,
    COUNT(c.id) AS cantidad_citas
FROM personal_veterinario pv
INNER JOIN usuarios u
    ON pv.id_usuario = u.id
LEFT JOIN citas c
    ON c.id_veterinario = pv.id_usuario
GROUP BY pv.id_usuario, u.nombre
ORDER BY cantidad_citas DESC;


-- ============================================================
-- 19. MASCOTAS CON ALERGIAS
-- ============================================================

SELECT
    m.nombre AS mascota,
    a.alergia
FROM alergias_mascota a
INNER JOIN mascotas m
    ON a.id_mascota = m.id
ORDER BY m.nombre;


-- ============================================================
-- 20. MASCOTAS CON CONDICIONES REGISTRADAS
-- ============================================================

SELECT
    m.nombre AS mascota,
    cm.condicion
FROM condiciones_mascota cm
INNER JOIN mascotas m
    ON cm.id_mascota = m.id
ORDER BY m.nombre;


-- ============================================================
-- 21. VALIDACIÓN DE INTEGRIDAD REFERENCIAL
-- ============================================================
-- Esta consulta busca mascotas cuyo propietario no exista.
-- El resultado esperado es 0 filas.

SELECT
    m.id,
    m.id_propietario
FROM mascotas m
LEFT JOIN propietarios p
    ON m.id_propietario = p.id_usuario
WHERE p.id_usuario IS NULL;


-- ============================================================
-- 22. VALIDACIÓN DE HISTORIAS CLÍNICAS
-- ============================================================
-- El resultado esperado es 0 filas.

SELECT
    hc.id,
    hc.id_mascota
FROM historias_clinicas hc
LEFT JOIN mascotas m
    ON hc.id_mascota = m.id
WHERE m.id IS NULL;


-- ============================================================
-- 23. VALIDACIÓN DE CITAS
-- ============================================================
-- El resultado esperado es 0 filas.

SELECT
    c.id,
    c.id_mascota,
    c.id_veterinario
FROM citas c
LEFT JOIN mascotas m
    ON c.id_mascota = m.id
LEFT JOIN personal_veterinario pv
    ON c.id_veterinario = pv.id_usuario
WHERE m.id IS NULL
   OR pv.id_usuario IS NULL;


-- ============================================================
-- 24. VALIDACIÓN DE CONSULTAS
-- ============================================================
-- El resultado esperado es 0 filas.

SELECT
    co.id,
    co.id_historia_clinica,
    co.id_veterinario,
    co.id_cita
FROM consultas co
LEFT JOIN historias_clinicas hc
    ON co.id_historia_clinica = hc.id
LEFT JOIN personal_veterinario pv
    ON co.id_veterinario = pv.id_usuario
LEFT JOIN citas c
    ON co.id_cita = c.id
WHERE hc.id IS NULL
   OR pv.id_usuario IS NULL
   OR c.id IS NULL;


-- ============================================================
-- 25. VALIDACIÓN DE MEDICAMENTOS
-- ============================================================
-- El resultado esperado es 0 filas.

SELECT
    mf.id,
    mf.id_consulta
FROM medicamentos_formulados mf
LEFT JOIN consultas co
    ON mf.id_consulta = co.id
WHERE co.id IS NULL;


-- ============================================================
-- 26. VALIDACIÓN DE VACUNAS
-- ============================================================
-- El resultado esperado es 0 filas.

SELECT
    v.id,
    v.id_mascota,
    v.id_veterinario
FROM vacunas v
LEFT JOIN mascotas m
    ON v.id_mascota = m.id
LEFT JOIN personal_veterinario pv
    ON v.id_veterinario = pv.id_usuario
WHERE m.id IS NULL
   OR pv.id_usuario IS NULL;


-- ============================================================
-- 27. PRUEBA DE RESTRICCIÓN FOREIGN KEY
-- ============================================================
-- NO EJECUTAR COMO PARTE DEL ARCHIVO COMPLETO.
--
-- Esta operación debe FALLAR porque USR999 no existe
-- como propietario.
--
-- INSERT INTO mascotas (
--     id,
--     id_propietario,
--     nombre,
--     especie
-- )
-- VALUES (
--     'PET999',
--     'USR999',
--     'Mascota de prueba',
--     'Perro'
-- );


-- ============================================================
-- 28. PRUEBA DE RESTRICCIÓN CHECK
-- ============================================================
-- NO EJECUTAR COMO PARTE DEL ARCHIVO COMPLETO.
--
-- Esta operación debe FALLAR porque el peso es negativo.
--
-- INSERT INTO mascotas (
--     id,
--     id_propietario,
--     nombre,
--     especie,
--     peso
-- )
-- VALUES (
--     'PET998',
--     'USR001',
--     'Mascota de prueba',
--     'Perro',
--     -5
-- );


-- ============================================================
-- FIN DE LAS CONSULTAS DE VALIDACIÓN
-- ============================================================