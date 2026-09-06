package com.bfjstudios.nottroll.entities;

public class BombInst {
    public String kind = "sky"; // sky | side
    public float x, y, triggerX, delay, groundY, radius = 20, blastRadius;
    public int dir = 1;
    public float fromX, toX, speed;

    public String state = "idle"; // idle | warn | active
    public float t;
    public float curX, curY, vy;
    public boolean gone;

    public BombInst copyForReset() {
        BombInst b = new BombInst();
        b.kind = kind; b.x = x; b.y = y; b.triggerX = triggerX; b.delay = delay; b.groundY = groundY;
        b.radius = radius; b.blastRadius = blastRadius; b.dir = dir; b.fromX = fromX; b.toX = toX; b.speed = speed;
        b.state = "idle"; b.t = 0;
        b.curX = "side".equals(kind) ? fromX : x;
        b.curY = y;
        b.vy = 0; b.gone = false;
        return b;
    }
}
