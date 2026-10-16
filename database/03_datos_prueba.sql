-- ============================================================
-- LibManage - 03_datos_prueba.sql
-- MySQL 8.0 - Datos de prueba para desarrollo y defensa del ABP.
-- Requiere 01_schema.sql. Ejecutar sobre las tablas VACIAS.
-- No ejecutar con datos reales ni en produccion.
-- No contiene DROP, DELETE ni instrucciones de creacion.
--
-- Contenido: 10 socios, 30 libros, 20 prestamos y 50 detalles.
-- Fecha de referencia: 2026-10-15 (hay prestamos vencidos).
-- Catalogo: 30 titulos reales, ISBN y ediciones verificados con fuentes.
-- Socios, prestamos, cantidades de ejemplares y bajas son ficticios.
-- Los IDs se fijan para relacionar los registros de forma estable.
-- ============================================================

USE libmanage;
SET NAMES utf8mb4;

START TRANSACTION;

-- 1. SOCIOS: 8 vigentes y 2 dados de baja.
INSERT INTO socio (id_socio, dni, nombre, apellido, fecha_asociacion, telefono, fecha_baja)
VALUES
    (1, '30124567', 'Laura', 'Medina', '2025-02-11', '3514552101', NULL),
    (2, '28456123', 'Martín', 'López', '2024-11-03', '3514552102', NULL),
    (3, '33452789', 'Camila', 'Fernández', '2025-05-19', '3514552103', NULL),
    (4, '27311654', 'Diego', 'Rodríguez', '2023-09-07', '3514552104', NULL),
    (5, '35644219', 'Sofía', 'Aguirre', '2026-01-12', '3514552105', NULL),
    (6, '31290476', 'Nicolás', 'Herrera', '2025-03-25', '3514552106', NULL),
    (7, '33987654', 'Valentina', 'Quiroga', '2025-07-09', '3514552107', NULL),
    (8, '29550881', 'Pablo', 'Díaz', '2024-04-15', '3514552108', NULL),
    (9, '26773450', 'Elena', 'Torres', '2023-06-30', '3514552109', '2026-09-22 11:15:00'),
    (10, '36441258', 'Bruno', 'Salas', '2025-10-18', '3514552110', '2026-10-07 16:30:00');

-- 2. LIBROS: titulos, autores, anios de edicion e ISBN reales.
-- 10 Caja Negra, 10 El Gato y La Caja, 8 Anagrama, 2 libros mencionados
-- en conversaciones previas (Anthropos y Editorial Medica Panamericana).
-- ISBN vinculado a la edicion consultada, no a cualquier reedicion o formato.
-- Cantidad total y fecha de baja son datos FICTICIOS para el ejercicio.
-- Fuentes verificables: FUENTES_CATALOGO.md
-- 28 vigentes (uno con stock cero) y 2 dados de baja.
INSERT INTO libro (id_libro, isbn, titulo, autor, anio, cantidad_total, fecha_baja)
VALUES
    (1, '9789871622450', 'Realismo capitalista', 'Mark Fisher', 2016, 4, NULL),
    (2, '9789871622610', 'Los fantasmas de mi vida', 'Mark Fisher', 2017, 3, NULL),
    (3, '9789871622580', 'Aceleracionismo', 'Armen Avanessian y Mauro Reis (comps.)', 2017, 5, NULL),
    (4, '9789878272054', 'Tecgnosis', 'Erik Davis', 2023, 3, NULL),
    (5, '9789878272269', 'Lo impensado', 'N. Katherine Hayles', 2024, 4, NULL),
    (6, '9789878272184', 'La pregunta por la técnica en China', 'Yuk Hui', 2024, 2, NULL),
    (7, '9789878272498', 'El desierto de nosotros mismos', 'Éric Sadin', 2026, 2, NULL),
    (8, '9789878272597', 'Imperios de silicio', 'Nick Srnicek', 2026, 1, NULL),
    (9, '9789878272481', 'Teoría de la dependencia digital', 'Cecilia Rikap', 2026, 3, NULL),
    (10, '9789874862365', 'Recursividad y contingencia', 'Yuk Hui', 2022, 4, NULL),
    (11, '9786319054439', 'El reino: Vida y obra de hongos y humanos', 'María Eugenia López', 2025, 2, NULL),
    (12, '9786319054415', 'La máquina ingobernable', 'Alejandro Galliano', 2024, 3, NULL),
    (13, '9786319005974', 'HumanLife', 'Tomás Gigante', 2024, 5, NULL),
    (14, '9786319005998', 'Febo', 'Sol Traverso', 2024, 2, NULL),
    (15, '9786319005950', 'La suerte de tu lado', 'Marina Larrondo', 2024, 2, NULL),
    (16, '9789874863850', 'Las ceremonias: Crónicas de personas que usan drogas', 'Marcos Aramburu', 2023, 3, NULL),
    (17, '9789874696380', '118: El universo en una tabla', 'Varios autores', 2019, 2, NULL),
    (18, '9789874808080', 'Las olas: Conceptos y herramientas terapéuticas de salud mental', 'Ángel Gargiulo', 2022, 4, NULL),
    (19, '9789874727015', 'Breve atlas anecdótico de la ciencia', 'Juan Manuel Carballeda', 2019, 2, NULL),
    (20, '9789874727084', 'Fiebre: Breve colección de epidemias', 'Juan Manuel Carballeda', 2020, 3, NULL),
    (21, '9788433980533', 'Los errantes', 'Olga Tokarczuk', 2019, 3, NULL),
    (22, '9788433977151', 'El adversario', 'Emmanuel Carrère', 2013, 2, NULL),
    (23, '9788433921765', 'La vida instrucciones de uso', 'Georges Perec', 2023, 2, NULL),
    (24, '9788433964175', 'El entusiasmo', 'Remedios Zafra', 2017, 2, NULL),
    (25, '9788433963772', 'El hambre', 'Martín Caparrós', 2015, 3, NULL),
    (26, '9788433998446', 'El nervio óptico', 'María Gainza', 2017, 0, NULL),
    (27, '9788476583142', 'Filosofía de las ciencias humanas y sociales: Materiales para una fundamentación científica', 'José María Mardones', 1991, 3, NULL),
    (28, '9789500697491', 'Adicciones: Uso de sustancias psicoactivas y presentaciones clínicas de la enfermedad adictiva', 'Marcela Waisman Campos y Antonio Benabarre Hernández', 2026, 2, NULL),
    (29, '9788433964694', 'Frágiles', 'Remedios Zafra', 2021, 2, '2026-09-28 09:00:00'),
    (30, '9788433998767', 'Un apartamento en Urano', 'Paul B. Preciado', 2019, 1, '2026-10-01 17:00:00');

-- 3. PRESTAMOS: 8 activos, 8 devueltos y 4 cerrados sin devolver.
-- Cada socio tiene, como maximo, un prestamo en estado activo.
INSERT INTO prestamo (id_prestamo, id_socio, fecha_prestamo, fecha_devolucion_estimada, fecha_devolucion_real, estado, observaciones)
VALUES
    (1, 1, '2026-09-28', '2026-10-12', NULL, 'activo', 'Préstamo vencido, pendiente de devolución.'),
    (2, 2, '2026-10-02', '2026-10-23', NULL, 'activo', NULL),
    (3, 3, '2026-10-05', '2026-10-19', NULL, 'activo', NULL),
    (4, 4, '2026-10-01', '2026-10-15', NULL, 'activo', 'Vence en la fecha de referencia de estos datos.'),
    (5, 5, '2026-09-16', '2026-10-01', NULL, 'activo', 'Préstamo vencido, pendiente de devolución.'),
    (6, 6, '2026-10-08', '2026-10-22', NULL, 'activo', NULL),
    (7, 7, '2026-10-10', '2026-10-24', NULL, 'activo', 'El socio tiene otro préstamo cerrado sin devolución.'),
    (8, 8, '2026-09-30', '2026-10-14', NULL, 'activo', 'Préstamo vencido; hay un cierre anterior sin devolución.'),
    (9, 1, '2026-07-12', '2026-07-26', '2026-07-24', 'devuelto', NULL),
    (10, 2, '2026-08-01', '2026-08-15', '2026-08-17', 'devuelto', 'Devolución realizada fuera de término.'),
    (11, 3, '2026-08-21', '2026-09-04', '2026-09-02', 'devuelto', NULL),
    (12, 4, '2026-09-01', '2026-09-15', '2026-09-15', 'devuelto', NULL),
    (13, 5, '2026-08-10', '2026-08-24', '2026-08-22', 'devuelto', NULL),
    (14, 6, '2026-09-04', '2026-09-18', '2026-09-20', 'devuelto', 'Devolución realizada fuera de término.'),
    (15, 9, '2026-07-07', '2026-07-21', '2026-07-21', 'devuelto', 'Socio dado de baja con posterioridad.'),
    (16, 10, '2026-08-05', '2026-08-19', '2026-08-17', 'devuelto', 'Socio dado de baja con posterioridad.'),
    (17, 7, '2026-07-18', '2026-08-01', NULL, 'cerrado_sin_devolver', 'No se recuperaron los ejemplares.'),
    (18, 8, '2026-08-07', '2026-08-21', NULL, 'cerrado_sin_devolver', 'No se recuperaron los ejemplares.'),
    (19, 9, '2026-09-02', '2026-09-16', NULL, 'cerrado_sin_devolver', 'Cerrado antes de la baja del socio.'),
    (20, 10, '2026-09-12', '2026-09-26', NULL, 'cerrado_sin_devolver', 'Cerrado antes de la baja del socio y del libro.');

-- 4. DETALLES: al menos un libro por prestamo; maximo 10 titulos.
-- Las copias en activos + cerrados sin devolver no superan el stock.
INSERT INTO detalle_prestamo (id_prestamo, id_libro, cantidad)
VALUES
    (1, 3, 1),
    (1, 5, 1),
    (1, 18, 2),
    (2, 1, 1),
    (2, 8, 1),
    (2, 14, 1),
    (3, 4, 1),
    (3, 13, 1),
    (3, 23, 1),
    (4, 6, 1),
    (4, 10, 2),
    (5, 11, 1),
    (5, 21, 1),
    (5, 27, 1),
    (6, 7, 1),
    (6, 15, 1),
    (6, 25, 2),
    (7, 2, 2),
    (7, 19, 1),
    (8, 9, 2),
    (8, 12, 1),
    (8, 17, 1),
    (9, 3, 1),
    (9, 29, 1),
    (10, 2, 1),
    (10, 10, 1),
    (10, 13, 1),
    (11, 12, 1),
    (11, 15, 1),
    (12, 1, 1),
    (12, 17, 1),
    (12, 20, 1),
    (13, 21, 1),
    (13, 27, 1),
    (14, 4, 1),
    (14, 18, 1),
    (14, 22, 1),
    (15, 6, 1),
    (15, 29, 1),
    (15, 24, 1),
    (16, 14, 1),
    (16, 30, 1),
    (17, 16, 1),
    (17, 22, 1),
    (18, 23, 1),
    (18, 24, 2),
    (19, 28, 1),
    (19, 29, 1),
    (20, 20, 2),
    (20, 30, 1);

COMMIT;
