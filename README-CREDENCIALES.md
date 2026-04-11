# Credenciales de demostración (Macuin)

Estas cuentas se crean o actualizan con el script de la API:

`docker exec macuin_api python scripts/seed_macuin_demo_users.py`

Tras ejecutar `setup.sh` o el comando anterior, puedes iniciar sesión en **Flask** (`http://localhost:5001/login`). El formulario usa **correo + contraseña**; el rol lo determina la base de datos (no se elige en el login).

| Rol             | Correo               | Contraseña   |
|-----------------|----------------------|--------------|
| Administrador   | admin@macuin.com     | admin123     |
| Ventas          | ventas@macuin.com    | ventas123    |
| Logística       | logistica@macuin.com | logistica123 |
| Almacén         | almacen@macuin.com   | almacen123   |

## API (HTTP Basic)

Los endpoints protegidos de FastAPI usan autenticación Basic. En Docker Compose el valor por defecto es:

- Usuario: `alidaniel`
- Contraseña: `123456`

Flask debe tener las mismas variables `API_BASIC_USER` y `API_BASIC_PASSWORD` para poder llamar a la API.

## Si no puedes entrar como administrador (Flask)

1. **La API debe estar en marcha** y Flask debe poder alcanzarla (`API_BASE_URL`, por ejemplo `http://localhost:8000` en local o `http://macuin_api:8000` en Docker).
2. Ejecuta el seed de usuarios con bcrypt (crea/actualiza `admin@macuin.com` y el resto):  
   `docker exec macuin_api python scripts/seed_macuin_demo_users.py`
3. Si el usuario existe pero nunca se ejecutó el seed, la API responde *«Usuario sin contraseña configurada»* o *«Credenciales incorrectas»* — el login de Flask ahora muestra ese mensaje en una notificación.
4. Contraseña del administrador demo: **admin123** (tras el seed).

## Seguridad

Son credenciales **solo para desarrollo**. En producción sustituye contraseñas, rotación de secretos y usuarios Basic.
