-- ============================================================
-- VetCare
-- Sprint 1 - Paso 3
-- Claves primarias y foráneas
-- ============================================================

-- ============================================================
-- CLAVES PRIMARIAS
-- ============================================================

ALTER TABLE usuarios
ADD CONSTRAINT pk_usuarios
PRIMARY KEY (id);

ALTER TABLE propietarios
ADD CONSTRAINT pk_propietarios
PRIMARY KEY (id_usuario);

ALTER TABLE personal_veterinario
ADD CONSTRAINT pk_personal_veterinario
PRIMARY KEY (id_usuario);

ALTER TABLE mascotas
ADD CONSTRAINT pk_mascotas
PRIMARY KEY (id);

ALTER TABLE alergias_mascota
ADD CONSTRAINT pk_alergias_mascota
PRIMARY KEY (id);

ALTER TABLE condiciones_mascota
ADD CONSTRAINT pk_condiciones_mascota
PRIMARY KEY (id);

ALTER TABLE historias_clinicas
ADD CONSTRAINT pk_historias_clinicas
PRIMARY KEY (id);

ALTER TABLE citas
ADD CONSTRAINT pk_citas
PRIMARY KEY (id);

ALTER TABLE consultas
ADD CONSTRAINT pk_consultas
PRIMARY KEY (id);

ALTER TABLE sintomas_consulta
ADD CONSTRAINT pk_sintomas_consulta
PRIMARY KEY (id);

ALTER TABLE observaciones_consulta
ADD CONSTRAINT pk_observaciones_consulta
PRIMARY KEY (id);

ALTER TABLE medicamentos_formulados
ADD CONSTRAINT pk_medicamentos_formulados
PRIMARY KEY (id);

ALTER TABLE vacunas
ADD CONSTRAINT pk_vacunas
PRIMARY KEY (id);

ALTER TABLE recordatorios
ADD CONSTRAINT pk_recordatorios
PRIMARY KEY (id);

ALTER TABLE gastos
ADD CONSTRAINT pk_gastos
PRIMARY KEY (id);

ALTER TABLE cuidados_rutina
ADD CONSTRAINT pk_cuidados_rutina
PRIMARY KEY (id);

ALTER TABLE solicitudes_seguimiento
ADD CONSTRAINT pk_solicitudes_seguimiento
PRIMARY KEY (id);

-- ============================================================
-- CLAVES FORÁNEAS
-- ============================================================

-- Propietarios -> Usuarios
ALTER TABLE propietarios
ADD CONSTRAINT fk_propietarios_usuario
FOREIGN KEY (id_usuario)
REFERENCES usuarios(id);


-- Personal veterinario -> Usuarios
ALTER TABLE personal_veterinario
ADD CONSTRAINT fk_personal_veterinario_usuario
FOREIGN KEY (id_usuario)
REFERENCES usuarios(id);


-- Mascotas -> Propietarios
ALTER TABLE mascotas
ADD CONSTRAINT fk_mascotas_propietario
FOREIGN KEY (id_propietario)
REFERENCES propietarios(id_usuario);


-- Alergias -> Mascotas
ALTER TABLE alergias_mascota
ADD CONSTRAINT fk_alergias_mascota
FOREIGN KEY (id_mascota)
REFERENCES mascotas(id);


-- Condiciones -> Mascotas
ALTER TABLE condiciones_mascota
ADD CONSTRAINT fk_condiciones_mascota
FOREIGN KEY (id_mascota)
REFERENCES mascotas(id);


-- Historia clínica -> Mascotas
ALTER TABLE historias_clinicas
ADD CONSTRAINT fk_historias_mascota
FOREIGN KEY (id_mascota)
REFERENCES mascotas(id);


-- Citas -> Mascotas
ALTER TABLE citas
ADD CONSTRAINT fk_citas_mascota
FOREIGN KEY (id_mascota)
REFERENCES mascotas(id);


-- Citas -> Personal veterinario
ALTER TABLE citas
ADD CONSTRAINT fk_citas_veterinario
FOREIGN KEY (id_veterinario)
REFERENCES personal_veterinario(id_usuario);


-- Consultas -> Historia clínica
ALTER TABLE consultas
ADD CONSTRAINT fk_consultas_historia
FOREIGN KEY (id_historia_clinica)
REFERENCES historias_clinicas(id);


-- Consultas -> Personal veterinario
ALTER TABLE consultas
ADD CONSTRAINT fk_consultas_veterinario
FOREIGN KEY (id_veterinario)
REFERENCES personal_veterinario(id_usuario);


-- Consultas -> Citas
ALTER TABLE consultas
ADD CONSTRAINT fk_consultas_cita
FOREIGN KEY (id_cita)
REFERENCES citas(id);


-- Síntomas -> Consultas
ALTER TABLE sintomas_consulta
ADD CONSTRAINT fk_sintomas_consulta
FOREIGN KEY (id_consulta)
REFERENCES consultas(id);


-- Observaciones -> Consultas
ALTER TABLE observaciones_consulta
ADD CONSTRAINT fk_observaciones_consulta
FOREIGN KEY (id_consulta)
REFERENCES consultas(id);


-- Medicamentos -> Consultas
ALTER TABLE medicamentos_formulados
ADD CONSTRAINT fk_medicamentos_consulta
FOREIGN KEY (id_consulta)
REFERENCES consultas(id);


-- Vacunas -> Mascotas
ALTER TABLE vacunas
ADD CONSTRAINT fk_vacunas_mascota
FOREIGN KEY (id_mascota)
REFERENCES mascotas(id);


-- Vacunas -> Personal veterinario
ALTER TABLE vacunas
ADD CONSTRAINT fk_vacunas_veterinario
FOREIGN KEY (id_veterinario)
REFERENCES personal_veterinario(id_usuario);


-- Recordatorios -> Mascotas
ALTER TABLE recordatorios
ADD CONSTRAINT fk_recordatorios_mascota
FOREIGN KEY (id_mascota)
REFERENCES mascotas(id);


-- Gastos -> Mascotas
ALTER TABLE gastos
ADD CONSTRAINT fk_gastos_mascota
FOREIGN KEY (id_mascota)
REFERENCES mascotas(id);


-- Cuidados y rutinas -> Mascotas
ALTER TABLE cuidados_rutina
ADD CONSTRAINT fk_cuidados_mascota
FOREIGN KEY (id_mascota)
REFERENCES mascotas(id);


-- Solicitudes de seguimiento -> Propietarios
ALTER TABLE solicitudes_seguimiento
ADD CONSTRAINT fk_solicitudes_propietario
FOREIGN KEY (id_propietario)
REFERENCES propietarios(id_usuario);


-- Solicitudes de seguimiento -> Mascotas
ALTER TABLE solicitudes_seguimiento
ADD CONSTRAINT fk_solicitudes_mascota
FOREIGN KEY (id_mascota)
REFERENCES mascotas(id);