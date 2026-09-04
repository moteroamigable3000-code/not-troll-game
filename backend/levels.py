from __future__ import annotations

from copy import deepcopy


GROUND_LIFT = 90


def rect(x: int, y: int, w: int, h: int) -> dict[str, int]:
    return {"x": x, "y": y, "w": w, "h": h}


LEVELS = [
    {
        "name": "Nivel 1",
        "hint": "Flechas / A-D para moverte, Espacio para saltar",
        "width": 1400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1320, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 500, 40), "type": "solid"},
            {**rect(560, 500, 300, 40), "type": "solid"},
            {**rect(920, 460, 200, 40), "type": "solid"},
            {**rect(1180, 500, 220, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(500, 480, 60, 60), "type": "spike"},
        ],
    },
    {
        "name": "Nivel 2",
        "hint": "Cuidado con los huecos",
        "width": 1600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(400, 500, 220, 40), "type": "solid"},
            {**rect(720, 460, 160, 40), "type": "solid"},
            {**rect(980, 500, 160, 40), "type": "solid"},
            {**rect(1240, 440, 160, 40), "type": "solid"},
            {**rect(1480, 500, 120, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(300, 520, 100, 20), "type": "spike"},
            {**rect(620, 520, 100, 20), "type": "spike"},
            {**rect(880, 520, 100, 20), "type": "spike"},
            {**rect(1140, 520, 100, 20), "type": "spike"},
        ],
    },
    {
        "name": "Nivel 3",
        "hint": "Ese piso se ve... demasiado normal?",
        "width": 1500,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1420, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "solid"},
            {**rect(400, 500, 200, 40), "type": "hidden_spike", "triggerX": 430, "delay": 0.28},
            {**rect(600, 500, 260, 40), "type": "solid"},
            {**rect(940, 500, 160, 40), "type": "hidden_spike", "triggerX": 960, "delay": 0.22},
            {**rect(1100, 500, 350, 40), "type": "solid"},
        ],
        "hazards": [],
    },
    {
        "name": "Nivel 4",
        "hint": "Aprende el patron, no confies en tus ojos",
        "width": 1600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 180, 40), "type": "hidden_spike", "triggerX": 330, "delay": 0.25},
            {**rect(480, 500, 200, 40), "type": "solid"},
            {**rect(680, 460, 160, 40), "type": "hidden_spike", "triggerX": 700, "delay": 0.2},
            {**rect(840, 460, 160, 40), "type": "solid"},
            {**rect(1000, 500, 200, 40), "type": "hidden_spike", "triggerX": 1030, "delay": 0.25},
            {**rect(1200, 500, 340, 40), "type": "solid"},
        ],
        "hazards": [],
    },
    {
        "name": "Nivel 5",
        "hint": "No todo lo que parece solido lo es",
        "width": 1500,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1420, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "solid"},
            {**rect(350, 500, 100, 40), "type": "fake_floor"},
            {**rect(450, 500, 340, 40), "type": "solid"},
            {**rect(790, 500, 100, 40), "type": "fake_floor"},
            {**rect(890, 500, 610, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2000, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 6",
        "hint": "Corre antes de que se caiga",
        "width": 1600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 120, 40), "type": "crumble", "delay": 0.35},
            {**rect(420, 500, 120, 40), "type": "crumble", "delay": 0.35},
            {**rect(540, 500, 120, 40), "type": "crumble", "delay": 0.35},
            {**rect(700, 460, 300, 40), "type": "solid"},
            {**rect(1080, 500, 160, 40), "type": "crumble", "delay": 0.3},
            {**rect(1300, 500, 300, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2000, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 7",
        "hint": "La sierra no perdona",
        "width": 1600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 1600, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2000, 40), "type": "void_disabled"},
        ],
        "saws": [
            {"x": 500, "y": 470, "r": 22, "minX": 400, "maxX": 700, "speed": 160},
            {"x": 1000, "y": 470, "r": 22, "minX": 900, "maxX": 1300, "speed": 220},
        ],
    },
    {
        "name": "Nivel 8",
        "hint": "Las paredes tambien muerden",
        "width": 1600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 1600, 40), "type": "solid"},
        ],
        "hazards": [],
        "wallSpikes": [
            {"x": 500, "y": 430, "w": 24, "h": 70, "reach": 55, "triggerX": 470, "delay": 0.25, "dir": 1},
            {"x": 1000, "y": 430, "w": 24, "h": 70, "reach": 55, "triggerX": 970, "delay": 0.25, "dir": 1},
        ],
    },
    {
        "name": "Nivel 9 - Prueba final",
        "hint": "Todo lo aprendido, junto",
        "width": 2000,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1920, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 160, 40), "type": "hidden_spike", "triggerX": 330, "delay": 0.22},
            {**rect(460, 500, 160, 40), "type": "crumble", "delay": 0.3},
            {**rect(620, 460, 200, 40), "type": "solid"},
            {**rect(820, 460, 100, 40), "type": "fake_floor"},
            {**rect(920, 460, 60, 40), "type": "solid"},
            {**rect(980, 500, 260, 40), "type": "solid"},
            {**rect(1240, 500, 160, 40), "type": "hidden_spike", "triggerX": 1270, "delay": 0.2},
            {**rect(1400, 460, 260, 40), "type": "solid"},
            {**rect(1660, 460, 160, 40), "type": "crumble", "delay": 0.28},
            {**rect(1820, 500, 200, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2200, 40), "type": "void"},
        ],
        "saws": [
            {"x": 720, "y": 430, "r": 20, "minX": 640, "maxX": 800, "speed": 180},
        ],
        "wallSpikes": [
            {"x": 1500, "y": 430, "w": 24, "h": 70, "reach": 55, "triggerX": 1470, "delay": 0.22, "dir": 1},
        ],
    },
]


def shifted_level(index: int) -> dict:
    level = deepcopy(LEVELS[index])
    level["spawn"]["y"] -= GROUND_LIFT
    level["goal"]["y"] -= GROUND_LIFT
    for platform in level.get("platforms", []):
        platform["y"] -= GROUND_LIFT
    for hazard in level.get("hazards", []):
        if hazard.get("type") != "void":
            hazard["y"] -= GROUND_LIFT
    for saw in level.get("saws", []):
        saw["y"] -= GROUND_LIFT
    for wall_spike in level.get("wallSpikes", []):
        wall_spike["y"] -= GROUND_LIFT
    return level


def level_count() -> int:
    return len(LEVELS)


def level_meta() -> list[dict]:
    return [
        {"index": i, "name": lvl["name"], "hint": lvl.get("hint", "")}
        for i, lvl in enumerate(LEVELS)
    ]
