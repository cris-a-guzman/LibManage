-- ============================================================
-- LibManage - 01_schema.sql
-- Motor: MySQL 8.0.16 o superior
-- No se incluyen DROP para evitar eliminaciones accidentales.
-- ============================================================

CREATE DATABASE IF NOT EXISTS libmanage
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_spanish_ci;

USE libmanage;

-- ------------------------------------------------------------
-- SOCIO
-- ------------------------------------------------------------
CREATE TABLE socio (
    id_socio INT NOT NULL AUTO_INCREMENT,
    dni VARCHAR(20) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_asociacion DATE NOT NULL,
    telefono VARCHAR(100) NOT NULL,
    fecha_baja DATETIME NULL,

    CONSTRAINT pk_socio PRIMARY KEY (id_socio),
    CONSTRAINT uq_socio_dni UNIQUE (dni)
) ENGINE = InnoDB;

-- ------------------------------------------------------------
-- LIBRO
-- ------------------------------------------------------------
CREATE TABLE libro (
    id_libro INT NOT NULL AUTO_INCREMENT,
    isbn VARCHAR(20) NULL,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    anio INT NULL,
    cantidad_total INT NOT NULL,
    fecha_baja DATETIME NULL,

    CONSTRAINT pk_libro PRIMARY KEY (id_libro),
    CONSTRAINT chk_libro_cantidad_total CHECK (cantidad_total >= 0)
) ENGINE = InnoDB;

-- ------------------------------------------------------------
-- PRESTAMO
-- ------------------------------------------------------------
CREATE TABLE prestamo (
    id_prestamo INT NOT NULL AUTO_INCREMENT,
    id_socio INT NOT NULL,
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion_estimada DATE NOT NULL,
    fecha_devolucion_real DATE NULL,
    estado VARCHAR(30) NOT NULL,
    observaciones TEXT NULL,

    CONSTRAINT pk_prestamo PRIMARY KEY (id_prestamo),
    CONSTRAINT fk_prestamo_socio FOREIGN KEY (id_socio)
        REFERENCES socio (id_socio)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT chk_prestamo_estado CHECK (
        estado IN ('activo', 'devuelto', 'cerrado_sin_devolver')
    ),
    CONSTRAINT chk_prestamo_fechas CHECK (
        fecha_devolucion_estimada >= fecha_prestamo
    ),
    CONSTRAINT chk_prestamo_fecha_real CHECK (
        fecha_devolucion_real IS NULL
        OR fecha_devolucion_real >= fecha_prestamo
    ),
    CONSTRAINT chk_prestamo_devolucion CHECK (
        (estado = 'devuelto' AND fecha_devolucion_real IS NOT NULL)
        OR
        (estado IN ('activo', 'cerrado_sin_devolver')
         AND fecha_devolucion_real IS NULL)
    )
) ENGINE = InnoDB;

-- ------------------------------------------------------------
-- DETALLE_PRESTAMO
-- ------------------------------------------------------------
CREATE TABLE detalle_prestamo (
    id_prestamo INT NOT NULL,
    id_libro INT NOT NULL,
    cantidad INT NOT NULL,

    CONSTRAINT pk_detalle_prestamo PRIMARY KEY (id_prestamo, id_libro),
    CONSTRAINT fk_detalle_prestamo_prestamo FOREIGN KEY (id_prestamo)
        REFERENCES prestamo (id_prestamo)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    CONSTRAINT fk_detalle_prestamo_libro FOREIGN KEY (id_libro)
        REFERENCES libro (id_libro)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    CONSTRAINT chk_detalle_cantidad CHECK (cantidad > 0)
) ENGINE = InnoDB;


CREATE UNIQUE INDEX uq_prestamo_socio_activo
ON prestamo (
    (CASE
        WHEN estado = 'activo' THEN id_socio
        ELSE NULL
    END)
);
