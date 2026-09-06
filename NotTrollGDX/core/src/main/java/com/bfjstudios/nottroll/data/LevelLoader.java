package com.bfjstudios.nottroll.data;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.utils.Array;
import com.badlogic.gdx.utils.JsonReader;
import com.badlogic.gdx.utils.JsonValue;
import com.bfjstudios.nottroll.entities.BombInst;
import com.bfjstudios.nottroll.entities.FallingBlockInst;
import com.bfjstudios.nottroll.entities.HazardInst;
import com.bfjstudios.nottroll.entities.PlatformInst;
import com.bfjstudios.nottroll.entities.RunWallInst;
import com.bfjstudios.nottroll.entities.SawInst;
import com.bfjstudios.nottroll.entities.TeleporterInst;
import com.bfjstudios.nottroll.entities.WallSpikeInst;

public final class LevelLoader {
    private LevelLoader() {}

    public static Array<LevelDef> loadAll(String internalPath) {
        JsonValue root = new JsonReader().parse(Gdx.files.internal(internalPath));
        Array<LevelDef> out = new Array<>();
        JsonValue levels = root.get("levels");
        JsonValue meta = root.get("meta");
        int i = 0;
        for (JsonValue lv = levels.child; lv != null; lv = lv.next, i++) {
            LevelDef def = new LevelDef();
            def.name = lv.getString("name", "Nivel " + (i + 1));
            def.hint = lv.getString("hint", "");
            def.width = lv.getFloat("width");
            JsonValue spawn = lv.get("spawn");
            def.spawnX = spawn.getFloat("x");
            def.spawnY = spawn.getFloat("y");
            JsonValue goal = lv.get("goal");
            def.goalX = goal.getFloat("x");
            def.goalY = goal.getFloat("y");
            def.goalW = goal.getFloat("w");
            def.goalH = goal.getFloat("h");

            JsonValue platforms = lv.get("platforms");
            if (platforms != null) {
                for (JsonValue p = platforms.child; p != null; p = p.next) {
                    PlatformInst pl = new PlatformInst();
                    pl.x = p.getFloat("x"); pl.y = p.getFloat("y");
                    pl.w = p.getFloat("w"); pl.h = p.getFloat("h");
                    pl.type = p.getString("type", "solid");
                    pl.triggerX = p.getFloat("triggerX", Float.NaN);
                    pl.delay = p.getFloat("delay", 0);
                    pl.power = p.getFloat("power", 950);
                    pl.axis = p.getString("axis", "x");
                    pl.minX = p.getFloat("minX", 0);
                    pl.maxX = p.getFloat("maxX", 0);
                    pl.minY = p.getFloat("minY", 0);
                    pl.maxY = p.getFloat("maxY", 0);
                    pl.speed = p.getFloat("speed", 0);
                    pl.blastRadius = p.getFloat("blastRadius", 70);
                    pl.spikeW = p.getFloat("spikeW", 40);
                    def.platforms.add(pl);
                }
            }

            JsonValue hazards = lv.get("hazards");
            if (hazards != null) {
                for (JsonValue h = hazards.child; h != null; h = h.next) {
                    HazardInst hz = new HazardInst();
                    hz.x = h.getFloat("x"); hz.y = h.getFloat("y");
                    hz.w = h.getFloat("w"); hz.h = h.getFloat("h");
                    hz.type = h.getString("type");
                    def.hazards.add(hz);
                }
            }

            JsonValue saws = lv.get("saws");
            if (saws != null) {
                for (JsonValue s = saws.child; s != null; s = s.next) {
                    SawInst sw = new SawInst();
                    sw.x = s.getFloat("x"); sw.y = s.getFloat("y"); sw.r = s.getFloat("r");
                    sw.minX = s.getFloat("minX"); sw.maxX = s.getFloat("maxX"); sw.speed = s.getFloat("speed");
                    def.saws.add(sw);
                }
            }

            JsonValue wallSpikes = lv.get("wallSpikes");
            if (wallSpikes != null) {
                for (JsonValue w = wallSpikes.child; w != null; w = w.next) {
                    WallSpikeInst ws = new WallSpikeInst();
                    ws.x = w.getFloat("x"); ws.y = w.getFloat("y"); ws.w = w.getFloat("w"); ws.h = w.getFloat("h");
                    ws.reach = w.getFloat("reach", 90);
                    ws.triggerX = w.getFloat("triggerX");
                    ws.delay = w.getFloat("delay", 0);
                    ws.dir = w.getInt("dir", 1);
                    def.wallSpikes.add(ws);
                }
            }

            JsonValue fallingBlocks = lv.get("fallingBlocks");
            if (fallingBlocks != null) {
                for (JsonValue b = fallingBlocks.child; b != null; b = b.next) {
                    FallingBlockInst fb = new FallingBlockInst();
                    fb.x = b.getFloat("x"); fb.y = b.getFloat("y"); fb.w = b.getFloat("w"); fb.h = b.getFloat("h");
                    fb.triggerX = b.getFloat("triggerX");
                    fb.delay = b.getFloat("delay", 0);
                    fb.groundY = b.getFloat("groundY");
                    def.fallingBlocks.add(fb);
                }
            }

            JsonValue bombs = lv.get("bombs");
            if (bombs != null) {
                for (JsonValue b = bombs.child; b != null; b = b.next) {
                    BombInst bm = new BombInst();
                    bm.kind = b.getString("kind", "sky");
                    bm.x = b.getFloat("x", 0);
                    bm.y = b.getFloat("y");
                    bm.triggerX = b.getFloat("triggerX");
                    bm.delay = b.getFloat("delay", 0);
                    bm.groundY = b.getFloat("groundY", 0);
                    bm.radius = b.getFloat("radius", 20);
                    bm.blastRadius = b.getFloat("blastRadius", bm.radius * 1.8f);
                    bm.dir = b.getInt("dir", 1);
                    bm.fromX = b.getFloat("fromX", 0);
                    bm.toX = b.getFloat("toX", 0);
                    bm.speed = b.getFloat("speed", 0);
                    def.bombs.add(bm);
                }
            }

            JsonValue teleporters = lv.get("teleporters");
            if (teleporters != null) {
                for (JsonValue t = teleporters.child; t != null; t = t.next) {
                    TeleporterInst tp = new TeleporterInst();
                    tp.x = t.getFloat("x"); tp.y = t.getFloat("y"); tp.w = t.getFloat("w"); tp.h = t.getFloat("h");
                    tp.toX = t.getFloat("toX"); tp.toY = t.getFloat("toY");
                    def.teleporters.add(tp);
                }
            }

            JsonValue runWall = lv.get("runWall");
            if (runWall != null) {
                RunWallInst rw = new RunWallInst();
                rw.startX = runWall.getFloat("startX");
                rw.y = runWall.getFloat("y");
                rw.h = runWall.getFloat("h");
                rw.speed = runWall.getFloat("speed");
                def.runWall = rw;
            }

            out.add(def);
        }

        // apply "locked" flag from meta (future levels marked locked server-side)
        if (meta != null) {
            int mi = 0;
            for (JsonValue m = meta.child; m != null; m = m.next, mi++) {
                if (mi < out.size) out.get(mi).locked = m.getBoolean("locked", false);
            }
        }

        return out;
    }
}
