BEGIN;
CREATE TABLE "libros_tipo_usuario" (
    "id" integer NOT NULL PRIMARY KEY,
    "nombre" varchar(100) NOT NULL
)
;
CREATE TABLE "libros_editorial" (
    "id" integer NOT NULL PRIMARY KEY,
    "nombre" varchar(200) NOT NULL
)
;
CREATE TABLE "libros_categoria" (
    "id" integer NOT NULL PRIMARY KEY,
    "nombre" varchar(200) NOT NULL
)
;
CREATE TABLE "libros_autor_categoria" (
    "id" integer NOT NULL PRIMARY KEY,
    "autor_id" integer NOT NULL,
    "categoria_id" integer NOT NULL REFERENCES "libros_categoria" ("id"),
    UNIQUE ("autor_id", "categoria_id")
)
;
CREATE TABLE "libros_autor" (
    "id" integer NOT NULL PRIMARY KEY,
    "nombre_autor" varchar(100) NOT NULL,
    "nacionalidad" varchar(100) NOT NULL,
    "fecha_nacimiento" date NOT NULL
)
;
CREATE TABLE "libros_libro_categoria" (
    "id" integer NOT NULL PRIMARY KEY,
    "libro_id" integer NOT NULL,
    "categoria_id" integer NOT NULL REFERENCES "libros_categoria" ("id"),
    UNIQUE ("libro_id", "categoria_id")
)
;
CREATE TABLE "libros_libro" (
    "id" integer NOT NULL PRIMARY KEY,
    "nombre_libro" varchar(200) NOT NULL,
    "autor_id" integer NOT NULL REFERENCES "libros_autor" ("id"),
    "editorial_id" integer NOT NULL REFERENCES "libros_editorial" ("id"),
    "paginas" integer NOT NULL,
    "version" varchar(10) NOT NULL,
    "tomo" integer NOT NULL,
    "codigo" integer NOT NULL,
    "estado" varchar(200) NOT NULL,
    "disponibilidad" bool NOT NULL,
    "fecha_adquisicion" date NOT NULL,
    "fecha_publicacion" date NOT NULL
)
;
CREATE TABLE "libros_biblioteca" (
    "id" integer NOT NULL PRIMARY KEY,
    "nombre" varchar(200) NOT NULL,
    "direccion" varchar(200) NOT NULL,
    "telefono" varchar(200) NOT NULL,
    "correo" varchar(200) NOT NULL,
    "reglamento" varchar(200) NOT NULL
)
;
CREATE TABLE "libros_ciudad" (
    "id" integer NOT NULL PRIMARY KEY,
    "nombre" varchar(200) NOT NULL
)
;
CREATE TABLE "libros_usuario" (
    "id" integer NOT NULL PRIMARY KEY,
    "nombre" varchar(100) NOT NULL,
    "apellido" varchar(100) NOT NULL,
    "tipo_id" varchar(100) NOT NULL,
    "identificacion" varchar(100) NOT NULL,
    "fecha_nac" date NOT NULL,
    "telefono" varchar(100) NOT NULL,
    "direccion" varchar(100) NOT NULL,
    "genero" varchar(200) NOT NULL,
    "ciudad_id" integer NOT NULL REFERENCES "libros_ciudad" ("id"),
    "tipo_usuario_id" integer NOT NULL REFERENCES "libros_tipo_usuario" ("id"),
    "user_id" integer NOT NULL UNIQUE,
    "photo" varchar(100)
)
;
CREATE TABLE "libros_bibliotecario" (
    "id" integer NOT NULL PRIMARY KEY,
    "nombre" varchar(200) NOT NULL,
    "apellidos" varchar(200) NOT NULL,
    "telefono" varchar(200) NOT NULL,
    "direcccion" varchar(200) NOT NULL,
    "correo" varchar(200) NOT NULL,
    "genero" varchar(200) NOT NULL
)
;
CREATE TABLE "libros_prestamo" (
    "id" integer NOT NULL PRIMARY KEY,
    "fecha_prestamo" date NOT NULL,
    "fecha_devolucion" date NOT NULL,
    "libro_id" integer NOT NULL REFERENCES "libros_libro" ("id"),
    "bibliotecario" varchar(100),
    "usuario_id" integer NOT NULL REFERENCES "libros_usuario" ("id"),
    "estado_prestamo" varchar(200) NOT NULL
)
;
CREATE TABLE "libros_busqueda" (
    "id" integer NOT NULL PRIMARY KEY,
    "busqueda" varchar(100) NOT NULL,
    "fecha" date NOT NULL,
    "resultados" bool NOT NULL
)
;
CREATE INDEX "libros_libro_40e8bcf3" ON "libros_libro" ("autor_id");
CREATE INDEX "libros_libro_7c985bea" ON "libros_libro" ("editorial_id");
CREATE INDEX "libros_usuario_67a22d87" ON "libros_usuario" ("ciudad_id");
CREATE INDEX "libros_usuario_b74f55c2" ON "libros_usuario" ("tipo_usuario_id");
CREATE INDEX "libros_prestamo_dd67b109" ON "libros_prestamo" ("libro_id");
CREATE INDEX "libros_prestamo_c69e2c81" ON "libros_prestamo" ("usuario_id");

COMMIT;
