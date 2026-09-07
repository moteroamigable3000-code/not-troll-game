package com.bfjstudios.nottroll.entities;

public class FallingBlockInst {
    public boolean ceilingSpikes;
    public float triggerY = Float.NaN, triggerH;
    public int triggerDir = 1;
    public float x, y, w, h, triggerX, delay, groundY;

    public String state = "idle"; // idle | warn | falling | landed
    public float t;
    public float curY;
    public float vy;
    public boolean gone;

    public FallingBlockInst copyForReset() {
        FallingBlockInst b = new FallingBlockInst();
        b.ceilingSpikes = ceilingSpikes;
        b.triggerY = triggerY; b.triggerH = triggerH; b.triggerDir = triggerDir;
        b.x = x; b.y = y; b.w = w; b.h = h; b.triggerX = triggerX; b.delay = delay; b.groundY = groundY;
        b.state = "idle"; b.t = 0; b.curY = y; b.vy = 0; b.gone = false;
        return b;
    }
}
