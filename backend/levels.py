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
            {**rect(420, 460, 120, 40), "type": "solid"},
            {**rect(540, 460, 160, 40), "type": "solid"},
            {**rect(700, 500, 140, 40), "type": "hidden_spike", "triggerX": 730, "delay": 0.32},
            {**rect(840, 500, 140, 40), "type": "crumble", "delay": 0.32},
            {**rect(980, 500, 140, 40), "type": "solid"},
            {**rect(1120, 500, 140, 40), "type": "hidden_spike", "triggerX": 1150, "delay": 0.32},
            {**rect(1260, 500, 300, 40), "type": "solid"},
            {**rect(1560, 460, 120, 40), "type": "fake_floor"},
            {**rect(1680, 460, 140, 40), "type": "solid"},
            {**rect(1820, 500, 140, 40), "type": "hidden_spike", "triggerX": 1850, "delay": 0.32},
            {**rect(1960, 500, 340, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2400, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1400, "y": 470, "r": 22, "minX": 1300, "maxX": 1520, "speed": 190},
            {"x": 2130, "y": 470, "r": 20, "minX": 2000, "maxX": 2280, "speed": 220},
        ],
        "wallSpikes": [
            {"x": 340, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 300, "delay": 0.36, "dir": 1},
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
            {**rect(240, 500, 120, 40), "type": "crumble", "delay": 0.329},
            {**rect(360, 500, 120, 40), "type": "crumble", "delay": 0.329},
            {**rect(480, 500, 120, 40), "type": "hidden_spike", "triggerX": 510, "delay": 0.329},
            {**rect(600, 460, 160, 40), "type": "solid"},
            {**rect(760, 460, 120, 40), "type": "hidden_spike", "triggerX": 790, "delay": 0.329},
            {**rect(880, 460, 120, 40), "type": "fake_floor"},
            {**rect(1000, 500, 360, 40), "type": "solid"},
            {**rect(1360, 500, 140, 40), "type": "crumble", "delay": 0.329},
            {**rect(1500, 460, 140, 40), "type": "fake_floor"},
            {**rect(1640, 460, 160, 40), "type": "solid"},
            {**rect(1800, 500, 140, 40), "type": "hidden_spike", "triggerX": 1830, "delay": 0.329},
            {**rect(1940, 500, 510, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2600, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1080, "y": 470, "r": 16, "minX": 1020, "maxX": 1180, "speed": 182},
            {"x": 1280, "y": 470, "r": 16, "minX": 1200, "maxX": 1340, "speed": 198},
            {"x": 2200, "y": 470, "r": 18, "minX": 2000, "maxX": 2400, "speed": 214},
        ],
        "wallSpikes": [
            {"x": 680, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 650, "delay": 0.352, "dir": 1},
            {"x": 2300, "y": 430, "w": 24, "h": 70, "reach": 45, "triggerX": 2270, "delay": 0.352, "dir": 1},
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
            {**rect(660, 500, 120, 40), "type": "hidden_spike", "triggerX": 690, "delay": 0.329},
            {**rect(780, 500, 120, 40), "type": "crumble", "delay": 0.329},
            {**rect(900, 500, 120, 40), "type": "hidden_spike", "triggerX": 930, "delay": 0.329},
            {**rect(1020, 500, 120, 40), "type": "crumble", "delay": 0.329},
            {**rect(1140, 500, 360, 40), "type": "solid"},
            {**rect(1500, 460, 120, 40), "type": "fake_floor"},
            {**rect(1620, 460, 140, 40), "type": "solid"},
            {**rect(1760, 500, 120, 40), "type": "hidden_spike", "triggerX": 1790, "delay": 0.329},
            {**rect(1880, 500, 120, 40), "type": "crumble", "delay": 0.329},
            {**rect(2000, 460, 160, 40), "type": "solid"},
            {**rect(2160, 500, 440, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2650, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1220, "y": 470, "r": 16, "minX": 1160, "maxX": 1320, "speed": 190},
            {"x": 1420, "y": 470, "r": 16, "minX": 1340, "maxX": 1480, "speed": 206},
            {"x": 2380, "y": 470, "r": 20, "minX": 2200, "maxX": 2560, "speed": 231},
        ],
        "wallSpikes": [
            {"x": 300, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 270, "delay": 0.352, "dir": 1},
            {"x": 2080, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 2050, "delay": 0.352, "dir": 1},
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
            {**rect(460, 500, 100, 40), "type": "hidden_spike", "triggerX": 490, "delay": 0.329},
            {**rect(560, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(660, 460, 140, 40), "type": "solid"},
            {**rect(800, 460, 100, 40), "type": "hidden_spike", "triggerX": 830, "delay": 0.329},
            {**rect(900, 460, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1000, 500, 340, 40), "type": "solid"},
            {**rect(1340, 460, 100, 40), "type": "fake_floor"},
            {**rect(1440, 460, 140, 40), "type": "solid"},
            {**rect(1580, 500, 100, 40), "type": "hidden_spike", "triggerX": 1610, "delay": 0.329},
            {**rect(1680, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1780, 420, 160, 40), "type": "solid"},
            {**rect(1940, 420, 100, 40), "type": "fake_floor"},
            {**rect(2040, 420, 160, 40), "type": "solid"},
            {**rect(2200, 500, 500, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2800, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1100, "y": 470, "r": 16, "minX": 1040, "maxX": 1200, "speed": 198},
            {"x": 1260, "y": 470, "r": 16, "minX": 1180, "maxX": 1320, "speed": 214},
            {"x": 2450, "y": 470, "r": 20, "minX": 2240, "maxX": 2660, "speed": 231},
        ],
        "wallSpikes": [
            {"x": 740, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 710, "delay": 0.352, "dir": 1},
            {"x": 1520, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 1490, "delay": 0.352, "dir": 1},
            {"x": 2120, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 2090, "delay": 0.352, "dir": 1},
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
            {**rect(200, 500, 100, 40), "type": "hidden_spike", "triggerX": 230, "delay": 0.329},
            {**rect(300, 500, 100, 40), "type": "hidden_spike", "triggerX": 330, "delay": 0.329},
            {**rect(400, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(500, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(600, 460, 140, 40), "type": "solid"},
            {**rect(740, 460, 100, 40), "type": "fake_floor"},
            {**rect(840, 460, 120, 40), "type": "solid"},
            {**rect(960, 500, 100, 40), "type": "hidden_spike", "triggerX": 990, "delay": 0.329},
            {**rect(1060, 500, 380, 40), "type": "solid"},
            {**rect(1440, 460, 100, 40), "type": "fake_floor"},
            {**rect(1540, 460, 120, 40), "type": "solid"},
            {**rect(1660, 500, 100, 40), "type": "hidden_spike", "triggerX": 1690, "delay": 0.329},
            {**rect(1760, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1860, 420, 140, 40), "type": "solid"},
            {**rect(2000, 420, 100, 40), "type": "fake_floor"},
            {**rect(2100, 420, 120, 40), "type": "solid"},
            {**rect(2220, 500, 100, 40), "type": "hidden_spike", "triggerX": 2250, "delay": 0.329},
            {**rect(2320, 500, 480, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2900, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1150, "y": 470, "r": 16, "minX": 1090, "maxX": 1250, "speed": 206},
            {"x": 1330, "y": 470, "r": 16, "minX": 1260, "maxX": 1410, "speed": 223},
            {"x": 2500, "y": 470, "r": 18, "minX": 2350, "maxX": 2550, "speed": 214},
            {"x": 2650, "y": 470, "r": 16, "minX": 2580, "maxX": 2770, "speed": 239},
        ],
        "wallSpikes": [
            {"x": 680, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 650, "delay": 0.352, "dir": 1},
            {"x": 1600, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 1570, "delay": 0.352, "dir": 1},
            {"x": 2160, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 2130, "delay": 0.352, "dir": 1},
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
            {**rect(180, 460, 100, 40), "type": "hidden_spike", "triggerX": 210, "delay": 0.329},
            {**rect(280, 500, 100, 40), "type": "solid"},
            {**rect(380, 460, 120, 40), "type": "crumble", "delay": 0.329},
            {**rect(500, 500, 100, 40), "type": "solid"},
            {**rect(600, 460, 120, 40), "type": "solid"},
            {**rect(720, 500, 100, 40), "type": "hidden_spike", "triggerX": 750, "delay": 0.329},
            {**rect(820, 460, 100, 40), "type": "fake_floor"},
            {**rect(920, 500, 400, 40), "type": "solid"},
            {**rect(1320, 460, 100, 40), "type": "fake_floor"},
            {**rect(1420, 460, 120, 40), "type": "solid"},
            {**rect(1540, 500, 100, 40), "type": "hidden_spike", "triggerX": 1570, "delay": 0.329},
            {**rect(1640, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1740, 420, 140, 40), "type": "solid"},
            {**rect(1880, 420, 100, 40), "type": "fake_floor"},
            {**rect(1980, 420, 120, 40), "type": "solid"},
            {**rect(2100, 500, 100, 40), "type": "hidden_spike", "triggerX": 2130, "delay": 0.329},
            {**rect(2200, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(2300, 500, 380, 40), "type": "solid"},
            {**rect(2680, 460, 100, 40), "type": "fake_floor"},
            {**rect(2780, 460, 100, 40), "type": "solid"},
            {**rect(2880, 500, 120, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3100, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1000, "y": 470, "r": 16, "minX": 940, "maxX": 1100, "speed": 206},
            {"x": 1200, "y": 470, "r": 16, "minX": 1120, "maxX": 1300, "speed": 223},
            {"x": 2400, "y": 470, "r": 18, "minX": 2320, "maxX": 2480, "speed": 214},
            {"x": 2560, "y": 470, "r": 16, "minX": 2500, "maxX": 2660, "speed": 231},
        ],
        "wallSpikes": [
            {"x": 680, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 650, "delay": 0.352, "dir": 1},
            {"x": 1500, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 1470, "delay": 0.352, "dir": 1},
            {"x": 2060, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 2030, "delay": 0.352, "dir": 1},
            {"x": 2860, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 2830, "delay": 0.352, "dir": 1},
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
            {**rect(840, 500, 100, 40), "type": "hidden_spike", "triggerX": 870, "delay": 0.329},
            {**rect(940, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1040, 500, 100, 40), "type": "hidden_spike", "triggerX": 1070, "delay": 0.329},
            {**rect(1140, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1240, 500, 100, 40), "type": "solid"},
            {**rect(1340, 500, 400, 40), "type": "solid"},
            {**rect(1740, 460, 100, 40), "type": "fake_floor"},
            {**rect(1840, 460, 100, 40), "type": "solid"},
            {**rect(1940, 500, 100, 40), "type": "hidden_spike", "triggerX": 1970, "delay": 0.329},
            {**rect(2040, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(2140, 420, 140, 40), "type": "solid"},
            {**rect(2280, 420, 100, 40), "type": "fake_floor"},
            {**rect(2380, 420, 100, 40), "type": "solid"},
            {**rect(2480, 500, 420, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3000, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1440, "y": 470, "r": 16, "minX": 1380, "maxX": 1540, "speed": 214},
            {"x": 1620, "y": 470, "r": 16, "minX": 1560, "maxX": 1700, "speed": 231},
            {"x": 2620, "y": 470, "r": 18, "minX": 2520, "maxX": 2680, "speed": 223},
            {"x": 2780, "y": 470, "r": 16, "minX": 2700, "maxX": 2860, "speed": 248},
        ],
        "wallSpikes": [
            {"x": 370, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 340, "delay": 0.352, "dir": 1},
            {"x": 690, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 660, "delay": 0.352, "dir": 1},
            {"x": 1900, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 1870, "delay": 0.352, "dir": 1},
            {"x": 2440, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 2410, "delay": 0.352, "dir": 1},
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
            {**rect(180, 500, 90, 40), "type": "crumble", "delay": 0.329},
            {**rect(270, 500, 90, 40), "type": "crumble", "delay": 0.329},
            {**rect(360, 500, 110, 40), "type": "crumble", "delay": 0.329},
            {**rect(470, 460, 90, 40), "type": "solid"},
            {**rect(560, 460, 100, 40), "type": "solid"},
            {**rect(660, 420, 110, 40), "type": "fake_floor"},
            {**rect(770, 420, 90, 40), "type": "solid"},
            {**rect(860, 420, 100, 40), "type": "solid"},
            {**rect(960, 500, 90, 40), "type": "hidden_spike", "triggerX": 985, "delay": 0.329},
            {**rect(1050, 500, 90, 40), "type": "hidden_spike", "triggerX": 1075, "delay": 0.329},
            {**rect(1140, 500, 420, 40), "type": "solid"},
            {**rect(1560, 460, 90, 40), "type": "fake_floor"},
            {**rect(1650, 460, 100, 40), "type": "solid"},
            {**rect(1750, 500, 90, 40), "type": "hidden_spike", "triggerX": 1775, "delay": 0.329},
            {**rect(1840, 500, 90, 40), "type": "crumble", "delay": 0.329},
            {**rect(1930, 420, 120, 40), "type": "solid"},
            {**rect(2050, 420, 90, 40), "type": "fake_floor"},
            {**rect(2140, 420, 100, 40), "type": "solid"},
            {**rect(2240, 500, 90, 40), "type": "hidden_spike", "triggerX": 2265, "delay": 0.329},
            {**rect(2330, 500, 720, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3150, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1260, "y": 470, "r": 16, "minX": 1200, "maxX": 1360, "speed": 223},
            {"x": 1440, "y": 470, "r": 16, "minX": 1380, "maxX": 1540, "speed": 239},
            {"x": 2600, "y": 470, "r": 18, "minX": 2400, "maxX": 2700, "speed": 223},
            {"x": 2850, "y": 470, "r": 16, "minX": 2750, "maxX": 3020, "speed": 248},
        ],
        "wallSpikes": [
            {"x": 610, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 580, "delay": 0.352, "dir": 1},
            {"x": 910, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 880, "delay": 0.352, "dir": 1},
            {"x": 1700, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 1670, "delay": 0.352, "dir": 1},
            {"x": 2190, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 2160, "delay": 0.352, "dir": 1},
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
            {**rect(180, 500, 90, 40), "type": "hidden_spike", "triggerX": 205, "delay": 0.329},
            {**rect(270, 460, 110, 40), "type": "solid"},
            {**rect(380, 460, 100, 40), "type": "solid"},
            {**rect(480, 460, 90, 40), "type": "hidden_spike", "triggerX": 505, "delay": 0.329},
            {**rect(570, 420, 110, 40), "type": "solid"},
            {**rect(680, 420, 100, 40), "type": "solid"},
            {**rect(780, 420, 90, 40), "type": "crumble", "delay": 0.329},
            {**rect(870, 460, 90, 40), "type": "fake_floor"},
            {**rect(960, 460, 100, 40), "type": "fake_floor"},
            {**rect(1060, 500, 90, 40), "type": "hidden_spike", "triggerX": 1085, "delay": 0.329},
            {**rect(1150, 500, 80, 40), "type": "crumble", "delay": 0.329},
            {**rect(1230, 500, 420, 40), "type": "solid"},
            {**rect(1650, 460, 90, 40), "type": "fake_floor"},
            {**rect(1740, 460, 100, 40), "type": "solid"},
            {**rect(1840, 500, 90, 40), "type": "hidden_spike", "triggerX": 1865, "delay": 0.329},
            {**rect(1930, 500, 90, 40), "type": "crumble", "delay": 0.329},
            {**rect(2020, 420, 130, 40), "type": "solid"},
            {**rect(2150, 420, 90, 40), "type": "fake_floor"},
            {**rect(2240, 420, 100, 40), "type": "solid"},
            {**rect(2340, 500, 90, 40), "type": "hidden_spike", "triggerX": 2365, "delay": 0.329},
            {**rect(2430, 500, 90, 40), "type": "crumble", "delay": 0.329},
            {**rect(2520, 500, 680, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3300, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1350, "y": 470, "r": 16, "minX": 1290, "maxX": 1450, "speed": 223},
            {"x": 1520, "y": 470, "r": 16, "minX": 1460, "maxX": 1610, "speed": 239},
            {"x": 2650, "y": 470, "r": 16, "minX": 2570, "maxX": 2730, "speed": 223},
            {"x": 2850, "y": 470, "r": 16, "minX": 2770, "maxX": 2930, "speed": 239},
            {"x": 3050, "y": 470, "r": 18, "minX": 2960, "maxX": 3160, "speed": 256},
        ],
        "wallSpikes": [
            {"x": 320, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 290, "delay": 0.352, "dir": 1},
            {"x": 620, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 590, "delay": 0.352, "dir": 1},
            {"x": 1790, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 1760, "delay": 0.352, "dir": 1},
            {"x": 2290, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 2260, "delay": 0.352, "dir": 1},
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
            {**rect(720, 500, 100, 40), "type": "hidden_spike", "triggerX": 750, "delay": 0.329},
            {**rect(820, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(920, 420, 140, 40), "type": "solid"},
            {**rect(1060, 420, 100, 40), "type": "fake_floor"},
            {**rect(1160, 420, 120, 40), "type": "solid"},
            {**rect(1280, 500, 100, 40), "type": "hidden_spike", "triggerX": 1310, "delay": 0.329},
            {**rect(1380, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1480, 500, 420, 40), "type": "solid"},
            {**rect(1900, 460, 100, 40), "type": "fake_floor"},
            {**rect(2000, 460, 120, 40), "type": "solid"},
            {**rect(2120, 500, 100, 40), "type": "hidden_spike", "triggerX": 2150, "delay": 0.329},
            {**rect(2220, 500, 680, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3000, 40), "type": "void"},
        ],
        "saws": [
            {"x": 330, "y": 470, "r": 16, "minX": 200, "maxX": 460, "speed": 214},
            {"x": 1650, "y": 470, "r": 16, "minX": 1540, "maxX": 1740, "speed": 231},
            {"x": 1800, "y": 470, "r": 16, "minX": 1720, "maxX": 1860, "speed": 248},
            {"x": 2600, "y": 470, "r": 20, "minX": 2280, "maxX": 2860, "speed": 256},
        ],
        "wallSpikes": [
            {"x": 660, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 630, "delay": 0.352, "dir": 1},
            {"x": 1220, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 1190, "delay": 0.352, "dir": 1},
            {"x": 2060, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 2030, "delay": 0.352, "dir": 1},
            {"x": 2750, "y": 430, "w": 24, "h": 70, "reach": 45, "triggerX": 2720, "delay": 0.352, "dir": 1},
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
            {**rect(600, 500, 100, 40), "type": "hidden_spike", "triggerX": 630, "delay": 0.329},
            {**rect(700, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(800, 500, 100, 40), "type": "hidden_spike", "triggerX": 830, "delay": 0.329},
            {**rect(900, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1000, 500, 400, 40), "type": "solid"},
            {**rect(1400, 460, 100, 40), "type": "fake_floor"},
            {**rect(1500, 460, 120, 40), "type": "solid"},
            {**rect(1620, 500, 100, 40), "type": "hidden_spike", "triggerX": 1650, "delay": 0.329},
            {**rect(1720, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1820, 420, 140, 40), "type": "solid"},
            {**rect(1960, 420, 100, 40), "type": "fake_floor"},
            {**rect(2060, 420, 120, 40), "type": "solid"},
            {**rect(2180, 500, 100, 40), "type": "hidden_spike", "triggerX": 2210, "delay": 0.329},
            {**rect(2280, 500, 720, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3100, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1150, "y": 470, "r": 16, "minX": 1080, "maxX": 1240, "speed": 223},
            {"x": 1300, "y": 470, "r": 16, "minX": 1240, "maxX": 1380, "speed": 239},
            {"x": 2550, "y": 470, "r": 18, "minX": 2350, "maxX": 2600, "speed": 231},
            {"x": 2800, "y": 470, "r": 16, "minX": 2650, "maxX": 2980, "speed": 256},
        ],
        "wallSpikes": [
            {"x": 220, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 190, "delay": 0.352, "dir": 1},
            {"x": 440, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 410, "delay": 0.352, "dir": 1},
            {"x": 1560, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 1530, "delay": 0.352, "dir": 1},
            {"x": 2120, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 2090, "delay": 0.352, "dir": 1},
        ],
    },
    {
        "name": "Nivel 22 - Cae o corre",
        "hint": "El suelo bajo tus pies ya cruje",
        "width": 2950,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2870, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 160, 40), "type": "crumble", "delay": 0.329},
            {**rect(160, 500, 140, 40), "type": "solid"},
            {**rect(300, 500, 100, 40), "type": "hidden_spike", "triggerX": 330, "delay": 0.329},
            {**rect(400, 460, 120, 40), "type": "solid"},
            {**rect(520, 460, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(620, 460, 100, 40), "type": "fake_floor"},
            {**rect(720, 500, 100, 40), "type": "hidden_spike", "triggerX": 750, "delay": 0.329},
            {**rect(820, 500, 380, 40), "type": "solid"},
            {**rect(1200, 420, 100, 40), "type": "fake_floor"},
            {**rect(1300, 420, 120, 40), "type": "solid"},
            {**rect(1420, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1520, 500, 100, 40), "type": "hidden_spike", "triggerX": 1550, "delay": 0.329},
            {**rect(1620, 460, 140, 40), "type": "solid"},
            {**rect(1760, 460, 100, 40), "type": "fake_floor"},
            {**rect(1860, 500, 100, 40), "type": "hidden_spike", "triggerX": 1890, "delay": 0.329},
            {**rect(1960, 500, 990, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3050, 40), "type": "void"},
        ],
        "saws": [
            {"x": 950, "y": 470, "r": 16, "minX": 900, "maxX": 1060, "speed": 223},
            {"x": 1120, "y": 470, "r": 16, "minX": 1060, "maxX": 1180, "speed": 239},
            {"x": 2500, "y": 470, "r": 18, "minX": 2100, "maxX": 2500, "speed": 231},
            {"x": 2750, "y": 470, "r": 18, "minX": 2600, "maxX": 2900, "speed": 256},
        ],
        "wallSpikes": [
            {"x": 460, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 430, "delay": 0.352, "dir": 1},
            {"x": 1360, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 1330, "delay": 0.352, "dir": 1},
            {"x": 1690, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 1660, "delay": 0.352, "dir": 1},
            {"x": 2200, "y": 430, "w": 24, "h": 70, "reach": 45, "triggerX": 2170, "delay": 0.352, "dir": 1},
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
            {**rect(1320, 500, 100, 40), "type": "hidden_spike", "triggerX": 1350, "delay": 0.329},
            {**rect(1420, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1520, 460, 100, 40), "type": "fake_floor"},
            {**rect(1620, 460, 100, 40), "type": "hidden_spike", "triggerX": 1650, "delay": 0.329},
            {**rect(1720, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1820, 500, 500, 40), "type": "solid"},
            {**rect(2320, 420, 100, 40), "type": "fake_floor"},
            {**rect(2420, 420, 120, 40), "type": "solid"},
            {**rect(2540, 500, 100, 40), "type": "hidden_spike", "triggerX": 2570, "delay": 0.329},
            {**rect(2640, 500, 580, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3320, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1020, "y": 470, "r": 16, "minX": 960, "maxX": 1120, "speed": 231},
            {"x": 1220, "y": 470, "r": 16, "minX": 1140, "maxX": 1300, "speed": 248},
            {"x": 2020, "y": 470, "r": 18, "minX": 1860, "maxX": 2080, "speed": 231},
            {"x": 2220, "y": 470, "r": 18, "minX": 2140, "maxX": 2300, "speed": 248},
            {"x": 2920, "y": 470, "r": 16, "minX": 2680, "maxX": 3200, "speed": 264},
        ],
        "wallSpikes": [
            {"x": 210, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 180, "delay": 0.447, "dir": 1},
            {"x": 430, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 400, "delay": 0.447, "dir": 1},
            {"x": 650, "y": 390, "w": 24, "h": 70, "reach": 45, "triggerX": 620, "delay": 0.447, "dir": 1},
            {"x": 870, "y": 430, "w": 24, "h": 70, "reach": 45, "triggerX": 840, "delay": 0.447, "dir": 1},
            {"x": 2480, "y": 350, "w": 24, "h": 70, "reach": 45, "triggerX": 2450, "delay": 0.447, "dir": 1},
            {"x": 3070, "y": 430, "w": 24, "h": 70, "reach": 45, "triggerX": 3040, "delay": 0.447, "dir": 1},
        ],
    },
    {
        "name": "Nivel 24 - Corre o cae",
        "hint": "El final de este tramo... por ahora",
        "width": 3300,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3220, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 140, 40), "type": "crumble", "delay": 0.329},
            {**rect(140, 500, 300, 40), "type": "solid"},
            {**rect(440, 460, 100, 40), "type": "fake_floor"},
            {**rect(540, 460, 120, 40), "type": "solid"},
            {**rect(660, 500, 100, 40), "type": "hidden_spike", "triggerX": 690, "delay": 0.329},
            {**rect(760, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(860, 420, 140, 40), "type": "solid"},
            {**rect(1000, 420, 100, 40), "type": "fake_floor"},
            {**rect(1100, 420, 120, 40), "type": "solid"},
            {**rect(1220, 500, 100, 40), "type": "hidden_spike", "triggerX": 1250, "delay": 0.329},
            {**rect(1320, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(1420, 500, 400, 40), "type": "solid"},
            {**rect(1820, 460, 100, 40), "type": "fake_floor"},
            {**rect(1920, 460, 120, 40), "type": "solid"},
            {**rect(2040, 500, 100, 40), "type": "hidden_spike", "triggerX": 2070, "delay": 0.329},
            {**rect(2140, 500, 100, 40), "type": "crumble", "delay": 0.329},
            {**rect(2240, 420, 140, 40), "type": "solid"},
            {**rect(2380, 420, 100, 40), "type": "fake_floor"},
            {**rect(2480, 420, 120, 40), "type": "solid"},
            {**rect(2600, 500, 100, 40), "type": "hidden_spike", "triggerX": 2630, "delay": 0.329},
            {**rect(2700, 500, 600, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3400, 40), "type": "void"},
        ],
        "saws": [
            {"x": 290, "y": 470, "r": 16, "minX": 180, "maxX": 400, "speed": 231},
            {"x": 1500, "y": 470, "r": 16, "minX": 1460, "maxX": 1590, "speed": 231},
            {"x": 1750, "y": 470, "r": 16, "minX": 1700, "maxX": 1800, "speed": 248},
            {"x": 2800, "y": 470, "r": 18, "minX": 2740, "maxX": 2880, "speed": 239},
            {"x": 3050, "y": 470, "r": 18, "minX": 2980, "maxX": 3260, "speed": 264},
        ],
        "wallSpikes": [
            {"x": 600, "y": 390, "w": 24, "h": 70, "reach": 33, "triggerX": 570, "delay": 0.493, "dir": 1},
            {"x": 1160, "y": 350, "w": 24, "h": 70, "reach": 33, "triggerX": 1130, "delay": 0.493, "dir": 1},
            {"x": 1980, "y": 390, "w": 24, "h": 70, "reach": 33, "triggerX": 1950, "delay": 0.493, "dir": 1},
            {"x": 2540, "y": 350, "w": 24, "h": 70, "reach": 33, "triggerX": 2510, "delay": 0.493, "dir": 1},
            {"x": 3150, "y": 430, "w": 24, "h": 70, "reach": 33, "triggerX": 3120, "delay": 0.493, "dir": 1},
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
            {"x": 550, "y": -80, "w": 70, "h": 70, "triggerX": 420, "delay": 0.588, "groundY": 500},
            {"x": 1300, "y": -80, "w": 70, "h": 70, "triggerX": 1150, "delay": 0.588, "groundY": 500},
            {"x": 2000, "y": -80, "w": 80, "h": 80, "triggerX": 1850, "delay": 0.529, "groundY": 500},
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
            {"x": 1000, "y": 470, "r": 16, "minX": 950, "maxX": 1150, "speed": 165},
        ],
        "fallingBlocks": [
            {"x": 300, "y": -80, "w": 70, "h": 70, "triggerX": 150, "delay": 0.588, "groundY": 500},
            {"x": 850, "y": -80, "w": 70, "h": 70, "triggerX": 700, "delay": 0.588, "groundY": 500},
            {"x": 1600, "y": -80, "w": 70, "h": 70, "triggerX": 1450, "delay": 0.529, "groundY": 500},
            {"x": 2350, "y": -80, "w": 80, "h": 80, "triggerX": 2200, "delay": 0.529, "groundY": 500},
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
            {"x": 400, "kind": "sky", "y": -80, "triggerX": 250, "delay": 0.588, "groundY": 500, "radius": 21, "blastRadius": 54},
            {"x": 1100, "kind": "sky", "y": -80, "triggerX": 950, "delay": 0.588, "groundY": 500, "radius": 21, "blastRadius": 54},
            {"x": 2000, "kind": "sky", "y": -80, "triggerX": 1850, "delay": 0.529, "groundY": 500, "radius": 23, "blastRadius": 58},
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
            {"kind": "side", "y": 495, "dir": 1, "fromX": 0, "toX": 1000, "triggerX": 400, "delay": 0.529, "speed": 231, "radius": 16},
            {"kind": "side", "y": 495, "dir": -1, "fromX": 1700, "toX": 700, "triggerX": 1100, "delay": 0.529, "speed": 248, "radius": 16},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1500, "toX": 2500, "triggerX": 1900, "delay": 0.47, "speed": 264, "radius": 18},
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
            {**rect(650, 500, 150, 40), "type": "hidden_spike", "triggerX": 680, "delay": 0.329},
            {**rect(800, 500, 700, 40), "type": "solid"},
            {**rect(1500, 460, 200, 40), "type": "solid"},
            {**rect(1700, 500, 1100, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2900, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 1150, "kind": "sky", "y": -80, "triggerX": 1000, "delay": 0.588, "groundY": 500, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1550, "toX": 2450, "triggerX": 1900, "delay": 0.47, "speed": 248, "radius": 16},
            {"x": 2300, "kind": "sky", "y": -80, "triggerX": 2150, "delay": 0.529, "groundY": 500, "radius": 23, "blastRadius": 58},
            {"kind": "side", "y": 495, "dir": -1, "fromX": 2750, "toX": 2100, "triggerX": 2500, "delay": 0.47, "speed": 264, "radius": 18},
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
            {**rect(300, 500, 150, 40), "type": "hidden_bomb", "triggerX": 330, "delay": 0.352, "blastRadius": 58},
            {**rect(450, 500, 150, 40), "type": "solid"},
            {**rect(600, 500, 150, 40), "type": "hidden_spike", "triggerX": 630, "delay": 0.329},
            {**rect(750, 500, 350, 40), "type": "solid"},
            {**rect(1100, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1130, "delay": 0.352, "blastRadius": 58},
            {**rect(1250, 500, 350, 40), "type": "solid"},
            {**rect(1600, 500, 150, 40), "type": "hidden_spike", "triggerX": 1630, "delay": 0.329},
            {**rect(1750, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1780, "delay": 0.352, "blastRadius": 58},
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
            {**rect(500, 500, 150, 40), "type": "hidden_bomb", "triggerX": 530, "delay": 0.352, "blastRadius": 58},
            {**rect(650, 460, 200, 40), "type": "solid"},
            {**rect(850, 500, 500, 40), "type": "solid"},
            {**rect(1350, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1380, "delay": 0.352, "blastRadius": 58},
            {**rect(1500, 460, 200, 40), "type": "solid"},
            {**rect(1700, 500, 1000, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2800, 40), "type": "void"},
        ],
        "fallingBlocks": [
            {"x": 1000, "y": -80, "w": 70, "h": 70, "triggerX": 870, "delay": 0.588, "groundY": 500},
            {"x": 2200, "y": -80, "w": 80, "h": 80, "triggerX": 2050, "delay": 0.529, "groundY": 500},
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
            {"x": 900, "y": 470, "r": 16, "minX": 820, "maxX": 1000, "speed": 165},
            {"x": 1600, "y": 470, "r": 16, "minX": 1520, "maxX": 1700, "speed": 182},
        ],
        "runWall": {"startX": -200, "speed": 124, "y": 0, "h": 620},
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
            {"x": 850, "y": 470, "r": 16, "minX": 780, "maxX": 950, "speed": 182},
            {"x": 2050, "y": 470, "r": 16, "minX": 1980, "maxX": 2150, "speed": 198},
        ],
        "wallSpikes": [
            {"x": 1500, "y": 390, "w": 24, "h": 70, "reach": 33, "triggerX": 1470, "delay": 0.493, "dir": 1},
        ],
        "runWall": {"startX": -150, "speed": 136, "y": 0, "h": 620},
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
            {"x": 1050, "y": -80, "w": 70, "h": 70, "triggerX": 900, "delay": 0.646, "groundY": 500},
            {"x": 2300, "y": -80, "w": 80, "h": 80, "triggerX": 2150, "delay": 0.529, "groundY": 500},
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
            {**rect(500, 500, 150, 40), "type": "hidden_bomb", "triggerX": 530, "delay": 0.352, "blastRadius": 58},
            {**rect(650, 500, 650, 40), "type": "solid"},
            {**rect(1300, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1330, "delay": 0.352, "blastRadius": 58},
            {**rect(1450, 500, 1250, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2800, 40), "type": "void"},
        ],
        "bombs": [
            {"kind": "side", "y": 495, "dir": 1, "fromX": 700, "toX": 1200, "triggerX": 900, "delay": 0.47, "speed": 231, "radius": 16},
            {"kind": "side", "y": 495, "dir": -1, "fromX": 2300, "toX": 1700, "triggerX": 2000, "delay": 0.47, "speed": 248, "radius": 18},
        ],
        "wallSpikes": [
            {"x": 1630, "y": 390, "w": 24, "h": 70, "reach": 33, "triggerX": 1600, "delay": 0.493, "dir": 1},
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
            {"x": 700, "kind": "sky", "y": -80, "triggerX": 550, "delay": 0.588, "groundY": 500, "radius": 20, "blastRadius": 50},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1200, "toX": 1700, "triggerX": 1400, "delay": 0.47, "speed": 248, "radius": 16},
            {"x": 2000, "kind": "sky", "y": -80, "triggerX": 1850, "delay": 0.529, "groundY": 500, "radius": 21, "blastRadius": 54},
        ],
        "runWall": {"startX": -200, "speed": 132, "y": 0, "h": 620},
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
            {"x": 1200, "y": -80, "w": 70, "h": 70, "triggerX": 1050, "delay": 0.588, "groundY": 500},
        ],
        "saws": [
            {"x": 1300, "y": 470, "r": 16, "minX": 1250, "maxX": 1420, "speed": 182},
        ],
        "bombs": [
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1700, "toX": 2200, "triggerX": 1850, "delay": 0.47, "speed": 231, "radius": 16},
            {"x": 2300, "kind": "sky", "y": -80, "triggerX": 2150, "delay": 0.529, "groundY": 500, "radius": 21, "blastRadius": 54},
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
            {**rect(1500, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1530, "delay": 0.352, "blastRadius": 58},
            {**rect(1650, 500, 1350, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3100, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 450, "y": 460, "w": 50, "h": 40, "toX": 950, "toY": 440},
        ],
        "fallingBlocks": [
            {"x": 1200, "y": -80, "w": 70, "h": 70, "triggerX": 1050, "delay": 0.588, "groundY": 500},
            {"x": 2400, "y": -80, "w": 80, "h": 80, "triggerX": 2250, "delay": 0.529, "groundY": 500},
        ],
        "bombs": [
            {"x": 1900, "kind": "sky", "y": -80, "triggerX": 1750, "delay": 0.588, "groundY": 500, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 2500, "toX": 3000, "triggerX": 2700, "delay": 0.47, "speed": 248, "radius": 18},
        ],
        "runWall": {"startX": -250, "speed": 116, "y": 0, "h": 620},
    },
]

# ---- Nivel 41-50: nuevos tipos de bloque — hielo resbaladizo (menos friccion,
# menos aceleracion), plataformas viajeras que cargan al jugador, resortes que
# lanzan con un arco completo y consistente, y piedra como textura nueva sin
# cambiar el comportamiento solido. Se combinan con los peligros ya existentes
# (bombas de cielo/flanco, bloques que caen, bombas escondidas, teletransporte).
LEVELS += [
    {
        "name": "Nivel 41 - Piso resbaladizo",
        "hint": "El hielo no perdona los frenazos, solo los saltos",
        "width": 2200,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2120, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 500, 40), "type": "ice"},
            {**rect(800, 460, 200, 40), "type": "solid"},
            {**rect(1000, 460, 400, 40), "type": "ice"},
            {**rect(1400, 500, 200, 40), "type": "solid"},
            {**rect(1600, 500, 600, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 2300, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1150, "y": 430, "r": 16, "minX": 1080, "maxX": 1320, "speed": 157},
        ],
    },
    {
        "name": "Nivel 42 - Plataformas viajeras",
        "hint": "Espera, sube, no te caigas",
        "width": 1450,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1370, 240, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 480, 100, 20), "type": "moving", "axis": "x", "minX": 300, "maxX": 700, "speed": 91},
            {**rect(750, 500, 350, 40), "type": "solid"},
            {**rect(1100, 500, 100, 20), "type": "moving", "axis": "y", "minY": 340, "maxY": 500, "speed": 74},
            {**rect(1100, 340, 350, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 1550, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 43 - Rebota o cae",
        "hint": "Deja que el resorte haga el trabajo",
        "width": 1900,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1820, 240, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 100, 40), "type": "bounce"},
            {**rect(560, 420, 400, 40), "type": "solid"},
            {**rect(960, 420, 100, 40), "type": "bounce"},
            {**rect(1200, 340, 700, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2000, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 44 - Piedra y hielo",
        "hint": "El suelo cambia, la sombra tambien",
        "width": 2600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "stone"},
            {**rect(400, 500, 400, 40), "type": "ice"},
            {**rect(800, 460, 200, 40), "type": "stone"},
            {**rect(1000, 460, 400, 40), "type": "ice"},
            {**rect(1400, 500, 300, 40), "type": "stone"},
            {**rect(1700, 500, 900, 40), "type": "stone"},
        ],
        "hazards": [
            {**rect(-50, 620, 2700, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1150, "y": 430, "r": 16, "minX": 1080, "maxX": 1320, "speed": 165},
        ],
        "fallingBlocks": [
            {"x": 600, "y": -80, "w": 70, "h": 70, "triggerX": 470, "delay": 0.588, "groundY": 500},
            {"x": 2100, "y": -80, "w": 80, "h": 80, "triggerX": 1950, "delay": 0.529, "groundY": 500},
        ],
    },
    {
        "name": "Nivel 45 - Todo se mueve",
        "hint": "Nada se queda quieto, ni el suelo ni las bombas",
        "width": 2400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2320, 240, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 480, 100, 20), "type": "moving", "axis": "x", "minX": 300, "maxX": 700, "speed": 99},
            {**rect(750, 500, 650, 40), "type": "solid"},
            {**rect(1400, 500, 100, 20), "type": "moving", "axis": "y", "minY": 340, "maxY": 500, "speed": 82},
            {**rect(1400, 340, 1000, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2500, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 1000, "kind": "sky", "y": -80, "triggerX": 850, "delay": 0.588, "groundY": 500, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 900, "toX": 1350, "triggerX": 1100, "delay": 0.47, "speed": 231, "radius": 16},
        ],
    },
    {
        "name": "Nivel 46 - Rebote mortal",
        "hint": "El resorte te sube, la pared te espera",
        "width": 2500,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2420, 300, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "solid"},
            {**rect(400, 500, 150, 40), "type": "hidden_bomb", "triggerX": 430, "delay": 0.352, "blastRadius": 58},
            {**rect(550, 500, 250, 40), "type": "solid"},
            {**rect(800, 500, 100, 40), "type": "bounce"},
            {**rect(1050, 400, 400, 40), "type": "solid"},
            {**rect(1450, 400, 1050, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2600, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1800, "y": 370, "r": 16, "minX": 1700, "maxX": 1950, "speed": 190},
        ],
        "wallSpikes": [
            {"x": 1600, "y": 320, "w": 24, "h": 70, "reach": 33, "triggerX": 1550, "delay": 0.493, "dir": 1},
        ],
    },
    {
        "name": "Nivel 47 - El laberinto helado",
        "hint": "El hielo esconde mas que resbalones",
        "width": 2300,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2220, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "ice"},
            {**rect(750, 500, 500, 40), "type": "ice"},
            {**rect(1250, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1280, "delay": 0.352, "blastRadius": 58},
            {**rect(1400, 500, 900, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 2400, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 300, "y": 460, "w": 50, "h": 40, "toX": 800, "toY": 440},
        ],
    },
    {
        "name": "Nivel 48 - Plataformas y explosivos",
        "hint": "El camino se mueve mientras todo explota",
        "width": 2600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2520, 240, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 480, 100, 20), "type": "moving", "axis": "x", "minX": 300, "maxX": 700, "speed": 99},
            {**rect(750, 500, 850, 40), "type": "solid"},
            {**rect(1600, 500, 100, 20), "type": "moving", "axis": "y", "minY": 340, "maxY": 500, "speed": 82},
            {**rect(1600, 340, 1000, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2700, 40), "type": "void"},
        ],
        "fallingBlocks": [
            {"x": 1000, "y": -80, "w": 70, "h": 70, "triggerX": 870, "delay": 0.588, "groundY": 500},
        ],
        "bombs": [
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1100, "toX": 1550, "triggerX": 1300, "delay": 0.47, "speed": 239, "radius": 16},
        ],
    },
    {
        "name": "Nivel 49 - Corre, resbala, rebota",
        "hint": "No frenes ni en el hielo ni en el aire",
        "width": 2300,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2220, 320, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "solid"},
            {**rect(400, 500, 400, 40), "type": "ice"},
            {**rect(800, 500, 100, 40), "type": "bounce"},
            {**rect(1050, 420, 400, 40), "type": "solid"},
            {**rect(1450, 420, 850, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 2400, 40), "type": "void"},
        ],
        "runWall": {"startX": -260, "speed": 107, "y": 0, "h": 620},
    },
    {
        "name": "Nivel 50 - Ultimatum de bloques",
        "hint": "Hielo, resortes, plataformas y bombas: todo junto",
        "width": 3200,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3120, 200, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "stone"},
            {**rect(350, 500, 400, 40), "type": "ice"},
            {**rect(750, 500, 150, 40), "type": "hidden_bomb", "triggerX": 780, "delay": 0.352, "blastRadius": 58},
            {**rect(900, 480, 100, 20), "type": "moving", "axis": "x", "minX": 900, "maxX": 1300, "speed": 99},
            {**rect(1350, 500, 450, 40), "type": "stone"},
            {**rect(1800, 500, 100, 40), "type": "bounce"},
            {**rect(2050, 400, 450, 40), "type": "ice"},
            {**rect(2500, 400, 100, 20), "type": "moving", "axis": "y", "minY": 300, "maxY": 400, "speed": 74},
            {**rect(2500, 300, 700, 40), "type": "stone"},
        ],
        "hazards": [
            {**rect(-50, 620, 3300, 40), "type": "void"},
        ],
        "fallingBlocks": [
            {"x": 1550, "y": -80, "w": 80, "h": 80, "triggerX": 1400, "delay": 0.588, "groundY": 500},
        ],
        "bombs": [
            {"x": 2250, "kind": "sky", "y": -80, "triggerX": 2100, "delay": 0.588, "groundY": 400, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 295, "dir": 1, "fromX": 2600, "toX": 3100, "triggerX": 2800, "delay": 0.47, "speed": 248, "radius": 18},
        ],
    },
]

# ---- Nivel 51-70: mas variedad remezclando el catalogo de trampas y bloques
# ya existente (hielo, plataformas viajeras, resortes, piedra, bombas de
# cielo/flanco, bloques que caen, bombas escondidas, teletransporte, muro de
# sombra) en combinaciones nuevas, escalando dificultad con margenes seguros.
LEVELS += [
    {
        "name": "Nivel 51 - Hielo y sierras",
        "hint": "El hielo te lleva directo a la sierra si no saltas a tiempo",
        "width": 2400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2320, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "solid"},
            {**rect(350, 500, 400, 40), "type": "ice"},
            {**rect(750, 500, 200, 40), "type": "solid"},
            {**rect(950, 500, 450, 40), "type": "ice"},
            {**rect(1400, 500, 200, 40), "type": "solid"},
            {**rect(1600, 500, 800, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 2500, 40), "type": "void"},
        ],
        "saws": [
            {"x": 550, "y": 470, "r": 16, "minX": 450, "maxX": 650, "speed": 157},
            {"x": 1150, "y": 470, "r": 16, "minX": 1020, "maxX": 1330, "speed": 173},
        ],
    },
    {
        "name": "Nivel 52 - El puente que se mueve",
        "hint": "Plataformas que no esperan a nadie",
        "width": 1900,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1820, 220, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 480, 100, 20), "type": "moving", "axis": "x", "minX": 300, "maxX": 650, "speed": 99},
            {**rect(700, 500, 300, 40), "type": "solid"},
            {**rect(1000, 500, 100, 20), "type": "moving", "axis": "y", "minY": 320, "maxY": 500, "speed": 82},
            {**rect(1000, 320, 300, 40), "type": "solid"},
            {**rect(1300, 320, 100, 20), "type": "moving", "axis": "x", "minX": 1300, "maxX": 1600, "speed": 91},
            {**rect(1650, 320, 250, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2000, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 53 - Rebote doble",
        "hint": "Tres saltos de resorte, cada vez mas alto",
        "width": 2200,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2120, 160, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 100, 40), "type": "bounce"},
            {**rect(560, 420, 300, 40), "type": "solid"},
            {**rect(860, 420, 100, 40), "type": "bounce"},
            {**rect(1120, 340, 300, 40), "type": "solid"},
            {**rect(1420, 340, 100, 40), "type": "bounce"},
            {**rect(1680, 260, 520, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2300, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 54 - Piedra, fuego y bombas",
        "hint": "La piedra aguanta, las bombas no avisan",
        "width": 2500,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2420, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 600, 40), "type": "stone"},
            {**rect(600, 460, 200, 40), "type": "stone"},
            {**rect(800, 500, 600, 40), "type": "stone"},
            {**rect(1400, 460, 200, 40), "type": "stone"},
            {**rect(1600, 500, 900, 40), "type": "stone"},
        ],
        "hazards": [
            {**rect(-50, 620, 2600, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 400, "kind": "sky", "y": -80, "triggerX": 250, "delay": 0.588, "groundY": 500, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 900, "toX": 1350, "triggerX": 1100, "delay": 0.47, "speed": 239, "radius": 16},
            {"x": 2100, "kind": "sky", "y": -80, "triggerX": 1950, "delay": 0.529, "groundY": 500, "radius": 23, "blastRadius": 58},
        ],
    },
    {
        "name": "Nivel 55 - El teletransporte extremo",
        "hint": "Cuatro portales, ni un paso de mas",
        "width": 3100,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3020, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(700, 500, 300, 40), "type": "solid"},
            {**rect(1400, 500, 300, 40), "type": "solid"},
            {**rect(2100, 500, 300, 40), "type": "solid"},
            {**rect(2800, 500, 300, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3200, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 250, "y": 460, "w": 50, "h": 40, "toX": 720, "toY": 440},
            {"x": 950, "y": 460, "w": 50, "h": 40, "toX": 1420, "toY": 440},
            {"x": 1650, "y": 460, "w": 50, "h": 40, "toX": 2120, "toY": 440},
            {"x": 2350, "y": 460, "w": 50, "h": 40, "toX": 2820, "toY": 440},
        ],
    },
    {
        "name": "Nivel 56 - Bloques y hielo",
        "hint": "El bloque cae igual, resbales o no",
        "width": 2400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2320, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 500, 40), "type": "ice"},
            {**rect(500, 460, 200, 40), "type": "solid"},
            {**rect(700, 500, 500, 40), "type": "ice"},
            {**rect(1200, 460, 200, 40), "type": "solid"},
            {**rect(1400, 500, 1000, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 2500, 40), "type": "void"},
        ],
        "fallingBlocks": [
            {"x": 250, "y": -80, "w": 70, "h": 70, "triggerX": 120, "delay": 0.588, "groundY": 500},
            {"x": 950, "y": -80, "w": 70, "h": 70, "triggerX": 800, "delay": 0.588, "groundY": 500},
            {"x": 1900, "y": -80, "w": 80, "h": 80, "triggerX": 1750, "delay": 0.529, "groundY": 500},
        ],
    },
    {
        "name": "Nivel 57 - Todo explota",
        "hint": "Nada es seguro: ni el suelo ni el aire",
        "width": 2700,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2620, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 500, 40), "type": "solid"},
            {**rect(500, 500, 150, 40), "type": "hidden_bomb", "triggerX": 530, "delay": 0.352, "blastRadius": 58},
            {**rect(650, 500, 650, 40), "type": "solid"},
            {**rect(1300, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1330, "delay": 0.352, "blastRadius": 58},
            {**rect(1450, 500, 1250, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2800, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 900, "kind": "sky", "y": -80, "triggerX": 750, "delay": 0.588, "groundY": 500, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1700, "toX": 2200, "triggerX": 1900, "delay": 0.47, "speed": 248, "radius": 16},
            {"x": 2450, "kind": "sky", "y": -80, "triggerX": 2300, "delay": 0.529, "groundY": 500, "radius": 23, "blastRadius": 58},
        ],
    },
    {
        "name": "Nivel 58 - Corre sin parar 2",
        "hint": "Mas rapido, sin margen para dudar",
        "width": 2600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 2600, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2700, 40), "type": "void"},
        ],
        "saws": [
            {"x": 900, "y": 470, "r": 16, "minX": 820, "maxX": 1020, "speed": 190},
            {"x": 1900, "y": 470, "r": 16, "minX": 1820, "maxX": 2020, "speed": 206},
        ],
        "wallSpikes": [
            {"x": 1450, "y": 390, "w": 24, "h": 70, "reach": 33, "triggerX": 1400, "delay": 0.493, "dir": 1},
        ],
        "runWall": {"startX": -180, "speed": 140, "y": 0, "h": 620},
    },
    {
        "name": "Nivel 59 - El combo helado",
        "hint": "Hielo, resorte y una plataforma que sube",
        "width": 2400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2320, 200, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "ice"},
            {**rect(300, 480, 100, 20), "type": "moving", "axis": "x", "minX": 300, "maxX": 650, "speed": 95},
            {**rect(700, 500, 300, 40), "type": "ice"},
            {**rect(1000, 500, 100, 40), "type": "bounce"},
            {**rect(1260, 420, 400, 40), "type": "ice"},
            {**rect(1660, 420, 100, 20), "type": "moving", "axis": "y", "minY": 300, "maxY": 420, "speed": 78},
            {**rect(1660, 300, 740, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 2500, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 60 - Ultimatum de bloques II",
        "hint": "Todo lo aprendido, en un solo tramo",
        "width": 3300,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3220, 200, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "stone"},
            {**rect(400, 500, 400, 40), "type": "ice"},
            {**rect(800, 500, 150, 40), "type": "hidden_bomb", "triggerX": 830, "delay": 0.352, "blastRadius": 58},
            {**rect(950, 480, 100, 20), "type": "moving", "axis": "x", "minX": 950, "maxX": 1350, "speed": 99},
            {**rect(1400, 500, 450, 40), "type": "stone"},
            {**rect(1850, 500, 100, 40), "type": "bounce"},
            {**rect(2100, 400, 450, 40), "type": "ice"},
            {**rect(2550, 400, 100, 20), "type": "moving", "axis": "y", "minY": 300, "maxY": 400, "speed": 74},
            {**rect(2550, 300, 750, 40), "type": "stone"},
        ],
        "hazards": [
            {**rect(-50, 620, 3400, 40), "type": "void"},
        ],
        "fallingBlocks": [
            {"x": 600, "y": -80, "w": 70, "h": 70, "triggerX": 470, "delay": 0.588, "groundY": 500},
        ],
        "bombs": [
            {"x": 2300, "kind": "sky", "y": -80, "triggerX": 2150, "delay": 0.588, "groundY": 400, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 295, "dir": 1, "fromX": 2650, "toX": 3200, "triggerX": 2850, "delay": 0.47, "speed": 248, "radius": 18},
        ],
    },
    {
        "name": "Nivel 61 - Sierras y resortes",
        "hint": "Salta, rebota, esquiva la sierra",
        "width": 2300,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2220, 240, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "solid"},
            {**rect(400, 500, 100, 40), "type": "bounce"},
            {**rect(660, 420, 400, 40), "type": "solid"},
            {**rect(1060, 420, 100, 40), "type": "bounce"},
            {**rect(1320, 340, 980, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2400, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1700, "y": 310, "r": 16, "minX": 1600, "maxX": 1900, "speed": 190},
        ],
    },
    {
        "name": "Nivel 62 - Plataformas fantasmas",
        "hint": "No todo lo que ves es real, ni todo se mueve",
        "width": 2200,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2120, 240, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 150, 40), "type": "fake_floor"},
            {**rect(450, 500, 250, 40), "type": "solid"},
            {**rect(700, 480, 100, 20), "type": "moving", "axis": "x", "minX": 700, "maxX": 1050, "speed": 95},
            {**rect(1100, 460, 400, 40), "type": "solid"},
            {**rect(1500, 460, 100, 20), "type": "moving", "axis": "y", "minY": 340, "maxY": 460, "speed": 74},
            {**rect(1500, 340, 700, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2300, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 63 - Bombas por todos lados",
        "hint": "El cielo y los costados, todo es peligro",
        "width": 2800,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2720, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 700, 40), "type": "solid"},
            {**rect(700, 460, 200, 40), "type": "solid"},
            {**rect(900, 500, 700, 40), "type": "solid"},
            {**rect(1600, 460, 200, 40), "type": "solid"},
            {**rect(1800, 500, 1000, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2900, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 400, "kind": "sky", "y": -80, "triggerX": 250, "delay": 0.588, "groundY": 500, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 850, "toX": 1350, "triggerX": 1050, "delay": 0.47, "speed": 239, "radius": 16},
            {"x": 1950, "kind": "sky", "y": -80, "triggerX": 1800, "delay": 0.529, "groundY": 500, "radius": 23, "blastRadius": 58},
            {"kind": "side", "y": 495, "dir": -1, "fromX": 2700, "toX": 2100, "triggerX": 2450, "delay": 0.47, "speed": 256, "radius": 18},
        ],
    },
    {
        "name": "Nivel 64 - Hielo mortal",
        "hint": "El hielo no te deja frenar a tiempo",
        "width": 2500,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2420, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "solid"},
            {**rect(400, 500, 600, 40), "type": "ice"},
            {**rect(1000, 460, 200, 40), "type": "solid"},
            {**rect(1200, 460, 600, 40), "type": "ice"},
            {**rect(1800, 500, 200, 40), "type": "solid"},
            {**rect(2000, 500, 500, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 2600, 40), "type": "void"},
        ],
        "saws": [
            {"x": 650, "y": 470, "r": 16, "minX": 550, "maxX": 850, "speed": 165},
            {"x": 1450, "y": 430, "r": 16, "minX": 1350, "maxX": 1650, "speed": 182},
        ],
    },
    {
        "name": "Nivel 65 - Teletransporte y bloques",
        "hint": "El portal no te salva de lo que cae",
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
            {"x": 1050, "y": -80, "w": 70, "h": 70, "triggerX": 900, "delay": 0.646, "groundY": 500},
            {"x": 2300, "y": -80, "w": 80, "h": 80, "triggerX": 2150, "delay": 0.529, "groundY": 500},
        ],
    },
    {
        "name": "Nivel 66 - La torre movil",
        "hint": "Sube piso a piso, sin caer",
        "width": 1400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1320, 90, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 100, 20), "type": "moving", "axis": "y", "minY": 380, "maxY": 500, "speed": 74},
            {**rect(300, 380, 300, 40), "type": "solid"},
            {**rect(700, 380, 100, 20), "type": "moving", "axis": "y", "minY": 260, "maxY": 380, "speed": 78},
            {**rect(700, 260, 300, 40), "type": "solid"},
            {**rect(1100, 260, 100, 20), "type": "moving", "axis": "y", "minY": 190, "maxY": 260, "speed": 82},
            {**rect(1100, 190, 300, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 1500, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 67 - Fuego cruzado 2",
        "hint": "El fuego cruzado no da tregua",
        "width": 2900,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2820, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 650, 40), "type": "solid"},
            {**rect(650, 500, 150, 40), "type": "hidden_spike", "triggerX": 680, "delay": 0.329},
            {**rect(800, 500, 700, 40), "type": "solid"},
            {**rect(1500, 460, 200, 40), "type": "solid"},
            {**rect(1700, 500, 1200, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3000, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 1150, "kind": "sky", "y": -80, "triggerX": 1000, "delay": 0.588, "groundY": 500, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1550, "toX": 2050, "triggerX": 1900, "delay": 0.47, "speed": 248, "radius": 16},
            {"x": 2350, "kind": "sky", "y": -80, "triggerX": 2200, "delay": 0.529, "groundY": 500, "radius": 23, "blastRadius": 58},
            {"kind": "side", "y": 495, "dir": -1, "fromX": 2850, "toX": 2400, "triggerX": 2600, "delay": 0.47, "speed": 264, "radius": 18},
        ],
    },
    {
        "name": "Nivel 68 - Corre, resbala, explota",
        "hint": "El hielo desliza, la bomba no perdona",
        "width": 2400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2320, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 2400, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 2500, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 700, "kind": "sky", "y": -80, "triggerX": 550, "delay": 0.588, "groundY": 500, "radius": 20, "blastRadius": 50},
            {"kind": "side", "y": 495, "dir": -1, "fromX": 1700, "toX": 1100, "triggerX": 1400, "delay": 0.47, "speed": 231, "radius": 16},
            {"x": 2000, "kind": "sky", "y": -80, "triggerX": 1850, "delay": 0.529, "groundY": 500, "radius": 21, "blastRadius": 54},
        ],
        "runWall": {"startX": -220, "speed": 124, "y": 0, "h": 620},
    },
    {
        "name": "Nivel 69 - El laberinto final",
        "hint": "Portales, plataformas y trampas escondidas",
        "width": 2600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "solid"},
            {**rect(750, 500, 150, 40), "type": "hidden_bomb", "triggerX": 780, "delay": 0.352, "blastRadius": 58},
            {**rect(900, 480, 100, 20), "type": "moving", "axis": "x", "minX": 900, "maxX": 1250, "speed": 95},
            {**rect(1300, 500, 500, 40), "type": "solid"},
            {**rect(1800, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1830, "delay": 0.352, "blastRadius": 58},
            {**rect(1950, 500, 650, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2700, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 300, "y": 460, "w": 50, "h": 40, "toX": 800, "toY": 440},
        ],
    },
    {
        "name": "Nivel 70 - Ultimatum total",
        "hint": "El final de este tramo: todo junto, otra vez",
        "width": 3400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3320, 200, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "stone"},
            {**rect(350, 500, 400, 40), "type": "ice"},
            {**rect(750, 500, 150, 40), "type": "hidden_bomb", "triggerX": 780, "delay": 0.352, "blastRadius": 58},
            {**rect(900, 480, 100, 20), "type": "moving", "axis": "x", "minX": 900, "maxX": 1300, "speed": 99},
            {**rect(1350, 500, 450, 40), "type": "stone"},
            {**rect(1800, 500, 100, 40), "type": "bounce"},
            {**rect(2050, 400, 450, 40), "type": "ice"},
            {**rect(2500, 400, 100, 20), "type": "moving", "axis": "y", "minY": 300, "maxY": 400, "speed": 74},
            {**rect(2500, 300, 900, 40), "type": "stone"},
        ],
        "hazards": [
            {**rect(-50, 620, 3500, 40), "type": "void"},
        ],
        "fallingBlocks": [
            {"x": 600, "y": -80, "w": 70, "h": 70, "triggerX": 470, "delay": 0.588, "groundY": 500},
        ],
        "bombs": [
            {"x": 2300, "kind": "sky", "y": -80, "triggerX": 2150, "delay": 0.588, "groundY": 400, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 295, "dir": 1, "fromX": 2650, "toX": 3300, "triggerX": 2850, "delay": 0.47, "speed": 248, "radius": 18},
        ],
        "saws": [
            {"x": 2700, "y": 270, "r": 16, "minX": 2600, "maxX": 2850, "speed": 190},
        ],
        "wallSpikes": [
            {"x": 3050, "y": 220, "w": 24, "h": 70, "reach": 33, "triggerX": 3000, "delay": 0.493, "dir": 1},
        ],
    },
]

# ---- Nivel 71-80: la dificultad sube (mas sierras simultaneas, mas bombas,
# resortes encadenados, torres verticales, un descenso) pero cada combo se
# valida con los mismos margenes seguros que el resto del juego — nada de
# ventanas de esquive imposibles.
LEVELS += [
    {
        "name": "Nivel 71 - Sierras dobles y hielo",
        "hint": "El hielo no perdona los frenazos, y ahora hay el doble de sierras",
        "width": 2600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "solid"},
            {**rect(350, 500, 500, 40), "type": "ice"},
            {**rect(850, 460, 200, 40), "type": "solid"},
            {**rect(1050, 460, 500, 40), "type": "ice"},
            {**rect(1550, 500, 200, 40), "type": "solid"},
            {**rect(1750, 500, 850, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 2700, 40), "type": "void"},
        ],
        "saws": [
            {"x": 550, "y": 470, "r": 16, "minX": 470, "maxX": 620, "speed": 165},
            {"x": 750, "y": 470, "r": 16, "minX": 700, "maxX": 800, "speed": 173},
            {"x": 1160, "y": 430, "r": 16, "minX": 1100, "maxX": 1230, "speed": 173},
            {"x": 1380, "y": 430, "r": 16, "minX": 1310, "maxX": 1450, "speed": 182},
        ],
    },
    {
        "name": "Nivel 72 - La torre y las bombas",
        "hint": "Sube la torre mientras el cielo te ataca",
        "width": 1400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1320, 90, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 100, 20), "type": "moving", "axis": "y", "minY": 380, "maxY": 500, "speed": 78},
            {**rect(300, 380, 400, 40), "type": "solid"},
            {**rect(700, 380, 100, 20), "type": "moving", "axis": "y", "minY": 260, "maxY": 380, "speed": 82},
            {**rect(700, 260, 400, 40), "type": "solid"},
            {**rect(1100, 260, 100, 20), "type": "moving", "axis": "y", "minY": 190, "maxY": 260, "speed": 87},
            {**rect(1100, 190, 300, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 1500, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 500, "kind": "sky", "y": -80, "triggerX": 350, "delay": 0.588, "groundY": 380, "radius": 20, "blastRadius": 50},
            {"x": 900, "kind": "sky", "y": -80, "triggerX": 750, "delay": 0.588, "groundY": 260, "radius": 20, "blastRadius": 50},
        ],
    },
    {
        "name": "Nivel 73 - Rebote extremo",
        "hint": "Cuatro resortes, cuatro alturas",
        "width": 2600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2520, 90, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 100, 40), "type": "bounce"},
            {**rect(560, 420, 300, 40), "type": "solid"},
            {**rect(860, 420, 100, 40), "type": "bounce"},
            {**rect(1120, 340, 300, 40), "type": "solid"},
            {**rect(1420, 340, 100, 40), "type": "bounce"},
            {**rect(1680, 260, 300, 40), "type": "solid"},
            {**rect(1980, 260, 100, 40), "type": "bounce"},
            {**rect(2240, 190, 360, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2700, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 74 - Piedra ardiente",
        "hint": "La piedra arde, las bombas no descansan",
        "width": 2700,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2620, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 600, 40), "type": "stone"},
            {**rect(600, 500, 150, 40), "type": "hidden_spike", "triggerX": 630, "delay": 0.329},
            {**rect(750, 500, 650, 40), "type": "stone"},
            {**rect(1400, 460, 200, 40), "type": "stone"},
            {**rect(1600, 500, 1100, 40), "type": "stone"},
        ],
        "hazards": [
            {**rect(-50, 620, 2800, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 300, "kind": "sky", "y": -80, "triggerX": 150, "delay": 0.588, "groundY": 500, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 900, "toX": 1300, "triggerX": 1050, "delay": 0.47, "speed": 248, "radius": 16},
            {"x": 2000, "kind": "sky", "y": -80, "triggerX": 1850, "delay": 0.529, "groundY": 500, "radius": 23, "blastRadius": 58},
            {"kind": "side", "y": 495, "dir": -1, "fromX": 2600, "toX": 2100, "triggerX": 2350, "delay": 0.47, "speed": 264, "radius": 18},
        ],
    },
    {
        "name": "Nivel 75 - Portales y sierras",
        "hint": "El portal te salva del vacio, no de la sierra",
        "width": 2500,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2420, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(700, 500, 300, 40), "type": "solid"},
            {**rect(1400, 500, 300, 40), "type": "solid"},
            {**rect(2100, 500, 400, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2600, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 250, "y": 460, "w": 50, "h": 40, "toX": 720, "toY": 440},
            {"x": 950, "y": 460, "w": 50, "h": 40, "toX": 1420, "toY": 440},
            {"x": 1650, "y": 460, "w": 50, "h": 40, "toX": 2120, "toY": 440},
        ],
        "saws": [
            {"x": 830, "y": 470, "r": 15, "minX": 760, "maxX": 900, "speed": 157},
            {"x": 1520, "y": 470, "r": 15, "minX": 1470, "maxX": 1580, "speed": 165},
        ],
    },
    {
        "name": "Nivel 76 - El descenso movil",
        "hint": "A veces hay que bajar para poder avanzar",
        "width": 2000,
        "spawn": {"x": 60, "y": 240},
        "goal": rect(1920, 360, 50, 100),
        "platforms": [
            {**rect(0, 300, 300, 40), "type": "solid"},
            {**rect(300, 300, 100, 20), "type": "moving", "axis": "y", "minY": 300, "maxY": 500, "speed": 91},
            {**rect(300, 500, 500, 40), "type": "ice"},
            {**rect(800, 460, 200, 40), "type": "solid"},
            {**rect(1000, 460, 100, 20), "type": "moving", "axis": "x", "minX": 1000, "maxX": 1350, "speed": 95},
            {**rect(1400, 460, 600, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 2100, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 77 - Todo esconde algo",
        "hint": "Nada aqui es lo que aparenta",
        "width": 2600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 150, 40), "type": "hidden_bomb", "triggerX": 330, "delay": 0.352, "blastRadius": 58},
            {**rect(450, 500, 150, 40), "type": "fake_floor"},
            {**rect(600, 500, 300, 40), "type": "solid"},
            {**rect(900, 500, 150, 40), "type": "hidden_spike", "triggerX": 930, "delay": 0.329},
            {**rect(1050, 500, 150, 40), "type": "fake_floor"},
            {**rect(1200, 500, 350, 40), "type": "solid"},
            {**rect(1550, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1580, "delay": 0.352, "blastRadius": 58},
            {**rect(1700, 500, 150, 40), "type": "hidden_spike", "triggerX": 1730, "delay": 0.329},
            {**rect(1850, 500, 750, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2700, 40), "type": "void"},
        ],
    },
    {
        "name": "Nivel 78 - Corre y salta sin fin",
        "hint": "El resorte te sube, la sombra no te espera",
        "width": 2400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2320, 320, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "solid"},
            {**rect(400, 500, 100, 40), "type": "bounce"},
            {**rect(660, 420, 1740, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2500, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1100, "y": 390, "r": 16, "minX": 1020, "maxX": 1220, "speed": 190},
            {"x": 1900, "y": 390, "r": 16, "minX": 1820, "maxX": 2020, "speed": 206},
        ],
        "runWall": {"startX": -200, "speed": 132, "y": 0, "h": 620},
    },
    {
        "name": "Nivel 79 - El ultimo laberinto",
        "hint": "Portales, plataformas, bombas y trampas: el ultimo tramo",
        "width": 2800,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2720, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "solid"},
            {**rect(800, 500, 150, 40), "type": "hidden_bomb", "triggerX": 830, "delay": 0.352, "blastRadius": 58},
            {**rect(950, 480, 100, 20), "type": "moving", "axis": "x", "minX": 950, "maxX": 1300, "speed": 95},
            {**rect(1350, 500, 500, 40), "type": "solid"},
            {**rect(1850, 500, 150, 40), "type": "hidden_bomb", "triggerX": 1880, "delay": 0.352, "blastRadius": 58},
            {**rect(2000, 500, 800, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2900, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 300, "y": 460, "w": 50, "h": 40, "toX": 850, "toY": 440},
        ],
        "bombs": [
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1450, "toX": 1950, "triggerX": 1650, "delay": 0.47, "speed": 248, "radius": 16},
        ],
    },
    {
        "name": "Nivel 80 - El desafio final",
        "hint": "El desafio final: todo lo que aprendiste, junto",
        "width": 3600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3520, 220, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "stone"},
            {**rect(350, 500, 400, 40), "type": "ice"},
            {**rect(750, 500, 150, 40), "type": "hidden_bomb", "triggerX": 780, "delay": 0.352, "blastRadius": 58},
            {**rect(900, 480, 100, 20), "type": "moving", "axis": "x", "minX": 900, "maxX": 1300, "speed": 99},
            {**rect(1350, 500, 450, 40), "type": "stone"},
            {**rect(1800, 500, 100, 40), "type": "bounce"},
            {**rect(2060, 420, 440, 40), "type": "ice"},
            {**rect(2500, 420, 100, 20), "type": "moving", "axis": "y", "minY": 320, "maxY": 420, "speed": 78},
            {**rect(2500, 320, 450, 40), "type": "stone"},
            {**rect(2950, 320, 150, 40), "type": "hidden_spike", "triggerX": 2980, "delay": 0.329},
            {**rect(3100, 320, 500, 40), "type": "stone"},
        ],
        "hazards": [
            {**rect(-50, 620, 3700, 40), "type": "void"},
        ],
        "fallingBlocks": [
            {"x": 600, "y": -80, "w": 70, "h": 70, "triggerX": 470, "delay": 0.588, "groundY": 500},
        ],
        "bombs": [
            {"x": 2280, "kind": "sky", "y": -80, "triggerX": 2150, "delay": 0.588, "groundY": 420, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 315, "dir": 1, "fromX": 3150, "toX": 3550, "triggerX": 3300, "delay": 0.47, "speed": 248, "radius": 18},
        ],
        "saws": [
            {"x": 1600, "y": 470, "r": 15, "minX": 1400, "maxX": 1700, "speed": 182},
        ],
        "wallSpikes": [
            {"x": 2650, "y": 280, "w": 24, "h": 70, "reach": 33, "triggerX": 2600, "delay": 0.493, "dir": 1},
        ],
    },
]

# ---- Nivel 81-90: mas altura y mas densidad, siempre respetando que la
# camara nunca se desplaza verticalmente — ninguna plataforma ni portal puede
# quedar por encima del borde superior del canvas tras el ajuste de GROUND_LIFT.
LEVELS += [
    {
        "name": "Nivel 81 - Sierras y hielo extremo",
        "hint": "El hielo no perdona los frenazos",
        "width": 2800,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2720, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "solid"},
            {**rect(350, 500, 450, 40), "type": "ice"},
            {**rect(800, 500, 200, 40), "type": "solid"},
            {**rect(1000, 500, 500, 40), "type": "ice"},
            {**rect(1500, 500, 200, 40), "type": "solid"},
            {**rect(1700, 500, 1100, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 2900, 40), "type": "void"},
        ],
        "saws": [
            {"x": 550, "y": 470, "r": 16, "minX": 470, "maxX": 650, "speed": 173},
            {"x": 1250, "y": 470, "r": 16, "minX": 1150, "maxX": 1350, "speed": 182},
            {"x": 2100, "y": 470, "r": 16, "minX": 2000, "maxX": 2200, "speed": 190},
            {"x": 2500, "y": 470, "r": 16, "minX": 2400, "maxX": 2600, "speed": 198},
        ],
    },
    {
        "name": "Nivel 82 - La gran torre",
        "hint": "Una torre mas alta, un peligro en cada piso",
        "width": 1400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(1320, 160, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 100, 20), "type": "moving", "axis": "y", "minY": 380, "maxY": 500, "speed": 78},
            {**rect(300, 380, 400, 40), "type": "solid"},
            {**rect(700, 380, 100, 20), "type": "moving", "axis": "y", "minY": 260, "maxY": 380, "speed": 82},
            {**rect(700, 260, 150, 40), "type": "hidden_spike", "triggerX": 730, "delay": 0.329},
            {**rect(850, 260, 550, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 1500, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 500, "kind": "sky", "y": -80, "triggerX": 350, "delay": 0.588, "groundY": 380, "radius": 20, "blastRadius": 50},
        ],
    },
    {
        "name": "Nivel 83 - Rebote y sierra",
        "hint": "El resorte te sube, la sierra te espera arriba",
        "width": 2200,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2120, 240, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 100, 40), "type": "bounce"},
            {**rect(560, 420, 600, 40), "type": "solid"},
            {**rect(1160, 420, 100, 40), "type": "bounce"},
            {**rect(1420, 340, 780, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2300, 40), "type": "void"},
        ],
        "saws": [
            {"x": 850, "y": 390, "r": 16, "minX": 760, "maxX": 1000, "speed": 173},
            {"x": 1750, "y": 310, "r": 16, "minX": 1650, "maxX": 1900, "speed": 190},
        ],
    },
    {
        "name": "Nivel 84 - Piedra y vacio",
        "hint": "El vacio es mas ancho de lo que crees",
        "width": 2600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "stone"},
            {**rect(900, 500, 500, 40), "type": "stone"},
            {**rect(1700, 500, 900, 40), "type": "stone"},
        ],
        "hazards": [
            {**rect(-50, 620, 2700, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 350, "y": 460, "w": 50, "h": 40, "toX": 950, "toY": 440},
            {"x": 1250, "y": 460, "w": 50, "h": 40, "toX": 1750, "toY": 440},
        ],
    },
    {
        "name": "Nivel 85 - Portales dobles",
        "hint": "Dos portales y un resorte para terminar",
        "width": 2400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2320, 320, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(700, 500, 300, 40), "type": "solid"},
            {**rect(1400, 500, 100, 40), "type": "bounce"},
            {**rect(1660, 420, 740, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2500, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 250, "y": 460, "w": 50, "h": 40, "toX": 720, "toY": 440},
            {"x": 950, "y": 460, "w": 50, "h": 40, "toX": 1420, "toY": 440},
        ],
    },
    {
        "name": "Nivel 86 - Bloques y explosivos",
        "hint": "Bloques arriba, bombas al lado, nada tranquilo",
        "width": 2700,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2620, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 500, 40), "type": "solid"},
            {**rect(500, 500, 150, 40), "type": "hidden_bomb", "triggerX": 530, "delay": 0.352, "blastRadius": 58},
            {**rect(650, 500, 650, 40), "type": "solid"},
            {**rect(1300, 460, 200, 40), "type": "solid"},
            {**rect(1500, 500, 1200, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2800, 40), "type": "void"},
        ],
        "fallingBlocks": [
            {"x": 900, "y": -80, "w": 70, "h": 70, "triggerX": 770, "delay": 0.588, "groundY": 500},
        ],
        "bombs": [
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1600, "toX": 2100, "triggerX": 1850, "delay": 0.47, "speed": 248, "radius": 16},
            {"x": 2400, "kind": "sky", "y": -80, "triggerX": 2250, "delay": 0.529, "groundY": 500, "radius": 23, "blastRadius": 58},
        ],
    },
    {
        "name": "Nivel 87 - El hielo final",
        "hint": "El hielo final, sin margen para el error",
        "width": 2900,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2820, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "solid"},
            {**rect(400, 500, 600, 40), "type": "ice"},
            {**rect(1000, 460, 200, 40), "type": "solid"},
            {**rect(1200, 460, 600, 40), "type": "ice"},
            {**rect(1800, 500, 200, 40), "type": "solid"},
            {**rect(2000, 500, 900, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 3000, 40), "type": "void"},
        ],
        "saws": [
            {"x": 650, "y": 470, "r": 16, "minX": 550, "maxX": 850, "speed": 173},
            {"x": 1450, "y": 430, "r": 16, "minX": 1350, "maxX": 1650, "speed": 182},
        ],
        "wallSpikes": [
            {"x": 2400, "y": 430, "w": 24, "h": 70, "reach": 33, "triggerX": 2350, "delay": 0.493, "dir": 1},
        ],
    },
    {
        "name": "Nivel 88 - Corre y esconde",
        "hint": "No hay tiempo de pararse a mirar que pisas",
        "width": 2500,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2420, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 500, 40), "type": "solid"},
            {**rect(500, 500, 150, 40), "type": "hidden_bomb", "triggerX": 530, "delay": 0.352, "blastRadius": 58},
            {**rect(650, 500, 650, 40), "type": "solid"},
            {**rect(1300, 500, 150, 40), "type": "hidden_spike", "triggerX": 1330, "delay": 0.329},
            {**rect(1450, 500, 1050, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2600, 40), "type": "void"},
        ],
        "runWall": {"startX": -200, "speed": 128, "y": 0, "h": 620},
    },
    {
        "name": "Nivel 89 - Plataformas y portales",
        "hint": "Plataformas que se mueven, portales que cruzan",
        "width": 2400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2320, 240, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 480, 100, 20), "type": "moving", "axis": "x", "minX": 300, "maxX": 650, "speed": 95},
            {**rect(700, 500, 300, 40), "type": "solid"},
            {**rect(1400, 500, 300, 40), "type": "solid"},
            {**rect(1700, 500, 100, 20), "type": "moving", "axis": "y", "minY": 340, "maxY": 500, "speed": 78},
            {**rect(1700, 340, 700, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2500, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 950, "y": 460, "w": 50, "h": 40, "toX": 1420, "toY": 440},
        ],
    },
    {
        "name": "Nivel 90 - Ultimatum de bloques III",
        "hint": "El final de esta tanda: todo junto, otra vez",
        "width": 3300,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3220, 220, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "stone"},
            {**rect(350, 500, 400, 40), "type": "ice"},
            {**rect(750, 500, 150, 40), "type": "hidden_bomb", "triggerX": 780, "delay": 0.352, "blastRadius": 58},
            {**rect(900, 480, 100, 20), "type": "moving", "axis": "x", "minX": 900, "maxX": 1300, "speed": 99},
            {**rect(1350, 500, 450, 40), "type": "stone"},
            {**rect(1800, 500, 100, 40), "type": "bounce"},
            {**rect(2060, 420, 440, 40), "type": "ice"},
            {**rect(2500, 420, 100, 20), "type": "moving", "axis": "y", "minY": 320, "maxY": 420, "speed": 78},
            {**rect(2500, 320, 800, 40), "type": "stone"},
        ],
        "hazards": [
            {**rect(-50, 620, 3400, 40), "type": "void"},
        ],
        "fallingBlocks": [
            {"x": 600, "y": -80, "w": 70, "h": 70, "triggerX": 470, "delay": 0.588, "groundY": 500},
        ],
        "bombs": [
            {"x": 2280, "kind": "sky", "y": -80, "triggerX": 2150, "delay": 0.588, "groundY": 420, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 315, "dir": 1, "fromX": 2650, "toX": 3200, "triggerX": 2850, "delay": 0.47, "speed": 248, "radius": 18},
        ],
    },
]

# ---- Nivel 91-100: el ultimo tramo del mapa. Nivel 100 es el nodo final —
# no hay placeholders despues, el mapa termina ahi.
LEVELS += [
    {
        "name": "Nivel 91 - El desafio de hielo",
        "hint": "El hielo definitivo, sin piedad",
        "width": 3000,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2920, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "solid"},
            {**rect(400, 500, 600, 40), "type": "ice"},
            {**rect(1000, 460, 200, 40), "type": "solid"},
            {**rect(1200, 460, 700, 40), "type": "ice"},
            {**rect(1900, 500, 200, 40), "type": "solid"},
            {**rect(2100, 500, 900, 40), "type": "ice"},
        ],
        "hazards": [
            {**rect(-50, 620, 3100, 40), "type": "void"},
        ],
        "saws": [
            {"x": 650, "y": 470, "r": 16, "minX": 550, "maxX": 850, "speed": 173},
            {"x": 1450, "y": 430, "r": 16, "minX": 1350, "maxX": 1650, "speed": 182},
            {"x": 2400, "y": 470, "r": 16, "minX": 2300, "maxX": 2600, "speed": 190},
        ],
    },
    {
        "name": "Nivel 92 - Torres gemelas",
        "hint": "Dos torres, un mismo destino",
        "width": 2400,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2320, 160, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 100, 20), "type": "moving", "axis": "y", "minY": 380, "maxY": 500, "speed": 78},
            {**rect(300, 380, 400, 40), "type": "solid"},
            {**rect(700, 380, 100, 20), "type": "moving", "axis": "x", "minX": 700, "maxX": 1050, "speed": 95},
            {**rect(1100, 380, 300, 40), "type": "solid"},
            {**rect(1400, 380, 100, 20), "type": "moving", "axis": "y", "minY": 260, "maxY": 380, "speed": 82},
            {**rect(1400, 260, 1000, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2500, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 1700, "kind": "sky", "y": -80, "triggerX": 1550, "delay": 0.588, "groundY": 260, "radius": 21, "blastRadius": 54},
        ],
    },
    {
        "name": "Nivel 93 - Bombas sin fin",
        "hint": "Bombas por delante, por arriba y por el medio",
        "width": 3000,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2920, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 700, 40), "type": "solid"},
            {**rect(700, 460, 200, 40), "type": "solid"},
            {**rect(900, 500, 700, 40), "type": "solid"},
            {**rect(1600, 460, 200, 40), "type": "solid"},
            {**rect(1800, 500, 1200, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3100, 40), "type": "void"},
        ],
        "bombs": [
            {"x": 350, "kind": "sky", "y": -80, "triggerX": 200, "delay": 0.588, "groundY": 500, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 800, "toX": 1300, "triggerX": 1000, "delay": 0.47, "speed": 239, "radius": 16},
            {"x": 1950, "kind": "sky", "y": -80, "triggerX": 1800, "delay": 0.529, "groundY": 500, "radius": 23, "blastRadius": 58},
            {"kind": "side", "y": 495, "dir": -1, "fromX": 2900, "toX": 2300, "triggerX": 2600, "delay": 0.47, "speed": 264, "radius": 18},
            {"x": 2500, "kind": "sky", "y": -80, "triggerX": 2350, "delay": 0.529, "groundY": 500, "radius": 21, "blastRadius": 54},
        ],
    },
    {
        "name": "Nivel 94 - Rebote total",
        "hint": "Resortes sin parar, hasta el limite del cielo",
        "width": 2800,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2720, 90, 50, 100),
        "platforms": [
            {**rect(0, 500, 300, 40), "type": "solid"},
            {**rect(300, 500, 100, 40), "type": "bounce"},
            {**rect(560, 420, 300, 40), "type": "solid"},
            {**rect(860, 420, 100, 40), "type": "bounce"},
            {**rect(1120, 340, 300, 40), "type": "solid"},
            {**rect(1420, 340, 100, 40), "type": "bounce"},
            {**rect(1680, 260, 300, 40), "type": "solid"},
            {**rect(1980, 260, 100, 40), "type": "bounce"},
            {**rect(2240, 190, 560, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2900, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1250, "y": 310, "r": 15, "minX": 1150, "maxX": 1350, "speed": 173},
        ],
    },
    {
        "name": "Nivel 95 - El laberinto de portales",
        "hint": "Cinco portales, un laberinto sin suelo",
        "width": 3500,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3420, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 250, 40), "type": "solid"},
            {**rect(650, 500, 250, 40), "type": "solid"},
            {**rect(1300, 500, 250, 40), "type": "solid"},
            {**rect(1950, 500, 250, 40), "type": "solid"},
            {**rect(2600, 500, 250, 40), "type": "solid"},
            {**rect(3250, 500, 250, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 3600, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 200, "y": 460, "w": 50, "h": 40, "toX": 670, "toY": 440},
            {"x": 850, "y": 460, "w": 50, "h": 40, "toX": 1320, "toY": 440},
            {"x": 1500, "y": 460, "w": 50, "h": 40, "toX": 1970, "toY": 440},
            {"x": 2150, "y": 460, "w": 50, "h": 40, "toX": 2620, "toY": 440},
            {"x": 2800, "y": 460, "w": 50, "h": 40, "toX": 3270, "toY": 440},
        ],
    },
    {
        "name": "Nivel 96 - Piedra, hielo y fuego",
        "hint": "Piedra, hielo y fuego cruzado, todo en un tramo",
        "width": 2900,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2820, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "stone"},
            {**rect(400, 500, 400, 40), "type": "ice"},
            {**rect(800, 460, 200, 40), "type": "stone"},
            {**rect(1000, 460, 400, 40), "type": "ice"},
            {**rect(1400, 500, 300, 40), "type": "stone"},
            {**rect(1700, 500, 1200, 40), "type": "stone"},
        ],
        "hazards": [
            {**rect(-50, 620, 3000, 40), "type": "void"},
        ],
        "saws": [
            {"x": 1150, "y": 430, "r": 16, "minX": 1080, "maxX": 1320, "speed": 173},
        ],
        "bombs": [
            {"x": 600, "kind": "sky", "y": -80, "triggerX": 470, "delay": 0.588, "groundY": 500, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 495, "dir": 1, "fromX": 1800, "toX": 2300, "triggerX": 2050, "delay": 0.47, "speed": 248, "radius": 16},
            {"x": 2600, "kind": "sky", "y": -80, "triggerX": 2450, "delay": 0.529, "groundY": 500, "radius": 23, "blastRadius": 58},
        ],
    },
    {
        "name": "Nivel 97 - Sierras por doquier",
        "hint": "Sierras por todas partes, manten el ritmo",
        "width": 2600,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2520, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 2600, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2700, 40), "type": "void"},
        ],
        "saws": [
            {"x": 500, "y": 470, "r": 16, "minX": 420, "maxX": 620, "speed": 182},
            {"x": 1000, "y": 470, "r": 16, "minX": 920, "maxX": 1120, "speed": 190},
            {"x": 1500, "y": 470, "r": 16, "minX": 1420, "maxX": 1620, "speed": 198},
            {"x": 2000, "y": 470, "r": 16, "minX": 1920, "maxX": 2120, "speed": 206},
        ],
    },
    {
        "name": "Nivel 98 - Corre hasta el final",
        "hint": "El ultimo tramo de sombra, el mas largo",
        "width": 2800,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(2720, 400, 50, 100),
        "platforms": [
            {**rect(0, 500, 2800, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 2900, 40), "type": "void"},
        ],
        "saws": [
            {"x": 900, "y": 470, "r": 16, "minX": 820, "maxX": 1020, "speed": 190},
            {"x": 2000, "y": 470, "r": 16, "minX": 1920, "maxX": 2120, "speed": 206},
        ],
        "wallSpikes": [
            {"x": 1500, "y": 390, "w": 24, "h": 70, "reach": 33, "triggerX": 1450, "delay": 0.493, "dir": 1},
        ],
        "runWall": {"startX": -200, "speed": 136, "y": 0, "h": 620},
    },
    {
        "name": "Nivel 99 - La antesala final",
        "hint": "Todo lo que aprendiste, una vez mas, antes del final",
        "width": 3200,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3120, 320, 50, 100),
        "platforms": [
            {**rect(0, 500, 350, 40), "type": "stone"},
            {**rect(350, 500, 400, 40), "type": "ice"},
            {**rect(750, 500, 150, 40), "type": "hidden_bomb", "triggerX": 780, "delay": 0.352, "blastRadius": 58},
            {**rect(900, 480, 100, 20), "type": "moving", "axis": "x", "minX": 900, "maxX": 1300, "speed": 99},
            {**rect(1350, 500, 450, 40), "type": "stone"},
            {**rect(1800, 500, 100, 40), "type": "bounce"},
            {**rect(2060, 420, 440, 40), "type": "ice"},
            {**rect(2950, 420, 250, 40), "type": "stone"},
        ],
        "hazards": [
            {**rect(-50, 620, 3300, 40), "type": "void"},
        ],
        "teleporters": [
            {"x": 2450, "y": 380, "w": 50, "h": 40, "toX": 3000, "toY": 360},
        ],
        "saws": [
            {"x": 1600, "y": 470, "r": 15, "minX": 1400, "maxX": 1700, "speed": 182},
        ],
    },
    {
        "name": "Nivel 100 - El Final",
        "hint": "Todo lo que aprendiste, todo junto, por ultima vez",
        "width": 4000,
        "spawn": {"x": 60, "y": 440},
        "goal": rect(3920, 180, 50, 100),
        "platforms": [
            {**rect(0, 500, 400, 40), "type": "solid"},
            {**rect(400, 500, 150, 40), "type": "hidden_spike", "triggerX": 430, "delay": 0.329},
            {**rect(550, 500, 400, 40), "type": "ice"},
            {**rect(950, 460, 200, 40), "type": "solid"},
            {**rect(1150, 460, 150, 40), "type": "hidden_bomb", "triggerX": 1180, "delay": 0.352, "blastRadius": 58},
            {**rect(1300, 460, 500, 40), "type": "stone"},
            {**rect(1800, 440, 100, 20), "type": "moving", "axis": "x", "minX": 1800, "maxX": 2200, "speed": 99},
            {**rect(2250, 460, 450, 40), "type": "stone"},
            {**rect(2700, 460, 100, 40), "type": "bounce"},
            {**rect(2960, 380, 440, 40), "type": "ice"},
            {**rect(3400, 380, 100, 20), "type": "moving", "axis": "y", "minY": 280, "maxY": 380, "speed": 78},
            {**rect(3400, 280, 600, 40), "type": "solid"},
        ],
        "hazards": [
            {**rect(-50, 620, 4100, 40), "type": "void"},
        ],
        "fallingBlocks": [
            {"x": 700, "y": -80, "w": 70, "h": 70, "triggerX": 570, "delay": 0.588, "groundY": 500},
        ],
        "bombs": [
            {"x": 2450, "kind": "sky", "y": -80, "triggerX": 2300, "delay": 0.588, "groundY": 460, "radius": 21, "blastRadius": 54},
            {"kind": "side", "y": 455, "dir": 1, "fromX": 1350, "toX": 1750, "triggerX": 1550, "delay": 0.47, "speed": 239, "radius": 16},
            {"kind": "side", "y": 275, "dir": 1, "fromX": 3300, "toX": 3700, "triggerX": 3500, "delay": 0.47, "speed": 248, "radius": 18},
        ],
        "saws": [
            {"x": 3150, "y": 350, "r": 15, "minX": 3050, "maxX": 3250, "speed": 182},
        ],
        "wallSpikes": [
            {"x": 3800, "y": 230, "w": 24, "h": 70, "reach": 33, "triggerX": 3750, "delay": 0.493, "dir": 1},
        ],
    },
]


def shifted_level(index: int) -> dict:
    level = deepcopy(LEVELS[index])
    level["spawn"]["y"] -= GROUND_LIFT
    level["goal"]["y"] -= GROUND_LIFT
    for platform in level.get("platforms", []):
        platform["y"] -= GROUND_LIFT
        if platform.get("type") == "moving" and platform.get("axis") == "y":
            if "minY" in platform:
                platform["minY"] -= GROUND_LIFT
            if "maxY" in platform:
                platform["maxY"] -= GROUND_LIFT
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
