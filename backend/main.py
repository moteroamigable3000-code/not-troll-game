from __future__ import annotations

import hashlib
import os
import re
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from levels import level_count, level_meta, playable_level_count, shifted_level


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = Path(os.getenv("FRONTEND_DIR", BASE_DIR.parent))
DB_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR / "scores.db"))
DEFAULT_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://moteroamigable3000-code.github.io",
]


def get_allowed_origins() -> list[str]:
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
    levels_completed: int = Field(ge=1, le=99)
    score: int = Field(ge=0, le=1_000_000)


class ScoreOut(ScoreIn):
    id: int
    created_at: str


class ProgressIn(BaseModel):
    player_id: str = Field(min_length=1, max_length=64)
    unlocked: int = Field(ge=1, le=99)


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


def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 200_000).hex()


def player_id_for(email: str) -> str:
    return f"acct:{email.lower()}"


@app.on_event("startup")
def startup() -> None:
    init_db()


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
    return {"email": email, "player_id": player_id_for(email)}


@app.get("/scores", response_model=list[ScoreOut])
def list_scores(limit: int = 10) -> list[sqlite3.Row]:
    limit = max(1, min(limit, 50))
    with connect() as conn:
        return conn.execute(
            """
            SELECT id, player, deaths, levels_completed, score, created_at
            FROM scores
            ORDER BY score DESC, deaths ASC, created_at ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()


@app.post("/scores", response_model=ScoreOut, status_code=201)
def create_score(score: ScoreIn) -> sqlite3.Row:
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
    return row


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
