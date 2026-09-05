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

## Despliegue

Puedes desplegar esta carpeta en Render, Railway, Fly.io u otro hosting para Python.
Cuando tengas la URL publica, ponla en `window.API_BASE_URL` dentro de `index.html`.
