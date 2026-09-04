from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from levels import level_count, shifted_level


BASE_DIR = Path(__file__).resolve().parent
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


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/levels/{level_index}")
def get_level(level_index: int) -> dict:
    if level_index < 0 or level_index >= level_count():
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return {
        "index": level_index,
        "total_levels": level_count(),
        "level": shifted_level(level_index),
    }


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
