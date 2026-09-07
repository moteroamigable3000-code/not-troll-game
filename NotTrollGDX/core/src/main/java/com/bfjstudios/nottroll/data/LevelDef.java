package com.bfjstudios.nottroll.data;

import com.badlogic.gdx.utils.Array;
import com.bfjstudios.nottroll.entities.BombInst;
import com.bfjstudios.nottroll.entities.FallingBlockInst;
import com.bfjstudios.nottroll.entities.HazardInst;
import com.bfjstudios.nottroll.entities.PlatformInst;
import com.bfjstudios.nottroll.entities.RunWallInst;
import com.bfjstudios.nottroll.entities.SawInst;
import com.bfjstudios.nottroll.entities.TeleporterInst;
import com.bfjstudios.nottroll.entities.WallSpikeInst;

/** Immutable template for a level, parsed once from levels.json. */
public class LevelDef {
    public String name;
    public String hint;
    public boolean chasingGhost;
    public float ghostSpeed, ghostCatchupSpeed, ghostDelay, ghostStartDistance;
    public float width;
    public float height;
    public boolean verticalCamera;
    public float[] routeFloors;
    public float spawnX, spawnY;
    public float goalX, goalY, goalW, goalH;
    public boolean locked;

    public final Array<PlatformInst> platforms = new Array<>();
    public final Array<HazardInst> hazards = new Array<>();
    public final Array<SawInst> saws = new Array<>();
    public final Array<WallSpikeInst> wallSpikes = new Array<>();
    public final Array<FallingBlockInst> fallingBlocks = new Array<>();
    public final Array<BombInst> bombs = new Array<>();
    public final Array<TeleporterInst> teleporters = new Array<>();
    public RunWallInst runWall; // nullable
}
