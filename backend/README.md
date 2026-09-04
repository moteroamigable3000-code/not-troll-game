# Not A Troll Game Backend

Backend pequeno en Python/FastAPI para guardar puntajes fuera del codigo publico del juego.

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

## Endpoints

- `GET /health`: revisa si la API esta viva.
- `GET /scores`: devuelve el top de puntajes.
- `POST /scores`: guarda una partida terminada.

## Despliegue

Puedes desplegar esta carpeta en Render, Railway, Fly.io u otro hosting para Python.
Cuando tengas la URL publica, ponla en `window.API_BASE_URL` dentro de `index.html`.
