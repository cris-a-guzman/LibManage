-- ============================================
-- SISTEMA DE GESTIÓN DE BIBLIOTECA
-- DDL - Definición del esquema
-- MySQL 8.x
-- ============================================


-- --------------------------------------------
-- TABLA: socio
-- --------------------------------------------
CREATE TABLE socio (
id_socio INT AUTO_INCREMENT,
    	dni VARCHAR(20) NOT NULL,
    	nombre VARCHAR(100) NOT NULL,
    	apellido VARCHAR(100) NOT NULL,
    	CONSTRAINT pk_socio
        		PRIMARY KEY (id_socio) );


-- --------------------------------------------
-- TABLA: libro
-- --------------------------------------------
CREATE TABLE libro (
    	id_libro INT AUTO_INCREMENT,
   	 isbn VARCHAR(20),
    	titulo VARCHAR(255) NOT NULL,
    	autor VARCHAR(255) NOT NULL,
    	anio INT,
    	cantidad_total INT NOT NULL,
    	CONSTRAINT pk_libro
        		PRIMARY KEY (id_libro),
    	CONSTRAINT chk_libro_cantidad_total
        		CHECK (cantidad_total >= 0) );


-- --------------------------------------------
-- TABLA: prestamo
-- --------------------------------------------
CREATE TABLE prestamo (
    	id_prestamo INT AUTO_INCREMENT,
    	id_socio INT NOT NULL,
    	fecha_prestamo DATE NOT NULL,
    	fecha_devolucion_estimada DATE NOT NULL,
    	fecha_devolucion_real DATE NULL,
    	estado VARCHAR(30) NOT NULL,
    	observaciones TEXT NULL,
    	CONSTRAINT pk_prestamo
        		PRIMARY KEY (id_prestamo),
    	CONSTRAINT fk_prestamo_socio
        		FOREIGN KEY (id_socio)
        		REFERENCES socio(id_socio)
        		ON DELETE RESTRICT
        		ON UPDATE RESTRICT,
    CONSTRAINT chk_prestamo_estado
        CHECK (
            estado IN (
                'activo',
                'vencido',
                'devuelto',
                'cerrado_sin_devolver' ) ),
    CONSTRAINT chk_prestamo_fechas
    	CHECK (
            fecha_devolucion_estimada >= fecha_prestamo),
    CONSTRAINT chk_prestamo_fecha_real
        CHECK (
            fecha_devolucion_real IS NULL
            OR fecha_devolucion_real >= fecha_prestamo ),
    CONSTRAINT chk_prestamo_devolucion
        CHECK (
            (estado = 'devuelto' AND fecha_devolucion_real IS NOT NULL)
            OR (
                estado IN (
                    'activo',
                    'vencido',
                    'cerrado_sin_devolver' )
                AND fecha_devolucion_real IS NULL ) ));


-- --------------------------------------------
-- TABLA: detalle_prestamo
-- --------------------------------------------
CREATE TABLE detalle_prestamo (
    id_prestamo INT NOT NULL,
    id_libro INT NOT NULL,
    cantidad INT NOT NULL,
    CONSTRAINT pk_detalle_prestamo
        PRIMARY KEY (id_prestamo, id_libro),
    CONSTRAINT fk_detalle_prestamo_prestamo
        FOREIGN KEY (id_prestamo)
        REFERENCES prestamo(id_prestamo)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    CONSTRAINT fk_detalle_prestamo_libro
        FOREIGN KEY (id_libro)
        REFERENCES libro(id_libro)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    CONSTRAINT chk_detalle_cantidad
        CHECK (cantidad > 0)
);

