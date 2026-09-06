package com.bfjstudios.nottroll.entities;

public class PlatformInst {
    public float x, y, w, h;
    public String type = "solid";

    // optional template fields
    public float triggerX = Float.NaN;
    public float delay;
    public float power = 950f;
    public String axis = "x";
    public float minX, maxX, minY, maxY, speed;
    public float blastRadius = 70f;

    // runtime state (reset on each attempt)
    public boolean triggered;
    public float t;
    public boolean gone;
    public boolean poppedUp;
    public float spikeW = 40f;
    public float spikeX;
    public boolean falling;
    public float fallVy;
    public int dir = 1;

    public PlatformInst copyForReset() {
        PlatformInst p = new PlatformInst();
        p.x = x; p.y = y; p.w = w; p.h = h; p.type = type;
        p.triggerX = triggerX; p.delay = delay; p.power = power;
        p.axis = axis; p.minX = minX; p.maxX = maxX; p.minY = minY; p.maxY = maxY; p.speed = speed;
        p.blastRadius = blastRadius;
        p.spikeW = spikeW;
        p.spikeX = "hidden_spike".equals(type) ? x + w / 2f - p.spikeW / 2f : 0;
        p.triggered = false;
        p.t = 0;
        p.gone = false;
        p.poppedUp = false;
        p.falling = false;
        p.fallVy = 0;
        p.dir = 1;
        return p;
    }

    public boolean isSolid() {
        return !gone && !"fake_floor".equals(type);
    }
}
