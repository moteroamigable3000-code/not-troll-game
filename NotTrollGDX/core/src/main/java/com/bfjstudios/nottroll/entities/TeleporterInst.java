package com.bfjstudios.nottroll.entities;

public class TeleporterInst {
    public float x, y, w, h, toX, toY;

    public TeleporterInst copyForReset() {
        TeleporterInst t = new TeleporterInst();
        t.x = x; t.y = y; t.w = w; t.h = h; t.toX = toX; t.toY = toY;
        return t;
    }
}
