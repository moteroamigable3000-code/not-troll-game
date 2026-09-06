package com.bfjstudios.nottroll.entities;

public class RunWallInst {
    public float startX, y, h, speed;
    public float x;

    public RunWallInst copyForReset() {
        RunWallInst r = new RunWallInst();
        r.startX = startX; r.y = y; r.h = h; r.speed = speed; r.x = startX;
        return r;
    }
}
