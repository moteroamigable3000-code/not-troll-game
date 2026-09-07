# Not A Troll Game Backend

Backend pequeno en Python/FastAPI para guardar puntajes fuera del codigo publico del juego.
Tambien sirve los datos de cada nivel para que no queden embebidos en `game.js`.

## Ejecutar localmente

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Luego cambia temporalmente `window.API_BASE_URL` en `index.html`:

```html
window.API_BASE_URL = 'http://127.0.0.1:8000';
```

Sin esta URL, el frontend no puede cargar niveles y mostrara un aviso de backend requerido.

## Endpoints

- `GET /health`: revisa si la API esta viva.
- `GET /levels/{index}`: devuelve solo el nivel solicitado por el juego.
- `GET /scores`: devuelve el top de puntajes.
- `POST /scores`: guarda una partida terminada.
- `POST /auth/register`, `POST /auth/login`: crear cuenta e iniciar sesion.
- `POST /auth/forgot-password`: recibe `{ "email" }` y, si existe una cuenta con ese correo,
  genera un codigo numerico de 6 digitos de un solo uso (vence en 10 minutos) y lo envia por
  correo. Siempre responde igual exista o no la cuenta, para no filtrar que correos estan
  registrados.
- `POST /auth/reset-password`: recibe `{ "email", "code", "password" }`, valida el codigo
  (maximo 5 intentos antes de invalidarlo) y actualiza la contrasena.

## Recuperacion de contrasena por correo

Para enviar el codigo de reseteo se usa la API de [Resend](https://resend.com). Variables de entorno:

- `RESEND_API_KEY`: API key de Resend. Sin ella, el backend no envia el correo real; en su
  lugar imprime el codigo en la consola/logs del servidor (util en desarrollo local).
- `RESEND_FROM`: remitente del correo (por defecto `onboarding@resend.dev`, el dominio de
  pruebas de Resend). Para produccion, verifica tu propio dominio en Resend y usa un remitente
  con ese dominio.

## Despliegue

Puedes desplegar esta carpeta en Render, Railway, Fly.io u otro hosting para Python.
Cuando tengas la URL publica, ponla en `window.API_BASE_URL` dentro de `index.html`.


## Cuenta de pruebas

Al iniciar el backend se prepara la cuenta `admin@bfjgames.com` con una contrase?a almacenada ?nicamente como hash con sal. Al iniciar sesi?n correctamente, se desbloquean todos los niveles jugables y la respuesta indica un saldo m?nimo de 500 monedas. El cliente repone hasta 500 si el saldo es menor; no suma 500 en cada acceso ni reduce un saldo mayor. La cartera actual sigue guard?ndose en el dispositivo.

Reinicia el backend y actualiza los archivos del cliente para activar el cambio. La cuenta no concede permisos de administraci?n del servidor. El servidor de archivos solo permite los recursos p?blicos del juego y bloquea el c?digo del backend, bases de datos y archivos internos. Si usas Nginx u otro servidor est?tico delante, sirve solo los recursos p?blicos tambi?n.
