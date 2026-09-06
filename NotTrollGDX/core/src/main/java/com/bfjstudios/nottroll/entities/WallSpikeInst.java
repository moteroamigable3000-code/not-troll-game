package com.bfjstudios.nottroll.entities;

public class WallSpikeInst {
    public float x, y, w, h, reach, triggerX, delay;
    public int dir = 1;

    public boolean triggered;
    public float t;
    public float extend;

    public WallSpikeInst copyForReset() {
        WallSpikeInst w = new WallSpikeInst();
        w.x = x; w.y = y; w.w = this.w; w.h = h; w.reach = reach; w.triggerX = triggerX; w.delay = delay; w.dir = dir;
        w.triggered = false; w.t = 0; w.extend = 0;
        return w;
    }
}
