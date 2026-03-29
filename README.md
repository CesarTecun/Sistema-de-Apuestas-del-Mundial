# Sistema de Apuestas del Mundial 2026

## Stack Tecnológico
- **Backend**: Python + Django + Django REST Framework
- **Frontend**: React + Node.js
- **Base de Datos**: PostgreSQL (recomendado)

## Estructura del Proyecto
```
Sistema de Apuestas del Mundial/
├── backend/              # Proyecto Django
│   ├── manage.py
│   ├── backend/
│   └── requirements.txt
├── frontend/             # Proyecto React
│   ├── src/
│   ├── public/
│   └── package.json
└── README.md
```

## Instalación para Desarrollo

### Prerrequisitos
- Python 3.10+
- Node.js 18+
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd "Sistema de Apuestas del Mundial"
```

2. **Instalar dependencias del Backend**
```bash
pip install -r requirements.txt
```

3. **Instalar dependencias del Frontend**
```bash
cd frontend
npm install
cd ..
```

### Ejecutar en Desarrollo

1. **Backend (Django)**
```bash
python manage.py migrate
python manage.py runserver
```
El backend correrá en: http://localhost:8000

2. **Frontend (React)**
```bash
cd frontend
npm start
```
El frontend correrá en: http://localhost:3000

## Configuración de Variables de Entorno

Crear archivo `.env` en la raíz del backend:
```
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Flujo de Trabajo con Git

1. Cada desarrollador crea su rama: `git checkout -b feature/nueva-funcionalidad`
2. Realiza cambios y commitea: `git add . && git commit -m "Descripción del cambio"`
3. Sube al repositorio: `git push origin feature/nueva-funcionalidad`
4. Crea Pull Request para revisión

## Notas Importantes
- Este proyecto está diseñado para ser desarrollado por equipos
- Mantener la estructura de carpetas tal como está
- Seguir las convenciones de nomenclatura de Django y React
