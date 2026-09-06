package com.bfjstudios.nottroll.entities;

public class Player {
    public float x, y;
    public float w = 26, h = 36;
    public float vx, vy;
    public boolean onGround;
    public int facing = 1;
    public boolean dead;
    public boolean falling;
    public float coyote;
    public float jumpBuffer;
    public float squashX = 1, squashY = 1;
    public float animTime;
    public float rotation;
    public float teleportCooldown;
    public String groundType;
    public PlatformInst groundPlatform;
    public boolean bounced;
}
