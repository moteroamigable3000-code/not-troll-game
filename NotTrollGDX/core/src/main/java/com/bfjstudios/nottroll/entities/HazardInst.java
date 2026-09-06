package com.bfjstudios.nottroll.entities;

public class HazardInst {
    public float x, y, w, h;
    public String type;

    public HazardInst copyForReset() {
        HazardInst copy = new HazardInst();
        copy.x = x; copy.y = y; copy.w = w; copy.h = h; copy.type = type;
        return copy;
    }
}
