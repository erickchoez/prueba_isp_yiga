
# Prueba Técnica Backend Developer (Django/DRF + Celery)

## Setup inicial

### 1. Levantar dependencias con Docker
```bash
docker-compose up -d
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Realizar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario (opcional, para admin)
```bash
python manage.py createsuperuser
```

## Ejecución

### 1. Servidor web (Django)
```bash
python manage.py runserver
```

### 2. Celery Worker
```bash
celery -A backend worker --loglevel=info
```

### 3. Celery Beat (para tarea periódica)
```bash
celery -A backend beat --loglevel=info
```

## Endpoints

- Clientes: `GET /api/clientes/` (Listar), `POST /api/clientes/` (Crear), `GET /api/clientes/{id}/` (Detalle), `PATCH /api/clientes/{id}/` (Actualizar), `DELETE /api/clientes/{id}/` (Eliminar lógico)
- Líneas de Servicio: `GET /api/lineas/` (Listar), `POST /api/lineas/` (Crear), `GET /api/lineas/{id}/` (Detalle), `PATCH /api/lineas/{id}/` (Actualizar), `DELETE /api/lineas/{id}/` (Eliminar lógico)
- Rubros: `GET /api/rubros/`, `POST /api/rubros/`, etc.
- Logs de ejecución: `GET /api/logs/`
- Admin: `GET /admin/`

## Tarea periódica de cobranza

Se ejecuta cada 5 minutos y:
- Detecta rubros vencidos/no pagados por línea
- Actualiza saldo vencido y estado de la línea
- Registra logs detallados en la base de datos

## Notas importantes

- Por defecto usa SQLite (solo para pruebas locales)
- Se puede usar PostgreSQL, modifica DATABASES en backend/settings.py
