package com.bfjstudios.nottroll.entities;

public class SawInst {
    public float x, y, r, minX, maxX, speed;
    public int dir = 1;

    public SawInst copyForReset() {
        SawInst s = new SawInst();
        s.x = x; s.y = y; s.r = r; s.minX = minX; s.maxX = maxX; s.speed = speed; s.dir = 1;
        return s;
    }
}
