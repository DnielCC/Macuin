# Flask API Framework

Esta es una aplicación Flask configurada para funcionar como framework aislado junto con Laravel.

## Estructura del Proyecto

```
Flask/
├── main.py              # Punto de entrada principal
├── routes.py            # Definición de rutas
├── requirements.txt     # Dependencias Python
├── .env                 # Variables de entorno
├── config/
│   └── config.py       # Configuración de la aplicación
├── templates/           # Plantillas HTML
├── static/             # Archivos estáticos
│   ├── css/
│   └── js/
└── README.md           # Este archivo
```

## Instalación y Ejecución

1. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate     # Windows
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**
   - Editar el archivo `.env` según sea necesario

4. **Ejecutar la aplicación:**
   ```bash
   python main.py
   ```

La aplicación estará disponible en `http://localhost:5000`

## Endpoints Disponibles

- `GET /` - Mensaje de bienvenida
- `GET /health` - Verificación de estado
- `GET /api/v1/info` - Información de la API

## Configuración de Puertos

- Flask: Puerto 5000 (configurable en .env)
- Laravel: Puerto 8000 (usualmente)

Ambos frameworks pueden funcionar simultáneamente en puertos diferentes.
