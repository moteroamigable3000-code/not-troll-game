package com.bfjstudios.nottroll.entities;

import com.badlogic.gdx.graphics.Color;

public class Particle {
    public float x, y, vx, vy;
    public float life, maxLife;
    public Color color;
    public float size;
    public String type; // spark | dust | debris
    public float rot, rotSpeed;
    public float gravity;
}
