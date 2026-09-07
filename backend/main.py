from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import sqlite3
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from levels import level_count, level_meta, playable_level_count, shifted_level


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = Path(os.getenv("FRONTEND_DIR", BASE_DIR.parent))
DB_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR / "scores.db"))
DEFAULT_ORIGINS = ["*"]

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_FROM = os.getenv("RESEND_FROM", "Evil Devil Ghost | Not A Troll Game <onboarding@resend.dev>")
RESET_CODE_TTL_MINUTES = 10
MAX_RESET_ATTEMPTS = 5


def get_allowed_origins() -> list[str]:
    # Wildcard is safe here: allow_credentials=False below, so no cookies or
    # auth headers ever ride along, and every endpoint is already public.
    # This lets the game load levels/scores when embedded on any game
    # portal (CrazyGames, Poki, itch.io, ...) without pre-listing origins.
    configured = os.getenv("CORS_ORIGINS")
    if not configured:
        return DEFAULT_ORIGINS
    return [origin.strip() for origin in configured.split(",") if origin.strip()]


app = FastAPI(title="Not A Troll Game API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class ScoreIn(BaseModel):
    player: str = Field(default="Anonimo", max_length=32)
    deaths: int = Field(ge=0, le=9999)
    levels_completed: int = Field(ge=1, le=level_count())
    score: int = Field(ge=0, le=1_000_000)


class ScoreOut(ScoreIn):
    id: int
    created_at: str


class ProgressIn(BaseModel):
    player_id: str = Field(min_length=1, max_length=64)
    unlocked: int = Field(ge=1, le=level_count())


class ProgressOut(BaseModel):
    player_id: str
    unlocked: int


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class AuthIn(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=4, max_length=72)


class AuthOut(BaseModel):
    email: str
    player_id: str
    coin_floor: int = 0


class ForgotPasswordIn(BaseModel):
    email: str = Field(min_length=5, max_length=254)


class ResetPasswordIn(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    code: str = Field(min_length=6, max_length=6)
    password: str = Field(min_length=4, max_length=72)


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                deaths INTEGER NOT NULL,
                levels_completed INTEGER NOT NULL,
                score INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS progress (
                player_id TEXT PRIMARY KEY,
                unlocked INTEGER NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        # Migrate the old link-token reset table (if present) to the
        # code-based schema below.
        existing_columns = {
            row["name"] for row in conn.execute("PRAGMA table_info(password_resets)")
        }
        if existing_columns and "code_hash" not in existing_columns:
            conn.execute("DROP TABLE password_resets")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS password_resets (
                email TEXT PRIMARY KEY,
                code_hash TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                attempts INTEGER NOT NULL DEFAULT 0
            )
            """
        )


def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 200_000).hex()


def hash_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def send_reset_email(email: str, code: str) -> None:
    if not RESEND_API_KEY:
        print(f"[dev] Codigo de reseteo para {email}: {code}")
        return
    payload = json.dumps(
        {
            "from": RESEND_FROM,
            "to": [email],
            "subject": "Tu codigo para restablecer la contrasena - Not A Troll Game",
            "html": (
                "<p>Usa este codigo para restablecer tu contrasena:</p>"
                f'<p style="font-size:28px;font-weight:bold;letter-spacing:4px">{code}</p>'
                f"<p>Vence en {RESET_CODE_TTL_MINUTES} minutos. "
                "Si no lo pediste, ignora este correo.</p>"
            ),
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
            # Cloudflare (in front of Resend's API) blocks urllib's default
            # "Python-urllib/..." user agent as a bot signature (error 1010).
            "User-Agent": "NotATrollGame-Backend/1.0",
        },
    )
    try:
        urllib.request.urlopen(request, timeout=10)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"No se pudo enviar el correo de reseteo a {email}: {exc} - {body}")
    except urllib.error.URLError as exc:
        print(f"No se pudo enviar el correo de reseteo a {email}: {exc}")


# Server-only test account; store only a salted password hash.
TEST_EMAIL = "admin@bfjgames.com"
TEST_PASSWORD_SALT = "0e72a499c3af68f0c5d9a32238a49a17"
TEST_PASSWORD_HASH = "a28b9b4fb3185732078d703d399a1656dbebf286a25c8b1950e7563eb46eca2c"


def player_id_for(email: str) -> str:
    return f"acct:{email.lower()}"


@app.on_event("startup")
def startup() -> None:
    init_db()
    with connect() as conn:
        conn.execute(
            """INSERT INTO users (email, password_hash, password_salt, created_at)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(email) DO UPDATE SET
                   password_hash = excluded.password_hash,
                   password_salt = excluded.password_salt""",
            (TEST_EMAIL, TEST_PASSWORD_HASH, TEST_PASSWORD_SALT,
             datetime.now(timezone.utc).isoformat()),
        )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/levels/{level_index}")
def get_level(level_index: int, player_id: str | None = None) -> dict:
    if level_index < 0 or level_index >= level_count():
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    meta = level_meta()[level_index]
    if meta["locked"]:
        raise HTTPException(status_code=403, detail="Nivel bloqueado")
    unlocked = 1
    if player_id:
        with connect() as conn:
            row = conn.execute(
                "SELECT unlocked FROM progress WHERE player_id = ?",
                (player_id,),
            ).fetchone()
        if row is not None:
            unlocked = min(row["unlocked"], playable_level_count())
    if level_index >= unlocked:
        raise HTTPException(status_code=403, detail="Nivel bloqueado")
    return {
        "index": level_index,
        "total_levels": level_count(),
        "level": shifted_level(level_index),
    }


@app.get("/levels")
def get_levels() -> dict:
    return {"total_levels": level_count(), "levels": level_meta()}


@app.get("/progress/{player_id}", response_model=ProgressOut)
def get_progress(player_id: str) -> dict:
    with connect() as conn:
        row = conn.execute(
            "SELECT player_id, unlocked FROM progress WHERE player_id = ?",
            (player_id,),
        ).fetchone()
    if row is None:
        return {"player_id": player_id, "unlocked": 1}
    return {"player_id": row["player_id"], "unlocked": min(row["unlocked"], playable_level_count())}


@app.post("/progress", response_model=ProgressOut)
def save_progress(progress: ProgressIn) -> dict:
    unlocked = min(progress.unlocked, playable_level_count())
    now = datetime.now(timezone.utc).isoformat()
    with connect() as conn:
        row = conn.execute(
            "SELECT unlocked FROM progress WHERE player_id = ?",
            (progress.player_id,),
        ).fetchone()
        new_unlocked = max(unlocked, row["unlocked"]) if row is not None else unlocked
        conn.execute(
            """
            INSERT INTO progress (player_id, unlocked, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(player_id) DO UPDATE SET
                unlocked = excluded.unlocked,
                updated_at = excluded.updated_at
            """,
            (progress.player_id, new_unlocked, now),
        )
    return {"player_id": progress.player_id, "unlocked": new_unlocked}


@app.post("/auth/register", response_model=AuthOut, status_code=201)
def register(auth: AuthIn) -> dict:
    if not EMAIL_RE.match(auth.email):
        raise HTTPException(status_code=400, detail="Ingresa un correo valido.")
    email = auth.email.lower()
    salt = secrets.token_hex(16)
    password_hash = hash_password(auth.password, salt)
    now = datetime.now(timezone.utc).isoformat()
    with connect() as conn:
        existing = conn.execute(
            "SELECT email FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing is not None:
            raise HTTPException(status_code=409, detail="Ya existe una cuenta con ese correo.")
        conn.execute(
            "INSERT INTO users (email, password_hash, password_salt, created_at) VALUES (?, ?, ?, ?)",
            (email, password_hash, salt, now),
        )
    return {"email": email, "player_id": player_id_for(email)}


@app.post("/auth/login", response_model=AuthOut)
def login(auth: AuthIn) -> dict:
    email = auth.email.lower()
    with connect() as conn:
        row = conn.execute(
            "SELECT password_hash, password_salt FROM users WHERE email = ?",
            (email,),
        ).fetchone()
    if row is None or not secrets.compare_digest(
        hash_password(auth.password, row["password_salt"]), row["password_hash"]
    ):
        raise HTTPException(status_code=401, detail="Correo o contrasena incorrectos.")
    player_id = player_id_for(email)
    coin_floor = 0
    if email == TEST_EMAIL:
        with connect() as conn:
            conn.execute(
                """INSERT INTO progress (player_id, unlocked, updated_at) VALUES (?, ?, ?)
                   ON CONFLICT(player_id) DO UPDATE SET
                       unlocked = excluded.unlocked, updated_at = excluded.updated_at""",
                (player_id, playable_level_count(), datetime.now(timezone.utc).isoformat()),
            )
        coin_floor = 500
    return {"email": email, "player_id": player_id, "coin_floor": coin_floor}


@app.post("/auth/forgot-password", status_code=202)
def forgot_password(payload: ForgotPasswordIn) -> dict:
    email = payload.email.strip().lower()
    now = datetime.now(timezone.utc)
    with connect() as conn:
        user = conn.execute("SELECT email FROM users WHERE email = ?", (email,)).fetchone()
        if user is not None:
            code = f"{secrets.randbelow(1_000_000):06d}"
            expires_at = (now + timedelta(minutes=RESET_CODE_TTL_MINUTES)).isoformat()
            conn.execute(
                """
                INSERT INTO password_resets (email, code_hash, expires_at, attempts)
                VALUES (?, ?, ?, 0)
                ON CONFLICT(email) DO UPDATE SET
                    code_hash = excluded.code_hash,
                    expires_at = excluded.expires_at,
                    attempts = 0
                """,
                (email, hash_code(code), expires_at),
            )
            send_reset_email(email, code)
    # Same response regardless of whether the email exists, to avoid leaking
    # which addresses have accounts.
    return {"detail": "Si el correo existe, enviamos un codigo para restablecer la contrasena."}


@app.post("/auth/reset-password", response_model=AuthOut)
def reset_password(payload: ResetPasswordIn) -> dict:
    email = payload.email.strip().lower()
    now = datetime.now(timezone.utc)
    with connect() as conn:
        row = conn.execute(
            "SELECT code_hash, expires_at, attempts FROM password_resets WHERE email = ?",
            (email,),
        ).fetchone()
        if row is None or datetime.fromisoformat(row["expires_at"]) < now:
            raise HTTPException(status_code=400, detail="El codigo es invalido o ya vencio.")
        if row["attempts"] >= MAX_RESET_ATTEMPTS:
            conn.execute("DELETE FROM password_resets WHERE email = ?", (email,))
            conn.commit()
            raise HTTPException(status_code=400, detail="Demasiados intentos. Solicita un codigo nuevo.")
        if not secrets.compare_digest(hash_code(payload.code), row["code_hash"]):
            conn.execute("UPDATE password_resets SET attempts = attempts + 1 WHERE email = ?", (email,))
            conn.commit()
            raise HTTPException(status_code=400, detail="El codigo es invalido o ya vencio.")
        salt = secrets.token_hex(16)
        password_hash = hash_password(payload.password, salt)
        conn.execute(
            "UPDATE users SET password_hash = ?, password_salt = ? WHERE email = ?",
            (password_hash, salt, email),
        )
        conn.execute("DELETE FROM password_resets WHERE email = ?", (email,))
    return {"email": email, "player_id": player_id_for(email)}


@app.get("/scores", response_model=list[ScoreOut])
def list_scores(limit: int = 10) -> list[dict]:
    limit = max(1, min(limit, 50))
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT id, player, deaths, levels_completed, score, created_at
            FROM scores
            ORDER BY score DESC, deaths ASC, created_at ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


@app.post("/scores", response_model=ScoreOut, status_code=201)
def create_score(score: ScoreIn) -> dict:
    player = score.player.strip() or "Anonimo"
    created_at = datetime.now(timezone.utc).isoformat()
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO scores (player, deaths, levels_completed, score, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (player, score.deaths, score.levels_completed, score.score, created_at),
        )
        row = conn.execute(
            """
            SELECT id, player, deaths, levels_completed, score, created_at
            FROM scores
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=500, detail="No se pudo guardar el puntaje")
    return dict(row)


class PublicStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        # Never expose backend source, databases, deployment files or dotfiles.
        parts = Path(path.replace("\\", "/")).parts
        allowed = {"index.html", "game.js", "game.min.js", "style.css", "recursos", "favicon.ico"}
        if parts and (parts[0] not in allowed or any(part.startswith(".") for part in parts)):
            if path not in (".", ""):
                raise HTTPException(status_code=404, detail="Not found")
        response = await super().get_response(path, scope)
        if path in (".", "", "index.html", "game.js", "game.min.js"):
            response.headers["Cache-Control"] = "no-cache"
        return response


if FRONTEND_DIR.exists():
    app.mount("/", PublicStaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
