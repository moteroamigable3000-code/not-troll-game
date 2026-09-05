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
    {
        "name": "Nivel 10 - El Ultimatum",
        "hint": "Todos los trucos a la vez. Sin descanso.",
        "width": 2450,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2370, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 260, 40), "type": "solid"},
            {**rect(260, 500, 140, 40), "type": "hidden_spike", "triggerX": 290, "delay": 0.28},
            {**rect(400, 500, 140, 40), "type": "crumble", "delay": 0.28},
            {**rect(540, 460, 160, 40), "type": "solid"},
            {**rect(700, 460, 140, 40), "type": "fake_floor"},
            {**rect(840, 460, 200, 40), "type": "solid"},
            {**rect(1040, 500, 140, 40), "type": "hidden_spike", "triggerX": 1070, "delay": 0.28},
            {**rect(1180, 500, 160, 40), "type": "crumble", "delay": 0.28},
            {**rect(1340, 500, 300, 40), "type": "solid"},
            {**rect(1640, 460, 140, 40), "type": "fake_floor"},
            {**rect(1780, 460, 160, 40), "type": "solid"},
            {**rect(1940, 500, 140, 40), "type": "hidden_spike", "triggerX": 1970, "delay": 0.28},
            {**rect(2080, 500, 320, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2550, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1400, "y": 470, "r": 22, "minX": 1340, "maxX": 1620, "speed": 230},
            {"x": 2150, "y": 470, "r": 20, "minX": 2080, "maxX": 2380, "speed": 260},
        ],
        "wallSpikes": [
            {"x": 900, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 870, "delay": 0.30, "dir": 1},
            {"x": 2250, "y": 430, "w": 24, "h": 70, "reach": 55, "triggerX": 2220, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 11 - El ritmo no perdona",
        "hint": "Reflejos mas rapidos, huecos mas justos",
        "width": 2300,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2220, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 260, 40), "type": "solid"},
            {**rect(260, 460, 160, 40), "type": "solid"},
            {**rect(420, 460, 120, 40), "type": "fake_floor"},
            {**rect(540, 460, 160, 40), "type": "solid"},
            {**rect(700, 500, 140, 40), "type": "hidden_spike", "triggerX": 730, "delay": 0.28},
            {**rect(840, 500, 140, 40), "type": "crumble", "delay": 0.28},
            {**rect(980, 500, 140, 40), "type": "crumble", "delay": 0.28},
            {**rect(1120, 500, 140, 40), "type": "hidden_spike", "triggerX": 1150, "delay": 0.28},
            {**rect(1260, 500, 300, 40), "type": "solid"},
            {**rect(1560, 460, 120, 40), "type": "fake_floor"},
            {**rect(1680, 460, 140, 40), "type": "solid"},
            {**rect(1820, 500, 140, 40), "type": "hidden_spike", "triggerX": 1850, "delay": 0.28},
            {**rect(1960, 500, 340, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2400, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1400, "y": 470, "r": 22, "minX": 1300, "maxX": 1520, "speed": 220},
            {"x": 2130, "y": 470, "r": 20, "minX": 2000, "maxX": 2280, "speed": 260},
        ],
        "wallSpikes": [
            {"x": 340, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 310, "delay": 0.30, "dir": 1},
            {"x": 2150, "y": 430, "w": 24, "h": 70, "reach": 55, "triggerX": 2120, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 12 - Trampas dobles",
        "hint": "Doble trampa, doble riesgo",
        "width": 2450,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2370, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 240, 40), "type": "solid"},
            {**rect(240, 500, 120, 40), "type": "crumble", "delay": 0.28},
            {**rect(360, 500, 120, 40), "type": "crumble", "delay": 0.28},
            {**rect(480, 500, 120, 40), "type": "hidden_spike", "triggerX": 510, "delay": 0.28},
            {**rect(600, 460, 160, 40), "type": "solid"},
            {**rect(760, 460, 120, 40), "type": "hidden_spike", "triggerX": 790, "delay": 0.28},
            {**rect(880, 460, 120, 40), "type": "fake_floor"},
            {**rect(1000, 500, 360, 40), "type": "solid"},
            {**rect(1360, 500, 140, 40), "type": "crumble", "delay": 0.28},
            {**rect(1500, 460, 140, 40), "type": "fake_floor"},
            {**rect(1640, 460, 160, 40), "type": "solid"},
            {**rect(1800, 500, 140, 40), "type": "hidden_spike", "triggerX": 1830, "delay": 0.28},
            {**rect(1940, 500, 510, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2600, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1080, "y": 470, "r": 20, "minX": 1020, "maxX": 1180, "speed": 220},
            {"x": 1280, "y": 470, "r": 20, "minX": 1200, "maxX": 1340, "speed": 240},
            {"x": 2200, "y": 470, "r": 22, "minX": 2000, "maxX": 2400, "speed": 260},
        ],
        "wallSpikes": [
            {"x": 680, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 650, "delay": 0.30, "dir": 1},
            {"x": 2300, "y": 430, "w": 24, "h": 70, "reach": 55, "triggerX": 2270, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 13 - Al limite",
        "hint": "Si sobrevives esto, ya no hay nada que temer",
        "width": 2600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 220, 40), "type": "solid"},
            {**rect(220, 420, 160, 40), "type": "solid"},
            {**rect(380, 420, 120, 40), "type": "fake_floor"},
            {**rect(500, 420, 160, 40), "type": "solid"},
            {**rect(660, 500, 120, 40), "type": "hidden_spike", "triggerX": 690, "delay": 0.28},
            {**rect(780, 500, 120, 40), "type": "crumble", "delay": 0.28},
            {**rect(900, 500, 120, 40), "type": "hidden_spike", "triggerX": 930, "delay": 0.28},
            {**rect(1020, 500, 120, 40), "type": "crumble", "delay": 0.28},
            {**rect(1140, 500, 360, 40), "type": "solid"},
            {**rect(1500, 460, 120, 40), "type": "fake_floor"},
            {**rect(1620, 460, 140, 40), "type": "solid"},
            {**rect(1760, 500, 120, 40), "type": "hidden_spike", "triggerX": 1790, "delay": 0.28},
            {**rect(1880, 500, 120, 40), "type": "crumble", "delay": 0.28},
            {**rect(2000, 460, 160, 40), "type": "solid"},
            {**rect(2160, 500, 440, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2650, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1220, "y": 470, "r": 20, "minX": 1160, "maxX": 1320, "speed": 230},
            {"x": 1420, "y": 470, "r": 20, "minX": 1340, "maxX": 1480, "speed": 250},
            {"x": 2380, "y": 470, "r": 24, "minX": 2200, "maxX": 2560, "speed": 280},
        ],
        "wallSpikes": [
            {"x": 300, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 270, "delay": 0.30, "dir": 1},
            {"x": 2080, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 2050, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 14 - Sin descanso",
        "hint": "El ritmo no baja nunca",
        "width": 2700,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2620, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 220, 40), "type": "solid"},
            {**rect(220, 500, 100, 40), "type": "fake_floor"},
            {**rect(320, 500, 140, 40), "type": "solid"},
            {**rect(460, 500, 100, 40), "type": "hidden_spike", "triggerX": 490, "delay": 0.28},
            {**rect(560, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(660, 460, 140, 40), "type": "solid"},
            {**rect(800, 460, 100, 40), "type": "hidden_spike", "triggerX": 830, "delay": 0.28},
            {**rect(900, 460, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1000, 500, 340, 40), "type": "solid"},
            {**rect(1340, 460, 100, 40), "type": "fake_floor"},
            {**rect(1440, 460, 140, 40), "type": "solid"},
            {**rect(1580, 500, 100, 40), "type": "hidden_spike", "triggerX": 1610, "delay": 0.28},
            {**rect(1680, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1780, 420, 160, 40), "type": "solid"},
            {**rect(1940, 420, 100, 40), "type": "fake_floor"},
            {**rect(2040, 420, 160, 40), "type": "solid"},
            {**rect(2200, 500, 500, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2800, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1100, "y": 470, "r": 20, "minX": 1040, "maxX": 1200, "speed": 240},
            {"x": 1260, "y": 470, "r": 20, "minX": 1180, "maxX": 1320, "speed": 260},
            {"x": 2450, "y": 470, "r": 24, "minX": 2240, "maxX": 2660, "speed": 280},
        ],
        "wallSpikes": [
            {"x": 740, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 710, "delay": 0.30, "dir": 1},
            {"x": 1520, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 1490, "delay": 0.30, "dir": 1},
            {"x": 2120, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 2090, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 15 - Cuenta atras",
        "hint": "Ya no hay margen de error",
        "width": 2800,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2720, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 200, 40), "type": "solid"},
            {**rect(200, 500, 100, 40), "type": "hidden_spike", "triggerX": 230, "delay": 0.28},
            {**rect(300, 500, 100, 40), "type": "hidden_spike", "triggerX": 330, "delay": 0.28},
            {**rect(400, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(500, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(600, 460, 140, 40), "type": "solid"},
            {**rect(740, 460, 100, 40), "type": "fake_floor"},
            {**rect(840, 460, 120, 40), "type": "solid"},
            {**rect(960, 500, 100, 40), "type": "hidden_spike", "triggerX": 990, "delay": 0.28},
            {**rect(1060, 500, 380, 40), "type": "solid"},
            {**rect(1440, 460, 100, 40), "type": "fake_floor"},
            {**rect(1540, 460, 120, 40), "type": "solid"},
            {**rect(1660, 500, 100, 40), "type": "hidden_spike", "triggerX": 1690, "delay": 0.28},
            {**rect(1760, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1860, 420, 140, 40), "type": "solid"},
            {**rect(2000, 420, 100, 40), "type": "fake_floor"},
            {**rect(2100, 420, 120, 40), "type": "solid"},
            {**rect(2220, 500, 100, 40), "type": "hidden_spike", "triggerX": 2250, "delay": 0.28},
            {**rect(2320, 500, 480, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2900, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1150, "y": 470, "r": 20, "minX": 1090, "maxX": 1250, "speed": 250},
            {"x": 1330, "y": 470, "r": 20, "minX": 1260, "maxX": 1410, "speed": 270},
            {"x": 2500, "y": 470, "r": 22, "minX": 2350, "maxX": 2550, "speed": 260},
            {"x": 2650, "y": 470, "r": 20, "minX": 2580, "maxX": 2770, "speed": 290},
        ],
        "wallSpikes": [
            {"x": 680, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 650, "delay": 0.30, "dir": 1},
            {"x": 1600, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 1570, "delay": 0.30, "dir": 1},
            {"x": 2160, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 2130, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 16 - El vacio final",
        "hint": "El ultimo tramo, sin piedad",
        "width": 3000,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2930, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 180, 40), "type": "solid"},
            {**rect(180, 460, 100, 40), "type": "hidden_spike", "triggerX": 210, "delay": 0.28},
            {**rect(280, 500, 100, 40), "type": "solid"},
            {**rect(380, 460, 120, 40), "type": "crumble", "delay": 0.28},
            {**rect(500, 500, 100, 40), "type": "solid"},
            {**rect(600, 460, 120, 40), "type": "solid"},
            {**rect(720, 500, 100, 40), "type": "hidden_spike", "triggerX": 750, "delay": 0.28},
            {**rect(820, 460, 100, 40), "type": "fake_floor"},
            {**rect(920, 500, 400, 40), "type": "solid"},
            {**rect(1320, 460, 100, 40), "type": "fake_floor"},
            {**rect(1420, 460, 120, 40), "type": "solid"},
            {**rect(1540, 500, 100, 40), "type": "hidden_spike", "triggerX": 1570, "delay": 0.28},
            {**rect(1640, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1740, 420, 140, 40), "type": "solid"},
            {**rect(1880, 420, 100, 40), "type": "fake_floor"},
            {**rect(1980, 420, 120, 40), "type": "solid"},
            {**rect(2100, 500, 100, 40), "type": "hidden_spike", "triggerX": 2130, "delay": 0.28},
            {**rect(2200, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(2300, 500, 380, 40), "type": "solid"},
            {**rect(2680, 460, 100, 40), "type": "fake_floor"},
            {**rect(2780, 460, 100, 40), "type": "solid"},
            {**rect(2880, 500, 120, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3100, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1000, "y": 470, "r": 20, "minX": 940, "maxX": 1100, "speed": 250},
            {"x": 1200, "y": 470, "r": 20, "minX": 1120, "maxX": 1300, "speed": 270},
            {"x": 2400, "y": 470, "r": 22, "minX": 2320, "maxX": 2480, "speed": 260},
            {"x": 2560, "y": 470, "r": 20, "minX": 2500, "maxX": 2660, "speed": 280},
        ],
        "wallSpikes": [
            {"x": 680, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 650, "delay": 0.30, "dir": 1},
            {"x": 1500, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 1470, "delay": 0.30, "dir": 1},
            {"x": 2060, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 2030, "delay": 0.30, "dir": 1},
            {"x": 2860, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 2830, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 17 - Ultima llamada",
        "hint": "No mires atras",
        "width": 2900,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2820, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 200, 40), "type": "solid"},
            {**rect(200, 460, 120, 40), "type": "solid"},
            {**rect(320, 460, 100, 40), "type": "solid"},
            {**rect(420, 460, 100, 40), "type": "fake_floor"},
            {**rect(520, 420, 120, 40), "type": "solid"},
            {**rect(640, 420, 100, 40), "type": "solid"},
            {**rect(740, 420, 100, 40), "type": "fake_floor"},
            {**rect(840, 500, 100, 40), "type": "hidden_spike", "triggerX": 870, "delay": 0.28},
            {**rect(940, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1040, 500, 100, 40), "type": "hidden_spike", "triggerX": 1070, "delay": 0.28},
            {**rect(1140, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1240, 500, 100, 40), "type": "solid"},
            {**rect(1340, 500, 400, 40), "type": "solid"},
            {**rect(1740, 460, 100, 40), "type": "fake_floor"},
            {**rect(1840, 460, 100, 40), "type": "solid"},
            {**rect(1940, 500, 100, 40), "type": "hidden_spike", "triggerX": 1970, "delay": 0.28},
            {**rect(2040, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(2140, 420, 140, 40), "type": "solid"},
            {**rect(2280, 420, 100, 40), "type": "fake_floor"},
            {**rect(2380, 420, 100, 40), "type": "solid"},
            {**rect(2480, 500, 420, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3000, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1440, "y": 470, "r": 20, "minX": 1380, "maxX": 1540, "speed": 260},
            {"x": 1620, "y": 470, "r": 20, "minX": 1560, "maxX": 1700, "speed": 280},
            {"x": 2620, "y": 470, "r": 22, "minX": 2520, "maxX": 2680, "speed": 270},
            {"x": 2780, "y": 470, "r": 20, "minX": 2700, "maxX": 2860, "speed": 300},
        ],
        "wallSpikes": [
            {"x": 370, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 340, "delay": 0.30, "dir": 1},
            {"x": 690, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 660, "delay": 0.30, "dir": 1},
            {"x": 1900, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 1870, "delay": 0.30, "dir": 1},
            {"x": 2440, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 2410, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 18 - Sin piedad",
        "hint": "Un parpadeo y todo termina",
        "width": 3050,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2970, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 180, 40), "type": "solid"},
            {**rect(180, 500, 90, 40), "type": "crumble", "delay": 0.28},
            {**rect(270, 500, 90, 40), "type": "crumble", "delay": 0.28},
            {**rect(360, 500, 110, 40), "type": "crumble", "delay": 0.28},
            {**rect(470, 460, 90, 40), "type": "solid"},
            {**rect(560, 460, 100, 40), "type": "solid"},
            {**rect(660, 420, 110, 40), "type": "fake_floor"},
            {**rect(770, 420, 90, 40), "type": "solid"},
            {**rect(860, 420, 100, 40), "type": "solid"},
            {**rect(960, 500, 90, 40), "type": "hidden_spike", "triggerX": 985, "delay": 0.28},
            {**rect(1050, 500, 90, 40), "type": "hidden_spike", "triggerX": 1075, "delay": 0.28},
            {**rect(1140, 500, 420, 40), "type": "solid"},
            {**rect(1560, 460, 90, 40), "type": "fake_floor"},
            {**rect(1650, 460, 100, 40), "type": "solid"},
            {**rect(1750, 500, 90, 40), "type": "hidden_spike", "triggerX": 1775, "delay": 0.28},
            {**rect(1840, 500, 90, 40), "type": "crumble", "delay": 0.28},
            {**rect(1930, 420, 120, 40), "type": "solid"},
            {**rect(2050, 420, 90, 40), "type": "fake_floor"},
            {**rect(2140, 420, 100, 40), "type": "solid"},
            {**rect(2240, 500, 90, 40), "type": "hidden_spike", "triggerX": 2265, "delay": 0.28},
            {**rect(2330, 500, 720, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3150, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1260, "y": 470, "r": 20, "minX": 1200, "maxX": 1360, "speed": 270},
            {"x": 1440, "y": 470, "r": 20, "minX": 1380, "maxX": 1540, "speed": 290},
            {"x": 2600, "y": 470, "r": 22, "minX": 2400, "maxX": 2700, "speed": 270},
            {"x": 2850, "y": 470, "r": 20, "minX": 2750, "maxX": 3020, "speed": 300},
        ],
        "wallSpikes": [
            {"x": 610, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 580, "delay": 0.30, "dir": 1},
            {"x": 910, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 880, "delay": 0.30, "dir": 1},
            {"x": 1700, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 1670, "delay": 0.30, "dir": 1},
            {"x": 2190, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 2160, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 19 - Casi imposible",
        "hint": "El limite de lo posible",
        "width": 3200,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3120, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 180, 40), "type": "solid"},
            {**rect(180, 500, 90, 40), "type": "hidden_spike", "triggerX": 205, "delay": 0.28},
            {**rect(270, 460, 110, 40), "type": "solid"},
            {**rect(380, 460, 100, 40), "type": "solid"},
            {**rect(480, 460, 90, 40), "type": "hidden_spike", "triggerX": 505, "delay": 0.28},
            {**rect(570, 420, 110, 40), "type": "solid"},
            {**rect(680, 420, 100, 40), "type": "solid"},
            {**rect(780, 420, 90, 40), "type": "crumble", "delay": 0.28},
            {**rect(870, 460, 90, 40), "type": "fake_floor"},
            {**rect(960, 460, 100, 40), "type": "fake_floor"},
            {**rect(1060, 500, 90, 40), "type": "hidden_spike", "triggerX": 1085, "delay": 0.28},
            {**rect(1150, 500, 80, 40), "type": "crumble", "delay": 0.28},
            {**rect(1230, 500, 420, 40), "type": "solid"},
            {**rect(1650, 460, 90, 40), "type": "fake_floor"},
            {**rect(1740, 460, 100, 40), "type": "solid"},
            {**rect(1840, 500, 90, 40), "type": "hidden_spike", "triggerX": 1865, "delay": 0.28},
            {**rect(1930, 500, 90, 40), "type": "crumble", "delay": 0.28},
            {**rect(2020, 420, 130, 40), "type": "solid"},
            {**rect(2150, 420, 90, 40), "type": "fake_floor"},
            {**rect(2240, 420, 100, 40), "type": "solid"},
            {**rect(2340, 500, 90, 40), "type": "hidden_spike", "triggerX": 2365, "delay": 0.28},
            {**rect(2430, 500, 90, 40), "type": "crumble", "delay": 0.28},
            {**rect(2520, 500, 680, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3300, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1350, "y": 470, "r": 20, "minX": 1290, "maxX": 1450, "speed": 270},
            {"x": 1520, "y": 470, "r": 20, "minX": 1460, "maxX": 1610, "speed": 290},
            {"x": 2650, "y": 470, "r": 20, "minX": 2570, "maxX": 2730, "speed": 270},
            {"x": 2850, "y": 470, "r": 20, "minX": 2770, "maxX": 2930, "speed": 290},
            {"x": 3050, "y": 470, "r": 22, "minX": 2960, "maxX": 3160, "speed": 310},
        ],
        "wallSpikes": [
            {"x": 320, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 290, "delay": 0.30, "dir": 1},
            {"x": 620, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 590, "delay": 0.30, "dir": 1},
            {"x": 1790, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 1760, "delay": 0.30, "dir": 1},
            {"x": 2290, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 2260, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 20 - Sin previo aviso",
        "hint": "La sierra no espera a nadie",
        "width": 2900,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2820, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 160, 40), "type": "solid"},
            {**rect(160, 500, 340, 40), "type": "solid"},
            {**rect(500, 460, 100, 40), "type": "fake_floor"},
            {**rect(600, 460, 120, 40), "type": "solid"},
            {**rect(720, 500, 100, 40), "type": "hidden_spike", "triggerX": 750, "delay": 0.28},
            {**rect(820, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(920, 420, 140, 40), "type": "solid"},
            {**rect(1060, 420, 100, 40), "type": "fake_floor"},
            {**rect(1160, 420, 120, 40), "type": "solid"},
            {**rect(1280, 500, 100, 40), "type": "hidden_spike", "triggerX": 1310, "delay": 0.28},
            {**rect(1380, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1480, 500, 420, 40), "type": "solid"},
            {**rect(1900, 460, 100, 40), "type": "fake_floor"},
            {**rect(2000, 460, 120, 40), "type": "solid"},
            {**rect(2120, 500, 100, 40), "type": "hidden_spike", "triggerX": 2150, "delay": 0.28},
            {**rect(2220, 500, 680, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3000, 40), "type": "void"},
        ],
        "saws": [
            {"x": 330, "y": 470, "r": 20, "minX": 200, "maxX": 460, "speed": 260},
            {"x": 1650, "y": 470, "r": 20, "minX": 1540, "maxX": 1740, "speed": 280},
            {"x": 1800, "y": 470, "r": 20, "minX": 1720, "maxX": 1860, "speed": 300},
            {"x": 2600, "y": 470, "r": 24, "minX": 2280, "maxX": 2860, "speed": 310},
        ],
        "wallSpikes": [
            {"x": 660, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 630, "delay": 0.30, "dir": 1},
            {"x": 1220, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 1190, "delay": 0.30, "dir": 1},
            {"x": 2060, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 2030, "delay": 0.30, "dir": 1},
            {"x": 2750, "y": 430, "w": 24, "h": 70, "reach": 55, "triggerX": 2720, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 21 - Muro tras muro",
        "hint": "Sin trucos de piso, solo reflejos",
        "width": 3000,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2920, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 160, 40), "type": "solid"},
            {**rect(160, 460, 120, 40), "type": "solid"},
            {**rect(280, 460, 100, 40), "type": "solid"},
            {**rect(380, 420, 120, 40), "type": "solid"},
            {**rect(500, 420, 100, 40), "type": "solid"},
            {**rect(600, 500, 100, 40), "type": "hidden_spike", "triggerX": 630, "delay": 0.28},
            {**rect(700, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(800, 500, 100, 40), "type": "hidden_spike", "triggerX": 830, "delay": 0.28},
            {**rect(900, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1000, 500, 400, 40), "type": "solid"},
            {**rect(1400, 460, 100, 40), "type": "fake_floor"},
            {**rect(1500, 460, 120, 40), "type": "solid"},
            {**rect(1620, 500, 100, 40), "type": "hidden_spike", "triggerX": 1650, "delay": 0.28},
            {**rect(1720, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1820, 420, 140, 40), "type": "solid"},
            {**rect(1960, 420, 100, 40), "type": "fake_floor"},
            {**rect(2060, 420, 120, 40), "type": "solid"},
            {**rect(2180, 500, 100, 40), "type": "hidden_spike", "triggerX": 2210, "delay": 0.28},
            {**rect(2280, 500, 720, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3100, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1150, "y": 470, "r": 20, "minX": 1080, "maxX": 1240, "speed": 270},
            {"x": 1300, "y": 470, "r": 20, "minX": 1240, "maxX": 1380, "speed": 290},
            {"x": 2550, "y": 470, "r": 22, "minX": 2350, "maxX": 2600, "speed": 280},
            {"x": 2800, "y": 470, "r": 20, "minX": 2650, "maxX": 2980, "speed": 310},
        ],
        "wallSpikes": [
            {"x": 220, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 190, "delay": 0.30, "dir": 1},
            {"x": 440, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 410, "delay": 0.30, "dir": 1},
            {"x": 1560, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 1530, "delay": 0.30, "dir": 1},
            {"x": 2120, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 2090, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 22 - Cae o corre",
        "hint": "El suelo bajo tus pies ya cruje",
        "width": 2950,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2870, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 160, 40), "type": "crumble", "delay": 0.28},
            {**rect(160, 500, 140, 40), "type": "solid"},
            {**rect(300, 500, 100, 40), "type": "hidden_spike", "triggerX": 330, "delay": 0.28},
            {**rect(400, 460, 120, 40), "type": "solid"},
            {**rect(520, 460, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(620, 460, 100, 40), "type": "fake_floor"},
            {**rect(720, 500, 100, 40), "type": "hidden_spike", "triggerX": 750, "delay": 0.28},
            {**rect(820, 500, 380, 40), "type": "solid"},
            {**rect(1200, 420, 100, 40), "type": "fake_floor"},
            {**rect(1300, 420, 120, 40), "type": "solid"},
            {**rect(1420, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1520, 500, 100, 40), "type": "hidden_spike", "triggerX": 1550, "delay": 0.28},
            {**rect(1620, 460, 140, 40), "type": "solid"},
            {**rect(1760, 460, 100, 40), "type": "fake_floor"},
            {**rect(1860, 500, 100, 40), "type": "hidden_spike", "triggerX": 1890, "delay": 0.28},
            {**rect(1960, 500, 990, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3050, 40), "type": "void"},
        ],
        "saws": [
            {"x": 950, "y": 470, "r": 20, "minX": 900, "maxX": 1060, "speed": 270},
            {"x": 1120, "y": 470, "r": 20, "minX": 1060, "maxX": 1180, "speed": 290},
            {"x": 2500, "y": 470, "r": 22, "minX": 2100, "maxX": 2500, "speed": 280},
            {"x": 2750, "y": 470, "r": 22, "minX": 2600, "maxX": 2900, "speed": 310},
        ],
        "wallSpikes": [
            {"x": 460, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 430, "delay": 0.30, "dir": 1},
            {"x": 1360, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 1330, "delay": 0.30, "dir": 1},
            {"x": 1690, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 1660, "delay": 0.30, "dir": 1},
            {"x": 2200, "y": 430, "w": 24, "h": 70, "reach": 55, "triggerX": 2170, "delay": 0.30, "dir": 1},
        ],
    },
    {
        "name": "Nivel 23 - Muros sin fin",
        "hint": "Pared, pared, pared... y otra vez",
        "width": 3220,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3140, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 160, 40), "type": "solid"},
            {**rect(160, 460, 100, 40), "type": "solid"},
            {**rect(260, 460, 120, 40), "type": "solid"},
            {**rect(380, 420, 100, 40), "type": "solid"},
            {**rect(480, 420, 120, 40), "type": "solid"},
            {**rect(600, 460, 100, 40), "type": "solid"},
            {**rect(700, 460, 120, 40), "type": "solid"},
            {**rect(820, 500, 100, 40), "type": "solid"},
            {**rect(920, 500, 400, 40), "type": "solid"},
            {**rect(1320, 500, 100, 40), "type": "hidden_spike", "triggerX": 1350, "delay": 0.28},
            {**rect(1420, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1520, 460, 100, 40), "type": "fake_floor"},
            {**rect(1620, 460, 100, 40), "type": "hidden_spike", "triggerX": 1650, "delay": 0.28},
            {**rect(1720, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1820, 500, 500, 40), "type": "solid"},
            {**rect(2320, 420, 100, 40), "type": "fake_floor"},
            {**rect(2420, 420, 120, 40), "type": "solid"},
            {**rect(2540, 500, 100, 40), "type": "hidden_spike", "triggerX": 2570, "delay": 0.28},
            {**rect(2640, 500, 580, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3320, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1020, "y": 470, "r": 20, "minX": 960, "maxX": 1120, "speed": 280},
            {"x": 1220, "y": 470, "r": 20, "minX": 1140, "maxX": 1300, "speed": 300},
            {"x": 2020, "y": 470, "r": 22, "minX": 1860, "maxX": 2080, "speed": 280},
            {"x": 2220, "y": 470, "r": 22, "minX": 2140, "maxX": 2300, "speed": 300},
            {"x": 2920, "y": 470, "r": 20, "minX": 2680, "maxX": 3200, "speed": 320},
        ],
        "wallSpikes": [
            {"x": 210, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 180, "delay": 0.38, "dir": 1},
            {"x": 430, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 400, "delay": 0.38, "dir": 1},
            {"x": 650, "y": 390, "w": 24, "h": 70, "reach": 55, "triggerX": 620, "delay": 0.38, "dir": 1},
            {"x": 870, "y": 430, "w": 24, "h": 70, "reach": 55, "triggerX": 840, "delay": 0.38, "dir": 1},
            {"x": 2480, "y": 350, "w": 24, "h": 70, "reach": 55, "triggerX": 2450, "delay": 0.38, "dir": 1},
            {"x": 3070, "y": 430, "w": 24, "h": 70, "reach": 55, "triggerX": 3040, "delay": 0.38, "dir": 1},
        ],
    },
    {
        "name": "Nivel 24 - Corre o cae",
        "hint": "El final de este tramo... por ahora",
        "width": 3300,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3220, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 140, 40), "type": "crumble", "delay": 0.28},
            {**rect(140, 500, 300, 40), "type": "solid"},
            {**rect(440, 460, 100, 40), "type": "fake_floor"},
            {**rect(540, 460, 120, 40), "type": "solid"},
            {**rect(660, 500, 100, 40), "type": "hidden_spike", "triggerX": 690, "delay": 0.28},
            {**rect(760, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(860, 420, 140, 40), "type": "solid"},
            {**rect(1000, 420, 100, 40), "type": "fake_floor"},
            {**rect(1100, 420, 120, 40), "type": "solid"},
            {**rect(1220, 500, 100, 40), "type": "hidden_spike", "triggerX": 1250, "delay": 0.28},
            {**rect(1320, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(1420, 500, 400, 40), "type": "solid"},
            {**rect(1820, 460, 100, 40), "type": "fake_floor"},
            {**rect(1920, 460, 120, 40), "type": "solid"},
            {**rect(2040, 500, 100, 40), "type": "hidden_spike", "triggerX": 2070, "delay": 0.28},
            {**rect(2140, 500, 100, 40), "type": "crumble", "delay": 0.28},
            {**rect(2240, 420, 140, 40), "type": "solid"},
            {**rect(2380, 420, 100, 40), "type": "fake_floor"},
            {**rect(2480, 420, 120, 40), "type": "solid"},
            {**rect(2600, 500, 100, 40), "type": "hidden_spike", "triggerX": 2630, "delay": 0.28},
            {**rect(2700, 500, 600, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3400, 40), "type": "void"},
        ],
        "saws": [
            {"x": 290, "y": 470, "r": 20, "minX": 180, "maxX": 400, "speed": 280},
            {"x": 1500, "y": 470, "r": 20, "minX": 1460, "maxX": 1590, "speed": 280},
            {"x": 1750, "y": 470, "r": 20, "minX": 1700, "maxX": 1800, "speed": 300},
            {"x": 2800, "y": 470, "r": 22, "minX": 2740, "maxX": 2880, "speed": 290},
            {"x": 3050, "y": 470, "r": 22, "minX": 2980, "maxX": 3260, "speed": 320},
        ],
        "wallSpikes": [
            {"x": 600, "y": 390, "w": 24, "h": 70, "reach": 40, "triggerX": 570, "delay": 0.42, "dir": 1},
            {"x": 1160, "y": 350, "w": 24, "h": 70, "reach": 40, "triggerX": 1130, "delay": 0.42, "dir": 1},
            {"x": 1980, "y": 390, "w": 24, "h": 70, "reach": 40, "triggerX": 1950, "delay": 0.42, "dir": 1},
            {"x": 2540, "y": 350, "w": 24, "h": 70, "reach": 40, "triggerX": 2510, "delay": 0.42, "dir": 1},
            {"x": 3150, "y": 430, "w": 24, "h": 70, "reach": 40, "triggerX": 3120, "delay": 0.42, "dir": 1},
        ],
    },
]

# ---- Nivel 25-40: nuevos peligros — bloques que caen del cielo y aplastan,
# bombas (cielo y flanco) que explotan al contacto, bombas escondidas
# disfrazadas de suelo normal, tramos donde detenerse significa la muerte
# (el vacio de sombra te alcanza), y cadenas de teletransporte sobre huecos
# imposibles de saltar.
LEVELS += [
    {
        "name": "Nivel 25 - Algo cae del cielo",
        "hint": "Esa sombra en el suelo no es decorativa",
        "width": 2400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2320, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 700, 40), "type": "solid"},
            {**rect(700, 460, 200, 40), "type": "solid"},
            {**rect(900, 500, 700, 40), "type": "solid"},
            {**rect(1600, 460, 200, 40), "type": "solid"},
            {**rect(1800, 500, 600, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2500, 40), "type": "void"},
        ],
        "fallingBlocks": [
            {"x": 550, "y": -80, "w": 70, "h": 70, "triggerX": 420, "delay": 0.5, "groundY": 500},
            {"x": 1300, "y": -80, "w": 70, "h": 70, "triggerX": 1150, "delay": 0.5, "groundY": 500},
            {"x": 2000, "y": -80, "w": 80, "h": 80, "triggerX": 1850, "delay": 0.45, "groundY": 500},
        ],
    },
    {
        "name": "Nivel 26 - Lluvia de escombros",
        "hint": "Mira arriba de vez en cuando",
        "width": 2700,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2620, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 500, 40), "type": "solid"},
            {**rect(500, 460, 200, 40), "type": "solid"},
            {**rect(700, 500, 500, 40), "type": "solid"},
            {**rect(1200, 460, 200, 40), "type": "solid"},
            {**rect(1400, 500, 500, 40), "type": "solid"},
            {**rect(1900, 460, 200, 40), "type": "solid"},
            {**rect(2100, 500, 600, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2800, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1000, "y": 470, "r": 20, "minX": 950, "maxX": 1150, "speed": 200},
        ],
        "fallingBlocks": [
            {"x": 300, "y": -80, "w": 70, "h": 70, "triggerX": 150, "delay": 0.5, "groundY": 500},
            {"x": 850, "y": -80, "w": 70, "h": 70, "triggerX": 700, "delay": 0.5, "groundY": 500},
            {"x": 1600, "y": -80, "w": 70, "h": 70, "triggerX": 1450, "delay": 0.45, "groundY": 500},
            {"x": 2350, "y": -80, "w": 80, "h": 80, "triggerX": 2200, "delay": 0.45, "groundY": 500},
        ],
    },
    {
        "name": "Nivel 27 - Bombas del cielo",
        "hint": "Cuando veas la sombra, muevete",
        "width": 2500,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2420, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 600, 40), "type": "solid"},
            {**rect(600, 460, 200, 40), "type": "solid"},
            {**rect(800, 500, 600, 40), "type": "solid"},
            {**rect(1400, 460, 200, 40), "type": "solid"},
            {**rect(1600, 500, 900, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2600, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 400, "kind": "sky", "y": -80, "triggerX": 250, "delay": 0.5, "groundY": 500, "radius": 26, "blastRadius": 65},
            {"x": 1100, "kind": "sky", "y": -80, "triggerX": 950, "delay": 0.5, "groundY": 500, "radius": 26, "blastRadius": 65},
            {"x": 2000, "kind": "sky", "y": -80, "triggerX": 1850, "delay": 0.45, "groundY": 500, "radius": 28, "blastRadius": 70},
        ],
    },
    {
        "name": "Nivel 28 - Ataque por el flanco",
        "hint": "Vienen de costado, salta o corre",
        "width": 2600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 2600, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2700, 40), "type": "void"},
        ],
        "bombs": [
            {"kind": "side", "y": 495, "dir": 1, "fromX": 0, "toX": 1000, "triggerX": 400, "delay": 0.45, "speed": 280, "radius": 20},
            {"kind": "side", "y": 495, "dir": -1, "fromX": 1700, "toX": 700, "triggerX": 1100, "delay": 0.45, "speed": 300, "radius": 20},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1500, "toX": 2500, "triggerX": 1900, "delay": 0.4, "speed": 320, "radius": 22},
        ],
    },
    {
        "name": "Nivel 29 - Fuego cruzado",
        "hint": "Todo puede caer o venir de cualquier lado",
        "width": 2800,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2720, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 650, 40), "type": "solid"},
            {**rect(650, 500, 150, 40), "type": "hidden_spike", "triggerX": 680, "delay": 0.28},
            {**rect(800, 500, 700, 40), "type": "solid"},
            {**rect(1500, 460, 200, 40), "type": "solid"},
            {**rect(1700, 500, 1100, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2900, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 1150, "kind": "sky", "y": -80, "triggerX": 1000, "delay": 0.5, "groundY": 500, "radius": 26, "blastRadius": 65},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1550, "toX": 2450, "triggerX": 1900, "delay": 0.4, "speed": 300, "radius": 20},
            {"x": 2300, "kind": "sky", "y": -80, "triggerX": 2150, "delay": 0.45, "groundY": 500, "radius": 28, "blastRadius": 70},
            {"kind": "side", "y": 495, "dir": -1, "fromX": 2750, "toX": 2100, "triggerX": 2500, "delay": 0.4, "speed": 320, "radius": 22},
        ],
    },
    {
        "name": "Nivel 30 - Nada es lo que parece",
        "hint": "El suelo no dice si es bomba o piedra",
        "width": 2500,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2420, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 150, 40), "type": "hidden_bomb", "triggerX": 330, "delay": 0.3, "blastRadius": 70},
            {**rect(450, 500, 150, 40), "type": "solid"},
            {**rect(600, 500, 150, 40), "type": "hidden_spike", "triggerX": 630, "delay": 0.28},
            {**rect(750, 500, 350, 40), "type": "solid"},
            {**rect(1100, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1130, "delay": 0.3, "blastRadius": 70},
            {**rect(1250, 500, 350, 40), "type": "solid"},
            {**rect(1600, 500, 150, 40), "type": "hidden_spike", "triggerX": 1630, "delay": 0.28},
            {**rect(1750, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1780, "delay": 0.3, "blastRadius": 70},
            {**rect(1900, 500, 600, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2600, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 31 - Trampas mortales",
        "hint": "Ni el suelo ni el cielo son de fiar",
        "width": 2700,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2620, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 500, 40), "type": "solid"},
            {**rect(500, 500, 150, 40), "type": "hidden_bomb", "triggerX": 530, "delay": 0.3, "blastRadius": 70},
            {**rect(650, 460, 200, 40), "type": "solid"},
            {**rect(850, 500, 500, 40), "type": "solid"},
            {**rect(1350, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1380, "delay": 0.3, "blastRadius": 70},
            {**rect(1500, 460, 200, 40), "type": "solid"},
            {**rect(1700, 500, 1000, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2800, 40), "type": "void"},
        ],
        "fallingBlocks": [
            {"x": 1000, "y": -80, "w": 70, "h": 70, "triggerX": 870, "delay": 0.5, "groundY": 500},
            {"x": 2200, "y": -80, "w": 80, "h": 80, "triggerX": 2050, "delay": 0.45, "groundY": 500},
        ],
    },
    {
        "name": "Nivel 32 - Corre o desaparece",
        "hint": "No te detengas... o la oscuridad te alcanza",
        "width": 2200,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2120, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 2200, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2300, 40), "type": "void"},
        ],
        "saws": [
            {"x": 900, "y": 470, "r": 20, "minX": 820, "maxX": 1000, "speed": 200},
            {"x": 1600, "y": 470, "r": 20, "minX": 1520, "maxX": 1700, "speed": 220},
        ],
        "runWall": {"startX": -200, "speed": 150, "y": 0, "h": 620},
    },
    {
        "name": "Nivel 33 - Sin mirar atras",
        "hint": "El muro de sombra es mas rapido esta vez",
        "width": 2500,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2420, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 2500, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2600, 40), "type": "void"},
        ],
        "saws": [
            {"x": 850, "y": 470, "r": 20, "minX": 780, "maxX": 950, "speed": 220},
            {"x": 2050, "y": 470, "r": 20, "minX": 1980, "maxX": 2150, "speed": 240},
        ],
        "wallSpikes": [
            {"x": 1500, "y": 390, "w": 24, "h": 70, "reach": 40, "triggerX": 1470, "delay": 0.42, "dir": 1},
        ],
        "runWall": {"startX": -150, "speed": 165, "y": 0, "h": 620},
    },
    {
        "name": "Nivel 34 - Salto cuantico",
        "hint": "Un paso al vacio... o un atajo",
        "width": 1500,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1420, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "solid"},
            {**rect(900, 500, 600, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 1600, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 340, "y": 460, "w": 50, "h": 40, "toX": 950, "toY": 440},
        ],
    },
    {
        "name": "Nivel 35 - Cadena de portales",
        "hint": "Salta de portal en portal hasta el final",
        "width": 2400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2320, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(700, 500, 300, 40), "type": "solid"},
            {**rect(1400, 500, 300, 40), "type": "solid"},
            {**rect(2100, 500, 300, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2500, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 250, "y": 460, "w": 50, "h": 40, "toX": 720, "toY": 440},
            {"x": 950, "y": 460, "w": 50, "h": 40, "toX": 1420, "toY": 440},
            {"x": 1650, "y": 460, "w": 50, "h": 40, "toX": 2120, "toY": 440},
        ],
    },
    {
        "name": "Nivel 36 - Teletransporte y escombros",
        "hint": "El salto no es el unico peligro",
        "width": 2600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "solid"},
            {**rect(800, 500, 500, 40), "type": "solid"},
            {**rect(1600, 500, 350, 40), "type": "solid"},
            {**rect(2050, 500, 550, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2700, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 300, "y": 460, "w": 50, "h": 40, "toX": 850, "toY": 440},
            {"x": 1250, "y": 460, "w": 50, "h": 40, "toX": 1650, "toY": 440},
        ],
        "fallingBlocks": [
            {"x": 1050, "y": -80, "w": 70, "h": 70, "triggerX": 900, "delay": 0.55, "groundY": 500},
            {"x": 2300, "y": -80, "w": 80, "h": 80, "triggerX": 2150, "delay": 0.45, "groundY": 500},
        ],
    },
    {
        "name": "Nivel 37 - Bombas escondidas",
        "hint": "Ni las bombas ni las paredes avisan siempre",
        "width": 2700,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2620, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 500, 40), "type": "solid"},
            {**rect(500, 500, 150, 40), "type": "hidden_bomb", "triggerX": 530, "delay": 0.3, "blastRadius": 70},
            {**rect(650, 500, 650, 40), "type": "solid"},
            {**rect(1300, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1330, "delay": 0.3, "blastRadius": 70},
            {**rect(1450, 500, 1250, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2800, 40), "type": "void"},
        ],
        "bombs": [
            {"kind": "side", "y": 495, "dir": 1, "fromX": 700, "toX": 1200, "triggerX": 900, "delay": 0.4, "speed": 280, "radius": 20},
            {"kind": "side", "y": 495, "dir": -1, "fromX": 2300, "toX": 1700, "triggerX": 2000, "delay": 0.4, "speed": 300, "radius": 22},
        ],
        "wallSpikes": [
            {"x": 1630, "y": 390, "w": 24, "h": 70, "reach": 40, "triggerX": 1600, "delay": 0.42, "dir": 1},
        ],
    },
    {
        "name": "Nivel 38 - Corre entre explosiones",
        "hint": "No frenes, ni siquiera para esquivar",
        "width": 2400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2320, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 2400, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2500, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 700, "kind": "sky", "y": -80, "triggerX": 550, "delay": 0.5, "groundY": 500, "radius": 24, "blastRadius": 60},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1200, "toX": 1700, "triggerX": 1400, "delay": 0.4, "speed": 300, "radius": 20},
            {"x": 2000, "kind": "sky", "y": -80, "triggerX": 1850, "delay": 0.45, "groundY": 500, "radius": 26, "blastRadius": 65},
        ],
        "runWall": {"startX": -200, "speed": 160, "y": 0, "h": 620},
    },
    {
        "name": "Nivel 39 - El combo",
        "hint": "Todo a la vez: portal, sierra, bomba y bloque",
        "width": 2900,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2820, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "solid"},
            {**rect(850, 500, 700, 40), "type": "solid"},
            {**rect(1550, 460, 200, 40), "type": "solid"},
            {**rect(1750, 500, 1150, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3000, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 350, "y": 460, "w": 50, "h": 40, "toX": 900, "toY": 440},
        ],
        "fallingBlocks": [
            {"x": 1200, "y": -80, "w": 70, "h": 70, "triggerX": 1050, "delay": 0.5, "groundY": 500},
        ],
        "saws": [
            {"x": 1300, "y": 470, "r": 20, "minX": 1250, "maxX": 1420, "speed": 220},
        ],
        "bombs": [
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1700, "toX": 2200, "triggerX": 1850, "delay": 0.4, "speed": 280, "radius": 20},
            {"x": 2300, "kind": "sky", "y": -80, "triggerX": 2150, "delay": 0.45, "groundY": 500, "radius": 26, "blastRadius": 65},
        ],
    },
    {
        "name": "Nivel 40 - Ultimatum definitivo",
        "hint": "Corre, esquiva, salta y no confies en nada",
        "width": 3000,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2920, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 500, 40), "type": "solid"},
            {**rect(900, 500, 600, 40), "type": "solid"},
            {**rect(1500, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1530, "delay": 0.3, "blastRadius": 70},
            {**rect(1650, 500, 1350, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3100, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 450, "y": 460, "w": 50, "h": 40, "toX": 950, "toY": 440},
        ],
        "fallingBlocks": [
            {"x": 1200, "y": -80, "w": 70, "h": 70, "triggerX": 1050, "delay": 0.5, "groundY": 500},
            {"x": 2400, "y": -80, "w": 80, "h": 80, "triggerX": 2250, "delay": 0.45, "groundY": 500},
        ],
        "bombs": [
            {"x": 1900, "kind": "sky", "y": -80, "triggerX": 1750, "delay": 0.5, "groundY": 500, "radius": 26, "blastRadius": 65},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 2500, "toX": 3000, "triggerX": 2700, "delay": 0.4, "speed": 300, "radius": 22},
        ],
        "runWall": {"startX": -250, "speed": 140, "y": 0, "h": 620},
    },
]

# Placeholder slots shown on the map as locked "Proximamente" nodes so the
# trail keeps going, but with no real content behind them yet — they 403
# if requested directly (see get_level) and never count toward
# playable_level_count(), so progress/unlock logic ignores them entirely.
LEVELS += [
    {
        "name": f"Nivel {i}",
        "hint": "",
        "locked": True,
        "width": 100,
        "spawn": {"x": 0, "y": 0},
        "goal": rect(0, 0, 0, 0),
        "platforms": [],
        "hazards": [],
    }
    for i in range(41, 61)
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
    for block in level.get("fallingBlocks", []):
        block["y"] -= GROUND_LIFT
        block["groundY"] -= GROUND_LIFT
    for bomb in level.get("bombs", []):
        bomb["y"] -= GROUND_LIFT
        if "groundY" in bomb:
            bomb["groundY"] -= GROUND_LIFT
    for tp in level.get("teleporters", []):
        tp["y"] -= GROUND_LIFT
        tp["toY"] -= GROUND_LIFT
    if level.get("runWall"):
        level["runWall"]["y"] -= GROUND_LIFT
    return level


def level_count() -> int:
    return len(LEVELS)


def playable_level_count() -> int:
    return sum(1 for lvl in LEVELS if not lvl.get("locked"))


def level_meta() -> list[dict]:
    return [
        {
            "index": i,
            "name": lvl["name"],
            "hint": lvl.get("hint", ""),
            "locked": bool(lvl.get("locked")),
        }
        for i, lvl in enumerate(LEVELS)
    ]
