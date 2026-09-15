# LibManage

Sistema de gestión de biblioteca desarrollado para el ABP.

## Ramas

El proyecto cuenta actualmente con tres ramas:

- `main`: versión principal del proyecto.
- `interfaz`: desarrollo de la interfaz gráfica.
- `database`: desarrollo relacionado con la base de datos.

> **Importante:** Antes de modificar archivos, asegurate de estar trabajando en la rama correspondiente.

---

## 1. Descargar el proyecto

La primera vez que trabajes con el proyecto, clonalo desde GitHub:

```bash
git clone https://github.com/cris-a-guzman/LibManage.git
```

Luego entrá a la carpeta:

```bash
cd LibManage
```

**No es necesario volver a clonar el proyecto cada vez.**

---

## 2. Actualizar el proyecto antes de trabajar

Cada vez que vayas a empezar a trabajar, primero actualizá tu rama:

```bash
git pull
```

Esto trae los cambios que hayan subido tus compañeros a la rama en la que estás.

Por ejemplo, si estás en `interfaz`:

```bash
git switch interfaz
git pull
```

> Aunque no vayas a modificar la parte que actualizó otro compañero, se recomienda hacer `git pull` antes de empezar para trabajar con la versión más reciente de tu rama.

---

## 3. Cambiar de rama

Para ver las ramas disponibles:

```bash
git branch
```

Para cambiar de rama:

```bash
git switch nombre-de-la-rama
```

Por ejemplo:

```bash
git switch interfaz
```

o:

```bash
git switch database
```

Para volver a `main`:

```bash
git switch main
```

---

## 4. Guardar y subir cambios

Después de realizar cambios:

### 1. Ver qué archivos modificaste

```bash
git status
```

### 2. Agregar los cambios

```bash
git add .
```

### 3. Crear un commit

```bash
git commit -m "Descripción breve del cambio"
```

Por ejemplo:

```bash
git commit -m "Agregar pantalla de libros"
```

### 4. Subir los cambios a GitHub

```bash
git push
```

Los cambios se subirán a la rama en la que estés trabajando.

---

## Flujo recomendado

Cada vez que vayas a trabajar:

```bash
git switch nombre-de-tu-rama
git pull
```

Trabajás en el código y después:

```bash
git status
git add .
git commit -m "Descripción del cambio"
git push
```

**No trabajar directamente sobre `main` salvo que el grupo acuerde hacerlo.**