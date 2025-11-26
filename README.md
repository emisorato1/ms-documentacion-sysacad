

# Microservicio de Documentación - SYSACAD

Este proyecto es un microservicio orquestador desarrollado en Python (Flask) utilizando Granian como servidor HTTP y uv para la gestión de dependencias.

Su función principal es generar documentación académica (Certificados de Alumno Regular) en formatos PDF, ODT y DOCX. Para ello, consume datos de otros microservices (Alumnos y Gestión Académica) y los combina en plantillas predefinidas.

## Prerrequisitos

- Git: Para clonar el repositorio.

- Python 3.12+: Lenguaje base.

- Docker & Docker Compose: Para levantar el microservicio de documentación.

- uv: Gestor de paquetes y entornos virtuales de alto rendimiento.


## Instalación y Configuración Local
Sigue estos pasos para ejecutar el microservicio en tu máquina local (sin Docker) para desarrollo.

1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd ms-documentacion-sysacad
```

2. Crear entorno y sincronizar dependencias

Utilizamos uv para asegurar una instalación rápida y determinista basada en uv.lock.

```bash
# Crea el entorno virtual (.venv) e instala las dependencias definidas en pyproject.toml
uv sync

```


3. Configurar entorno
Crea un archivo .env en la raíz del proyecto basándote en el ejemplo:

```bash
cp .env-example .env
```


4. Ejecutar el servidor

Puedes usar uv run para ejecutar el servidor Granian utilizando el entorno virtual creado:

```bash
uv run granian --port 5000 --host 0.0.0.0 --http auto --workers 1 --interface wsgi wsgi:app
```


5. Configuración de Variables de Entorno en el .env

FLASK_CONTEXT=development
# URLs apuntando al HOST (tu máquina) porque levantaste los mocks manualmente con docker run -p
ALUMNO_SERVICE_URL=http://localhost:8080/api/v1/alumnos
GESTION_SERVICE_URL=http://localhost:8081/api/v1/especialidades





## Despliegue con Docker

**Importante:** Los mocks (mock-alumno y mock-gestion) son servicios separados que deben levantarse manualmente antes del microservicio de documentación.

### 1. Levantar los mocks manualmente

Primero, construye y ejecuta los mocks como servicios independientes:

**Mock Alumno (puerto 8080):**
```bash
cd ../mock-server-alumno-main
docker build -t mock-alumno:latest .
docker run -d --name mock-alumno --network emisoratored -p 8080:8080 mock-alumno:latest
```

**Mock Gestión Académica (puerto 8081):**
```bash
cd ../mock-gestion-academica-main/mock-gestion-academica-main
docker build -t mock-gestion:latest .
docker run -d --name mock-gestion --network emisoratored -p 8081:8080 mock-gestion:latest
```

**Nota:** Si la red `emisoratored` no existe, créala primero:
```bash
docker network create emisoratored
```

### 2. Levantar el microservicio de documentación

```bash
cd docker
```

Este comando construye la imagen (si es necesario) y levanta el microservicio:

```bash
docker compose up -d --build
```

### 3. Configurar variables de entorno

Antes de levantar el microservicio, asegúrate de tener un archivo `.env` en el directorio `docker/` con las URLs de los servicios mock:

```bash
cd docker
cp ../.env-example .env
```

Edita el archivo `.env` y configura las URLs según tu entorno:

**Para Docker (mocks en la misma red):**
```bash
FLASK_CONTEXT=production
ALUMNO_SERVICE_URL=http://mock-alumno:8080/api/v1/alumnos
GESTION_SERVICE_URL=http://mock-gestion:8080/api/v1/especialidades
```

**Para desarrollo local (mocks en localhost):**
```bash
FLASK_CONTEXT=development
ALUMNO_SERVICE_URL=http://localhost:8080/api/v1/alumnos
GESTION_SERVICE_URL=http://localhost:8081/api/v1/especialidades
```

### 4. Ver logs en tiempo real

Para ver los logs del microservicio:
```bash
docker compose logs -f documentacion
```

### 5. Detener servicios

**Detener el microservicio de documentación:**
```bash
docker compose stop
```

**Detener los mocks (manual):**
```bash
docker stop mock-alumno mock-gestion
docker rm mock-alumno mock-gestion
```

**Reiniciar el microservicio:**
Si hiciste cambios en el código y necesitas reiniciar:
```bash
docker compose down
docker compose up -d --build
```






## Uso de la API

Una vez levantado con Docker, el microservicio estará disponible en http://localhost:5001.

### Endpoints de Certificados
El flujo es: Se solicita un certificado pasando el ID del alumno. El microservicio busca los datos personales y académicos y devuelve el archivo generado.

1. Generar PDF
Muestra el PDF directamente en el navegador.

Método: GET
http://localhost:5001/api/v1/certificado/<id_alumno>/pdf

2. Descargar ODT (OpenDocument Text)
Descarga el archivo editable compatible con LibreOffice/OpenOffice.

Método: GET
http://localhost:5001/api/v1/certificado/<id_alumno>/odt

3. Descargar DOCX (Microsoft Word)
Descarga el archivo editable compatible con Word.

Método: GET
http://localhost:5001/api/v1/certificado/<id_alumno>/docx

