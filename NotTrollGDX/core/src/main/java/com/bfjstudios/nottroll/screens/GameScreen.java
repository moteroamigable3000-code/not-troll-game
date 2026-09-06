package com.bfjstudios.nottroll.screens;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Input;
import com.badlogic.gdx.InputAdapter;
import com.badlogic.gdx.ScreenAdapter;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.g2d.TextureRegion;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import com.badlogic.gdx.math.MathUtils;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.ui.Image;
import com.badlogic.gdx.scenes.scene2d.ui.Label;
import com.badlogic.gdx.scenes.scene2d.ui.TextButton;
import com.badlogic.gdx.scenes.scene2d.utils.ClickListener;
import com.badlogic.gdx.scenes.scene2d.utils.TextureRegionDrawable;
import com.badlogic.gdx.scenes.scene2d.InputEvent;
import com.badlogic.gdx.scenes.scene2d.InputListener;
import com.badlogic.gdx.utils.Align;
import com.badlogic.gdx.utils.Array;
import com.badlogic.gdx.utils.viewport.FitViewport;
import com.badlogic.gdx.utils.viewport.Viewport;
import com.bfjstudios.nottroll.Constants;
import com.bfjstudios.nottroll.NotTrollGame;
import com.bfjstudios.nottroll.UiSkin;
import com.bfjstudios.nottroll.data.LevelDef;
import com.bfjstudios.nottroll.entities.BombInst;
import com.bfjstudios.nottroll.entities.FallingBlockInst;
import com.bfjstudios.nottroll.entities.HazardInst;
import com.bfjstudios.nottroll.entities.Particle;
import com.bfjstudios.nottroll.entities.PlatformInst;
import com.bfjstudios.nottroll.entities.Player;
import com.bfjstudios.nottroll.entities.RunWallInst;
import com.bfjstudios.nottroll.entities.SawInst;
import com.bfjstudios.nottroll.entities.TeleporterInst;
import com.bfjstudios.nottroll.entities.WallSpikeInst;

import java.util.Iterator;

public class GameScreen extends ScreenAdapter {
    private final NotTrollGame game;

    private final OrthographicCamera worldCamera = new OrthographicCamera();
    private final Viewport worldViewport;
    private final ShapeRenderer shapes;

    private final Stage hud;
    private Label levelLabel, deathLabel, overlayTitle, overlaySub;
    private Image progressTrack, progressFill;
    private TouchButtonActor touchLeft, touchRight, touchJump;

    private int levelIndex;
    private LevelDef levelDef;

    private Player player;
    private final Array<PlatformInst> platforms = new Array<>();
    private final Array<SawInst> saws = new Array<>();
    private final Array<WallSpikeInst> wallSpikes = new Array<>();
    private final Array<FallingBlockInst> fallingBlocks = new Array<>();
    private final Array<BombInst> bombs = new Array<>();
    private final Array<TeleporterInst> teleporters = new Array<>();
    private RunWallInst runWall;
    private final Array<Particle> particles = new Array<>();
    private final Array<float[]> stars = new Array<>(); // x, y, r, twinkle
    private final Array<float[]> portalMotes = new Array<>(); // angle, radius, speed, bob, size, colorIdx

    private String state = "intro"; // intro | playing | dead | complete
    private float stateTimer;
    private float flash;
    private float camX, camTarget;
    private float shakeT, shakeMag;
    private float portalCx, portalCy, pullStartX, pullStartY;
    private float completeDuration = 1.1f;
    private boolean advancingLevel;
    private int deaths;
    private float sawSpin;
    private float bgAnimT;

    private boolean touchLeftDown, touchRightDown, touchJumpHeld;
    private boolean touchJumpJustPressed;

    private static final Color COL_SOLID = new Color(0x4a7a3dff);
    private static final Color COL_SOLID_TOP = new Color(0x5f9950ff);
    private static final Color COL_ICE = new Color(0xbfe9ffff);
    private static final Color COL_ICE_TOP = new Color(0xeaf9ffff);
    private static final Color COL_BOUNCE = new Color(0xf7b733ff);
    private static final Color COL_BOUNCE_TOP = new Color(0xffe08aff);
    private static final Color COL_MOVING = new Color(0x7d8596ff);
    private static final Color COL_MOVING_TOP = new Color(0xa8b0c2ff);
    private static final Color COL_STONE = new Color(0x6b6f76ff);
    private static final Color COL_STONE_TOP = new Color(0x888e99ff);
    private static final Color COL_CRUMBLE = new Color(0x8b5a2bff);
    private static final Color COL_CRUMBLE_TRIG = new Color(0xa86a3dff);
    private static final Color COL_SPIKE = new Color(0xd63b3bff);
    private static final Color COL_VOID_DUMMY = new Color(0, 0, 0, 0);

    public GameScreen(NotTrollGame game, int levelIndex) {
        this.game = game;
        worldViewport = new FitViewport(Constants.W, Constants.H, worldCamera);
        worldCamera.setToOrtho(true, Constants.W, Constants.H);
        shapes = new ShapeRenderer();

        hud = new Stage(new FitViewport(Constants.W, Constants.H));
        buildHud();

        loadLevel(levelIndex);
    }

    // ---------------------------------------------------------------- setup

    private void buildHud() {
        levelLabel = new Label("", game.uiSkin.skin, "hud");
        levelLabel.setColor(UiSkin.GOLD);
        levelLabel.setPosition(14, Constants.H - 28);
        hud.addActor(levelLabel);

        deathLabel = new Label("", game.uiSkin.skin, "hud");
        deathLabel.setColor(UiSkin.RED);
        deathLabel.setPosition(14, Constants.H - 50);
        hud.addActor(deathLabel);

        TextButton mapBtn = smallButton("Mapa (Esc)", () -> {
            game.setScreen(new LevelMapScreen(game, GameScreen.this));
        });
        TextButton optionsBtn = smallButton("Opciones", () -> {
            game.setScreen(new OptionsScreen(game, GameScreen.this));
        });
        TextButton restartBtn = smallButton("Reiniciar (R)", this::restartLevel);

        float gap = 10f;
        float y = Constants.H - 42;
        float x = Constants.W - 16;
        for (TextButton b : new TextButton[]{restartBtn, optionsBtn, mapBtn}) {
            x -= b.getWidth();
            b.setPosition(x, y);
            x -= gap;
        }
        hud.addActor(mapBtn);
        hud.addActor(optionsBtn);
        hud.addActor(restartBtn);

        progressTrack = colorImage(Color.valueOf("1a1626ff"));
        progressTrack.setBounds(0, Constants.H - 8, Constants.W, 8);
        hud.addActor(progressTrack);
        progressFill = colorImage(UiSkin.GOLD);
        progressFill.setBounds(0, Constants.H - 8, 0, 8);
        hud.addActor(progressFill);

        overlayTitle = new Label("", game.uiSkin.skin, "h1");
        overlayTitle.setAlignment(Align.center);
        overlayTitle.setWidth(Constants.W);
        overlayTitle.setPosition(0, Constants.H / 2f + 10);
        hud.addActor(overlayTitle);

        overlaySub = new Label("", game.uiSkin.skin, "body");
        overlaySub.setColor(UiSkin.GOLD);
        overlaySub.setAlignment(Align.center);
        overlaySub.setWidth(Constants.W);
        overlaySub.setPosition(0, Constants.H / 2f - 30);
        hud.addActor(overlaySub);

        touchLeft = touchButton(20, 20, 92, 64, TouchButtonActor.Kind.LEFT);
        touchRight = touchButton(118, 20, 92, 64, TouchButtonActor.Kind.RIGHT);
        touchJump = touchButton(Constants.W - 122, 20, 102, 74, TouchButtonActor.Kind.JUMP);

        touchLeft.addListener(holdListener(down -> { touchLeft.pressed = down; touchLeftDown = down; }));
        touchRight.addListener(holdListener(down -> { touchRight.pressed = down; touchRightDown = down; }));
        touchJump.addListener(holdListener(down -> {
            touchJump.pressed = down;
            if (down && !touchJumpHeld) touchJumpJustPressed = true;
            touchJumpHeld = down;
        }));
    }

    private interface BoolConsumer { void accept(boolean v); }

    private InputListener holdListener(BoolConsumer onChange) {
        return new InputListener() {
            @Override
            public boolean touchDown(InputEvent event, float x, float y, int pointer, int button) {
                onChange.accept(true);
                return true;
            }

            @Override
            public void touchUp(InputEvent event, float x, float y, int pointer, int button) {
                onChange.accept(false);
            }
        };
    }

    private TouchButtonActor touchButton(float x, float y, float w, float h, TouchButtonActor.Kind kind) {
        TouchButtonActor btn = new TouchButtonActor(kind, shapes);
        btn.setBounds(x, y, w, h);
        hud.addActor(btn);
        return btn;
    }

    private Image colorImage(Color c) {
        Image img = new Image(new TextureRegionDrawable(new TextureRegion(game.assets.pixel)));
        img.setColor(c);
        return img;
    }

    private TextButton smallButton(String text, Runnable action) {
        TextButton btn = new TextButton(text, game.uiSkin.skin, "hud");
        com.badlogic.gdx.graphics.g2d.GlyphLayout layout = new com.badlogic.gdx.graphics.g2d.GlyphLayout(game.assets.pxTiny, text);
        btn.setSize(layout.width + 28, 36);
        btn.addListener(new ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                game.sfx.click();
                action.run();
            }
        });
        return btn;
    }

    // ------------------------------------------------------------ level load

    private void loadLevel(int index) {
        advancingLevel = false;
        this.levelIndex = index;
        levelDef = game.assets.levels.get(index);
        deaths = 0;
        if (index == 0) game.totalDeaths = 0;

        levelLabel.setText(levelDef.name);
        deathLabel.setText("Muertes: 0");
        progressFill.setWidth(0);

        stars.clear();
        int starCount = (int) (levelDef.width / 40f);
        for (int i = 0; i < starCount; i++) {
            stars.add(new float[]{
                MathUtils.random() * levelDef.width * 1.4f,
                MathUtils.random() * Constants.H * 0.55f,
                MathUtils.random() * 1.6f + 0.4f,
                MathUtils.random() * MathUtils.PI2
            });
        }

        portalMotes.clear();
        for (int i = 0; i < 16; i++) {
            portalMotes.add(new float[]{
                MathUtils.random() * MathUtils.PI2,
                34 + MathUtils.random() * 44,
                (0.5f + MathUtils.random() * 1.1f) * (MathUtils.randomBoolean() ? 1 : -1),
                MathUtils.random() * MathUtils.PI2,
                1.2f + MathUtils.random() * 2.2f,
                i % 3
            });
        }

        resetEntities();
        showIntro();
    }

    private void resetEntities() {
        player = new Player();
        player.x = levelDef.spawnX;
        player.y = levelDef.spawnY;

        camX = player.x - Constants.W / 2f;
        camTarget = camX;
        particles.clear();
        shakeT = 0; shakeMag = 0;
        flash = 0;

        platforms.clear();
        for (PlatformInst p : levelDef.platforms) platforms.add(p.copyForReset());

        saws.clear();
        for (SawInst s : levelDef.saws) saws.add(s.copyForReset());

        wallSpikes.clear();
        for (WallSpikeInst w : levelDef.wallSpikes) wallSpikes.add(w.copyForReset());

        fallingBlocks.clear();
        for (FallingBlockInst b : levelDef.fallingBlocks) fallingBlocks.add(b.copyForReset());

        bombs.clear();
        for (BombInst b : levelDef.bombs) bombs.add(b.copyForReset());

        teleporters.clear();
        for (TeleporterInst t : levelDef.teleporters) teleporters.add(t.copyForReset());

        runWall = levelDef.runWall != null ? levelDef.runWall.copyForReset() : null;
    }

    private void restartLevel() {
        if (levelDef == null) return;
        deaths++;
        game.totalDeaths++;
        deathLabel.setText("Muertes: " + deaths);
        resetEntities();
        state = "playing";
        overlayTitle.getColor().a = 0f;
        overlaySub.getColor().a = 0f;
    }

    private void showIntro() {
        state = "intro";
        stateTimer = 1.3f;
        overlayTitle.setText(levelDef.name);
        overlaySub.setText(levelDef.hint != null ? levelDef.hint : "");
        overlayTitle.getColor().a = 1f;
        overlaySub.getColor().a = 1f;
    }

    // ----------------------------------------------------------------- show

    @Override
    public void show() {
        Gdx.input.setInputProcessor(hud);
    }

    @Override
    public void resize(int width, int height) {
        worldViewport.update(width, height, false);
        hud.getViewport().update(width, height, true);
    }

    // --------------------------------------------------------------- update

    @Override
    public void render(float delta) {
        float dt = Math.min(delta, 0.05f);
        update(dt);
        renderWorld();

        boolean pausedForOverlay = false; // this screen only renders while active/unpaused
        game.sfx.updateMusic(false, "playing".equals(state) && !pausedForOverlay);

        hud.act(dt);
        hud.draw();

        if (Gdx.input.isKeyJustPressed(Input.Keys.ESCAPE) || Gdx.input.isKeyJustPressed(Input.Keys.BACK)) {
            game.setScreen(new LevelMapScreen(game, this));
        }
        if (Gdx.input.isKeyJustPressed(Input.Keys.R)) {
            restartLevel();
        }
    }

    private void update(float dt) {
        if (shakeT > 0) {
            shakeT -= dt;
            if (shakeT <= 0) shakeMag = 0;
        }
        flash = Math.max(0, flash - dt * 1.8f);
        bgAnimT += dt;
        sawSpin += dt;

        if ("intro".equals(state)) {
            stateTimer -= dt;
            float elapsed = 1.3f - stateTimer;
            float alpha;
            if (elapsed < 0.2f) alpha = elapsed / 0.2f;
            else if (stateTimer < 0.35f) alpha = Math.max(0, stateTimer / 0.35f);
            else alpha = 1f;
            overlayTitle.getColor().a = alpha;
            overlaySub.getColor().a = alpha;
            if (stateTimer <= 0) {
                state = "playing";
                overlayTitle.getColor().a = 0f;
                overlaySub.getColor().a = 0f;
            }
            return;
        }
        if ("complete".equals(state)) {
            float progress = Math.min(1, 1 - stateTimer / completeDuration);
            float ease = progress * progress;
            player.x = pullStartX + (portalCx - player.w / 2f - pullStartX) * ease;
            player.y = pullStartY + (portalCy - player.h / 2f - pullStartY) * ease;
            player.squashX = player.squashY = Math.max(0, 1 - progress * 1.15f);
            player.rotation += dt * 16f;
            player.falling = false;
            if (MathUtils.random() < 0.7f) spawnPortalPull(portalCx, portalCy);
            updateParticles(dt);
            stateTimer -= dt;
            if (stateTimer <= 0) advanceAfterComplete();
            return;
        }
        if ("dead".equals(state)) {
            updateParticles(dt);
            stateTimer -= dt;
            if (stateTimer <= 0) restartLevel();
            return;
        }

        updatePlayer(dt);
        updateTraps(dt);
        updateMovingPlatforms(dt);
        updateSaws(dt);
        updateWallSpikes(dt);
        updateFallingBlocks(dt);
        updateBombs(dt);
        updateTeleporters(dt);
        updateRunWall(dt);
        updateParticles(dt);
        checkHazards();
        checkGoal();

        camTarget = Math.max(0, Math.min(player.x - Constants.W / 2f + player.facing * 40, levelDef.width - Constants.W));
        camX += (camTarget - camX) * Math.min(1, Constants.CAM_SMOOTH * dt);

        float pct = MathUtils.clamp((player.x / levelDef.width) * 100f, 0, 100);
        progressFill.setWidth(Constants.W * pct / 100f);
    }

    private void updatePlayer(float dt) {
        boolean left = Gdx.input.isKeyPressed(Input.Keys.LEFT) || Gdx.input.isKeyPressed(Input.Keys.A) || touchLeftDown;
        boolean right = Gdx.input.isKeyPressed(Input.Keys.RIGHT) || Gdx.input.isKeyPressed(Input.Keys.D) || touchRightDown;
        boolean jumpHeld = Gdx.input.isKeyPressed(Input.Keys.SPACE) || Gdx.input.isKeyPressed(Input.Keys.UP) || Gdx.input.isKeyPressed(Input.Keys.W) || touchJumpHeld;
        boolean jumpPressed = Gdx.input.isKeyJustPressed(Input.Keys.SPACE) || Gdx.input.isKeyJustPressed(Input.Keys.UP) || Gdx.input.isKeyJustPressed(Input.Keys.W) || touchJumpJustPressed;
        touchJumpJustPressed = false;
        if (jumpPressed) player.jumpBuffer = Constants.JUMP_BUFFER_TIME;

        boolean wasOnGround = player.onGround;
        boolean onIce = player.onGround && "ice".equals(player.groundType);
        float accel = Constants.MOVE_ACCEL * (player.onGround ? (onIce ? 0.35f : 1f) : Constants.AIR_ACCEL_MULT);

        if (left && !right) {
            player.vx -= accel * dt;
            player.facing = -1;
        } else if (right && !left) {
            player.vx += accel * dt;
            player.facing = 1;
        } else if (player.onGround) {
            float f = (onIce ? Constants.FRICTION * 0.08f : Constants.FRICTION) * dt;
            if (player.vx > 0) player.vx = Math.max(0, player.vx - f);
            else if (player.vx < 0) player.vx = Math.min(0, player.vx + f);
        }
        player.vx = MathUtils.clamp(player.vx, -Constants.MAX_SPEED, Constants.MAX_SPEED);

        if (player.onGround) player.coyote = Constants.COYOTE_TIME;
        else player.coyote -= dt;
        player.jumpBuffer -= dt;

        if (player.jumpBuffer > 0 && player.coyote > 0) {
            player.vy = -Constants.JUMP_VELOCITY;
            player.onGround = false;
            player.coyote = 0;
            player.jumpBuffer = 0;
            player.squashX = 0.7f; player.squashY = 1.35f;
            spawnDust(player.x + player.w / 2f, player.y + player.h, 5);
            game.sfx.jump();
        }

        float g = Constants.GRAVITY;
        if (player.vy < 0 && !jumpHeld && !player.bounced) g *= Constants.CUT_GRAVITY_MULT;
        else if (player.vy > 0) g *= Constants.FALL_GRAVITY_MULT;
        player.vy += g * dt;
        if (player.vy > Constants.MAX_FALL) player.vy = Constants.MAX_FALL;
        if (player.bounced && player.vy >= 0) player.bounced = false;

        player.x += player.vx * dt;
        resolveCollisions(true);

        float impactVy = player.vy;
        player.y += player.vy * dt;
        player.onGround = false;
        player.groundType = null;
        player.groundPlatform = null;
        resolveCollisions(false);

        if (!wasOnGround && player.onGround) {
            boolean hard = impactVy > 480;
            player.squashX = hard ? 1.45f : 1.25f;
            player.squashY = hard ? 0.55f : 0.75f;
            spawnDust(player.x + player.w / 2f, player.y + player.h, hard ? 9 : 5);
            if (hard) addShake(2.5f, 0.12f);
            game.sfx.land();
        }

        player.x = MathUtils.clamp(player.x, 0, levelDef.width - player.w);

        float relax = 1 - (float) Math.exp(-14 * dt);
        player.squashX += (1 - player.squashX) * relax;
        player.squashY += (1 - player.squashY) * relax;

        if (player.onGround && Math.abs(player.vx) > 40) {
            player.animTime += dt * (Math.abs(player.vx) / 60f);
            if (MathUtils.random() < 0.35f) spawnDust(player.x + player.w / 2f, player.y + player.h, 1);
        }

        player.falling = !player.onGround && player.y > Constants.H - 40 - Constants.GROUND_LIFT;
        if (player.falling) player.rotation += dt * 9f * (player.facing != 0 ? player.facing : 1);
        else player.rotation *= Math.max(0, 1 - dt * 10);
    }

    private boolean overlap(float ax, float ay, float aw, float ah, float bx, float by, float bw, float bh) {
        return ax < bx + bw && ax + aw > bx && ay < by + bh && ay + ah > by;
    }

    private boolean overlapPlayer(float bx, float by, float bw, float bh) {
        return overlap(player.x, player.y, player.w, player.h, bx, by, bw, bh);
    }

    private void resolveCollisions(boolean axisX) {
        for (PlatformInst p : platforms) {
            if (!p.isSolid()) continue;
            if (!overlapPlayer(p.x, p.y, p.w, p.h)) continue;
            if (axisX) {
                if (player.vx > 0) player.x = p.x - player.w;
                else if (player.vx < 0) player.x = p.x + p.w;
                player.vx = 0;
            } else {
                if (player.vy > 0) {
                    player.y = p.y - player.h;
                    if ("bounce".equals(p.type)) {
                        player.vy = -p.power;
                        player.bounced = true;
                        player.squashX = 0.6f; player.squashY = 1.5f;
                        spawnDust(player.x + player.w / 2f, player.y + player.h, 8);
                        addShake(2, 0.1f);
                        game.sfx.jump();
                    } else {
                        player.vy = 0;
                        player.onGround = true;
                        player.groundType = p.type;
                        player.groundPlatform = p;
                    }
                    if (("hidden_spike".equals(p.type) || "crumble".equals(p.type) || "hidden_bomb".equals(p.type)) && !p.triggered) {
                        p.triggered = true;
                        p.t = 0;
                    }
                } else if (player.vy < 0) {
                    player.y = p.y + p.h;
                    player.vy = 0;
                }
            }
        }
    }

    private void updateTraps(float dt) {
        for (PlatformInst p : platforms) {
            if ("hidden_spike".equals(p.type)) {
                if (!p.triggered && !Float.isNaN(p.triggerX) && player.x + player.w > p.triggerX) {
                    p.triggered = true; p.t = 0;
                }
                if (p.triggered && !p.poppedUp) {
                    p.t += dt;
                    if (p.t >= p.delay) {
                        p.poppedUp = true;
                        game.sfx.pop();
                        addShake(1.5f, 0.08f);
                    }
                }
            }
            if ("crumble".equals(p.type) && p.triggered && !p.gone) {
                p.t += dt;
                if (p.t >= p.delay) {
                    p.gone = true;
                    game.sfx.crumble();
                    spawnBurst(p.x + p.w / 2f, p.y + p.h / 2f, 10, COL_CRUMBLE, 6, 0.6f, 140, 1400, 0, "debris");
                }
            }
            if ("hidden_bomb".equals(p.type)) {
                if (!p.triggered && !Float.isNaN(p.triggerX) && player.x + player.w > p.triggerX) {
                    p.triggered = true; p.t = 0;
                }
                if (p.triggered && !p.gone) {
                    p.t += dt;
                    if (p.t >= p.delay) {
                        p.gone = true;
                        float cx = p.x + p.w / 2f, cy = p.y;
                        float dist = (float) Math.hypot((player.x + player.w / 2f) - cx, (player.y + player.h / 2f) - cy);
                        if (!player.dead && dist < p.blastRadius) killPlayer();
                        addShake(7, 0.3f);
                        flash = Math.max(flash, 0.35f);
                        game.sfx.boom();
                        spawnBurst(cx, cy, 18, new Color(1f, 0.7f, 0.28f, 1f), 6, 0.5f, 320, 700, 0, "spark");
                    }
                }
            }
            if ("fake_floor".equals(p.type) && !p.falling && overlapPlayer(p.x, p.y, p.w, p.h)) {
                p.falling = true;
                p.fallVy = 40;
                game.sfx.crumble();
                spawnBurst(p.x + p.w / 2f, p.y + p.h / 2f, 12, new Color(0.24f, 0.42f, 0.19f, 1f), 6, 0.6f, 160, 1200, 0, "debris");
            }
            if (p.falling && !p.gone) {
                p.fallVy += 2000 * dt;
                p.y += p.fallVy * dt;
                if (p.y > Constants.H + 200) p.gone = true;
            }
        }
    }

    private void updateMovingPlatforms(float dt) {
        for (PlatformInst p : platforms) {
            if (!"moving".equals(p.type) || p.gone) continue;
            float prevX = p.x, prevY = p.y;
            if ("y".equals(p.axis)) {
                p.y += p.speed * p.dir * dt;
                if (p.y >= p.maxY) { p.y = p.maxY; p.dir = -1; }
                if (p.y <= p.minY) { p.y = p.minY; p.dir = 1; }
            } else {
                p.x += p.speed * p.dir * dt;
                if (p.x >= p.maxX) { p.x = p.maxX; p.dir = -1; }
                if (p.x <= p.minX) { p.x = p.minX; p.dir = 1; }
            }
            if (player.onGround && player.groundPlatform == p) {
                player.x += p.x - prevX;
                player.y += p.y - prevY;
            }
        }
    }

    private void updateSaws(float dt) {
        for (SawInst s : saws) {
            s.x += s.speed * s.dir * dt;
            if (s.x >= s.maxX) { s.x = s.maxX; s.dir = -1; }
            if (s.x <= s.minX) { s.x = s.minX; s.dir = 1; }
        }
    }

    private void updateWallSpikes(float dt) {
        for (WallSpikeInst w : wallSpikes) {
            if (!w.triggered && player.x + player.w > w.triggerX) {
                w.triggered = true; w.t = 0;
            }
            if (w.triggered) {
                w.t += dt;
                float progress = MathUtils.clamp((w.t - w.delay) / 0.15f, 0, 1);
                if (progress > 0 && w.extend == 0) game.sfx.pop();
                w.extend = progress * w.reach;
            }
        }
    }

    private void updateFallingBlocks(float dt) {
        for (FallingBlockInst b : fallingBlocks) {
            if (b.gone) continue;
            if ("idle".equals(b.state)) {
                if (player.x + player.w > b.triggerX) { b.state = "warn"; b.t = 0; }
            } else if ("warn".equals(b.state)) {
                b.t += dt;
                if (b.t >= b.delay) { b.state = "falling"; b.vy = 60; }
            } else if ("falling".equals(b.state)) {
                b.vy += 2200 * dt;
                b.curY += b.vy * dt;
                if (!player.dead && overlapPlayer(b.x, b.curY, b.w, b.h)) killPlayer();
                if (b.curY + b.h >= b.groundY) {
                    b.curY = b.groundY - b.h;
                    b.state = "landed";
                    b.t = 0;
                    addShake(6, 0.25f);
                    game.sfx.boom();
                    spawnBurst(b.x + b.w / 2f, b.groundY, 14, COL_CRUMBLE, 6, 0.5f, 220, 900, 0, "debris");
                }
            } else if ("landed".equals(b.state)) {
                b.t += dt;
                if (b.t > 0.6f) b.gone = true;
            }
        }
    }

    private void updateBombs(float dt) {
        for (BombInst b : bombs) {
            if (b.gone) continue;
            if ("idle".equals(b.state)) {
                if (player.x + player.w > b.triggerX) { b.state = "warn"; b.t = 0; }
            } else if ("warn".equals(b.state)) {
                b.t += dt;
                if (b.t >= b.delay) {
                    b.state = "active";
                    if ("sky".equals(b.kind)) { b.curY = b.y; b.vy = 40; }
                }
            } else if ("active".equals(b.state)) {
                if ("sky".equals(b.kind)) {
                    b.vy += 2000 * dt;
                    b.curY += b.vy * dt;
                    float dx = (player.x + player.w / 2f) - b.x;
                    float dy = (player.y + player.h / 2f) - b.curY;
                    if (!player.dead && Math.hypot(dx, dy) < b.radius) killPlayer();
                    if (b.curY >= b.groundY) {
                        float bdx = (player.x + player.w / 2f) - b.x;
                        float bdy = (player.y + player.h / 2f) - b.groundY;
                        if (!player.dead && Math.hypot(bdx, bdy) < b.blastRadius) killPlayer();
                        addShake(7, 0.3f);
                        flash = Math.max(flash, 0.35f);
                        game.sfx.boom();
                        spawnBurst(b.x, b.groundY, 20, new Color(1f, 0.7f, 0.28f, 1f), 6, 0.5f, 340, 600, 0, "spark");
                        b.gone = true;
                    }
                } else {
                    b.curX += b.speed * b.dir * dt;
                    float dx = (player.x + player.w / 2f) - b.curX;
                    float dy = (player.y + player.h / 2f) - b.y;
                    if (!player.dead && Math.hypot(dx, dy) < b.radius) {
                        killPlayer();
                        addShake(7, 0.3f);
                        flash = Math.max(flash, 0.35f);
                        game.sfx.boom();
                        spawnBurst(b.curX, b.y, 20, new Color(1f, 0.7f, 0.28f, 1f), 6, 0.5f, 340, 300, 0, "spark");
                        b.gone = true;
                    }
                    boolean outOfBounds = b.dir == 1 ? b.curX > b.toX : b.curX < b.toX;
                    if (outOfBounds) b.gone = true;
                }
            }
        }
    }

    private void updateTeleporters(float dt) {
        if (player.teleportCooldown > 0) { player.teleportCooldown -= dt; return; }
        for (TeleporterInst tp : teleporters) {
            if (overlapPlayer(tp.x, tp.y, tp.w, tp.h)) {
                spawnBurst(player.x + player.w / 2f, player.y + player.h / 2f, 14, new Color(0.56f, 0.91f, 1f, 1f), 5, 0.4f, 260, 0, 0, "spark");
                player.x = tp.toX;
                player.y = tp.toY;
                player.vx = 0; player.vy = 0;
                spawnBurst(player.x + player.w / 2f, player.y + player.h / 2f, 14, new Color(0.79f, 0.64f, 1f, 1f), 5, 0.4f, 260, 0, 0, "spark");
                player.teleportCooldown = 0.35f;
                addShake(2, 0.15f);
                game.sfx.pop();
                break;
            }
        }
    }

    private void updateRunWall(float dt) {
        if (runWall == null) return;
        runWall.x += runWall.speed * dt;
        if (!player.dead && player.x < runWall.x) killPlayer();
    }

    private void updateParticles(float dt) {
        Iterator<Particle> it = particles.iterator();
        while (it.hasNext()) {
            Particle p = it.next();
            p.x += p.vx * dt;
            p.y += p.vy * dt;
            p.vy += p.gravity * dt;
            p.life -= dt;
            p.rot += p.rotSpeed * dt;
            if (p.life <= 0) it.remove();
        }
    }

    private void checkHazards() {
        if (player.dead) return;
        for (HazardInst h : levelDef.hazards) {
            if ("void".equals(h.type) && overlapPlayer(h.x, h.y, h.w, h.h)) { killPlayer(); return; }
            if ("spike".equals(h.type) && overlapPlayer(h.x, h.y, h.w, h.h)) { killPlayer(); return; }
        }
        for (PlatformInst p : platforms) {
            if ("hidden_spike".equals(p.type) && p.poppedUp && overlapPlayer(p.spikeX, p.y - 8, p.spikeW, 16)) { killPlayer(); return; }
        }
        for (SawInst s : saws) {
            float dx = (player.x + player.w / 2f) - s.x;
            float dy = (player.y + player.h / 2f) - s.y;
            if (Math.hypot(dx, dy) < s.r + 10) { killPlayer(); return; }
        }
        for (WallSpikeInst w : wallSpikes) {
            float rx = w.dir == 1 ? w.x : w.x - w.extend;
            if (w.extend > 10 && overlapPlayer(rx, w.y, w.extend, w.h)) { killPlayer(); return; }
        }
        if (player.y > Constants.H + 200) killPlayer();
    }

    private void checkGoal() {
        if (!"playing".equals(state)) return;
        if (overlapPlayer(levelDef.goalX, levelDef.goalY, levelDef.goalW, levelDef.goalH)) completeLevel();
    }

    private void addShake(float mag, float dur) {
        if (mag > shakeMag) shakeMag = mag;
        shakeT = Math.max(shakeT, dur);
    }

    private void spawnBurst(float x, float y, int count, Color color, float size, float life, float speedRange, float gravity, float upBias, String type) {
        for (int i = 0; i < count; i++) {
            float ang = MathUtils.random() * MathUtils.PI2;
            float spd = 60 + MathUtils.random() * speedRange;
            Particle p = new Particle();
            p.x = x; p.y = y;
            p.vx = MathUtils.cos(ang) * spd;
            p.vy = MathUtils.sin(ang) * spd - upBias;
            p.life = life; p.maxLife = life;
            p.color = color; p.size = size; p.type = type;
            p.rot = MathUtils.random() * MathUtils.PI2;
            p.rotSpeed = (MathUtils.random() - 0.5f) * 10f;
            p.gravity = gravity;
            particles.add(p);
        }
    }

    private void spawnDust(float x, float y, int count) {
        spawnBurst(x, y, count, new Color(0.9f, 0.9f, 0.9f, 0.85f), 4, 0.35f, 90, 250, 60, "dust");
    }

    private void spawnPortalPull(float cx, float cy) {
        float ang = MathUtils.random() * MathUtils.PI2;
        float dist = 70 + MathUtils.random() * 30;
        float sx = cx + MathUtils.cos(ang) * dist;
        float sy = cy + MathUtils.sin(ang) * dist * 0.6f;
        Particle p = new Particle();
        p.x = sx; p.y = sy;
        p.vx = (cx - sx) * 3.5f; p.vy = (cy - sy) * 3.5f;
        p.life = 0.4f; p.maxLife = 0.4f;
        p.color = MathUtils.randomBoolean() ? new Color(0.7f, 0.4f, 1f, 1f) : new Color(0.4f, 0.86f, 1f, 1f);
        p.size = 4; p.type = "dust"; p.gravity = 0;
        particles.add(p);
    }

    private void killPlayer() {
        if (player.dead) return;
        player.dead = true;
        state = "dead";
        stateTimer = 0.55f;
        player.squashX = 1.4f; player.squashY = 0.5f;
        spawnBurst(player.x + player.w / 2f, player.y + player.h / 2f, 20, new Color(1f, 0.34f, 0.34f, 1f), 5, 0.55f, 420, 1000, 0, "spark");
        addShake(9, 0.3f);
        flash = 0.5f;
        game.sfx.death();
    }

    private void completeLevel() {
        state = "complete";
        stateTimer = 1.1f;
        completeDuration = 1.1f;
        portalCx = levelDef.goalX + levelDef.goalW / 2f;
        portalCy = levelDef.goalY + levelDef.goalH / 2f;
        pullStartX = player.x; pullStartY = player.y;
        spawnBurst(portalCx, portalCy, 20, new Color(0.7f, 0.4f, 1f, 1f), 5, 0.9f, 340, 300, 150, "spark");
        addShake(3, 0.2f);
        game.sfx.goal();
    }

    private void advanceAfterComplete() {
        if (advancingLevel) return;
        advancingLevel = true;
        int next = levelIndex + 1;
        boolean reachedEnd = next >= game.assets.levels.size || game.assets.levels.get(next).locked;
        if (reachedEnd) {
            game.progress.setUnlockedLevels(game.assets.levels.size);
            loadLevel(0);
            return;
        }
        game.progress.setUnlockedLevels(next + 1);
        loadLevel(next);
    }

    // --------------------------------------------------------------- render

    private void renderWorld() {
        Gdx.gl.glClearColor(0, 0, 0, 1);
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT);

        float shakeX = 0, shakeY = 0;
        if (shakeT > 0) {
            shakeX = (MathUtils.random() - 0.5f) * shakeMag;
            shakeY = (MathUtils.random() - 0.5f) * shakeMag;
        }

        worldCamera.position.set(camX + Constants.W / 2f + shakeX, Constants.H / 2f + shakeY, 0);
        worldCamera.update();

        game.batch.setProjectionMatrix(worldCamera.combined);
        game.batch.begin();
        game.batch.draw(game.assets.backgroundGame, camX, Constants.H, Constants.W, -Constants.H);
        drawStars();
        game.batch.end();

        Gdx.gl.glEnable(GL20.GL_BLEND);
        shapes.setProjectionMatrix(worldCamera.combined);

        shapes.begin(ShapeRenderer.ShapeType.Filled);
        drawPlatforms();
        drawStaticHazards();
        drawRunWall();
        drawTeleporters();
        drawFallingBlocks();
        drawBombs();
        drawSaws();
        drawWallSpikes();
        drawGoal();
        if (!player.dead || "dead".equals(state)) drawPlayer();
        drawParticles();
        shapes.end();

        if (flash > 0) {
            shapes.begin(ShapeRenderer.ShapeType.Filled);
            shapes.setColor(1f, 0.24f, 0.24f, flash);
            shapes.rect(camX, 0, Constants.W, Constants.H);
            shapes.end();
        }
        Gdx.gl.glDisable(GL20.GL_BLEND);
    }

    private void drawStars() {
        game.batch.setColor(1, 1, 1, 1);
        // stars use additive-ish twinkle via alpha; drawn as tiny quads using the pixel texture
        for (float[] s : stars) {
            float sx = s[0];
            float alpha = 0.4f + MathUtils.sin(bgAnimT * 2f + s[3]) * 0.3f;
            game.batch.setColor(1, 1, 1, Math.max(0, alpha));
            float r = s[2];
            game.batch.draw(game.assets.pixel, sx - r, s[1] - r, r * 2, r * 2);
        }
        game.batch.setColor(1, 1, 1, 1);
    }

    private void rect(float x, float y, float w, float h, Color c) {
        shapes.setColor(c);
        shapes.rect(x, y, w, h);
    }

    private void drawPlatforms() {
        for (PlatformInst p : platforms) {
            if (p.gone) continue;
            switch (p.type) {
                case "crumble": {
                    float shakeAmt = p.triggered && !p.gone ? (MathUtils.random() - 0.5f) * 4 : 0;
                    rect(p.x + shakeAmt, p.y, p.w, p.h, p.triggered ? COL_CRUMBLE_TRIG : COL_CRUMBLE);
                    rect(p.x + shakeAmt, p.y, p.w, 6, new Color(0.42f, 0.27f, 0.14f, 1f));
                    break;
                }
                case "fake_floor":
                case "solid": {
                    rect(p.x, p.y, p.w, p.h, COL_SOLID);
                    rect(p.x, p.y, p.w, 6, COL_SOLID_TOP);
                    shapes.setColor(0, 0, 0, 0.12f);
                    for (float bx = p.x; bx < p.x + p.w; bx += 34) shapes.rect(bx, p.y + 10, 1, p.h - 10);
                    break;
                }
                case "hidden_spike": {
                    rect(p.x, p.y, p.w, p.h, COL_SOLID);
                    rect(p.x, p.y, p.w, 6, COL_SOLID_TOP);
                    if (p.poppedUp) {
                        float wobble = Math.min(1, p.t - p.delay) * 3;
                        shapes.setColor(COL_SPIKE);
                        int n = Math.max(1, (int) (p.spikeW / 18));
                        for (int i = 0; i < n; i++) {
                            float sx = p.spikeX + (i + 0.5f) * (p.spikeW / n);
                            shapes.triangle(sx - 9, p.y, sx, p.y - 22 - wobble, sx + 9, p.y);
                        }
                    }
                    break;
                }
                case "hidden_bomb": {
                    rect(p.x, p.y, p.w, p.h, COL_SOLID);
                    rect(p.x, p.y, p.w, 6, COL_SOLID_TOP);
                    if (p.triggered && !p.gone) {
                        float pulse = 0.4f + MathUtils.sin(bgAnimT * 11f) * 0.3f;
                        shapes.setColor(1f, 0.55f, 0.2f, 0.5f + pulse * 0.4f);
                        shapes.circle(p.x + p.w / 2f, p.y - 6, 10);
                    }
                    break;
                }
                case "ice": {
                    rect(p.x, p.y, p.w, p.h, COL_ICE);
                    rect(p.x, p.y, p.w, 6, COL_ICE_TOP);
                    break;
                }
                case "bounce": {
                    rect(p.x, p.y, p.w, p.h, COL_BOUNCE);
                    rect(p.x, p.y, p.w, 6, COL_BOUNCE_TOP);
                    break;
                }
                case "moving": {
                    rect(p.x, p.y, p.w, p.h, COL_MOVING);
                    rect(p.x, p.y, p.w, 6, COL_MOVING_TOP);
                    break;
                }
                case "stone": {
                    rect(p.x, p.y, p.w, p.h, COL_STONE);
                    rect(p.x, p.y, p.w, 6, COL_STONE_TOP);
                    break;
                }
                default: {
                    rect(p.x, p.y, p.w, p.h, COL_SOLID);
                    rect(p.x, p.y, p.w, 6, COL_SOLID_TOP);
                }
            }
        }
    }

    private void drawStaticHazards() {
        for (HazardInst h : levelDef.hazards) {
            if (!"spike".equals(h.type)) continue;
            shapes.setColor(COL_SPIKE);
            int n = Math.max(1, (int) (h.w / 20));
            for (int i = 0; i < n; i++) {
                float sx = h.x + (i + 0.5f) * (h.w / n);
                shapes.triangle(sx - 10, h.y + h.h, sx, h.y, sx + 10, h.y + h.h);
            }
        }
    }

    private void drawSaws() {
        for (SawInst s : saws) {
            shapes.setColor(0, 0, 0, 0.25f);
            shapes.circle(s.x, s.y + 4, s.r * 0.9f, 20);
            shapes.setColor(0.79f, 0.79f, 0.79f, 1f);
            int spikes = 10;
            float angle = sawSpin * 10f;
            float[] vx = new float[spikes * 2];
            float[] vy = new float[spikes * 2];
            for (int i = 0; i < spikes * 2; i++) {
                float rad = i % 2 == 0 ? s.r : s.r * 0.7f;
                float a = angle + (i / (float) (spikes * 2)) * MathUtils.PI2;
                vx[i] = s.x + MathUtils.cos(a) * rad;
                vy[i] = s.y + MathUtils.sin(a) * rad;
            }
            for (int i = 1; i < spikes * 2 - 1; i++) {
                shapes.triangle(vx[0], vy[0], vx[i], vy[i], vx[i + 1], vy[i + 1]);
            }
            shapes.setColor(0.47f, 0.47f, 0.47f, 1f);
            shapes.circle(s.x, s.y, s.r * 0.28f, 12);
        }
    }

    private void drawWallSpikes() {
        for (WallSpikeInst w : wallSpikes) {
            shapes.setColor(0.6f, 0.6f, 0.6f, 1f);
            shapes.rect(w.x - (w.dir == 1 ? 6 : 0), w.y, 6, w.h);
        }
        for (WallSpikeInst w : wallSpikes) {
            if (w.extend <= 0) continue;
            shapes.setColor(COL_SPIKE);
            float bx = w.dir == 1 ? w.x : w.x - w.extend;
            shapes.rect(bx, w.y, w.extend, w.h);
        }
    }

    private void drawFallingBlocks() {
        for (FallingBlockInst b : fallingBlocks) {
            if (b.gone) continue;
            if ("warn".equals(b.state)) {
                float pulse = 0.4f + MathUtils.sin(bgAnimT * 11f) * 0.3f;
                shapes.setColor(1f, 0.3f, 0.3f, 0.25f + pulse * 0.25f);
                shapes.ellipse(b.x, b.groundY - 12, b.w, 20);
                continue;
            }
            if ("falling".equals(b.state) || "landed".equals(b.state)) {
                rect(b.x, b.curY, b.w, b.h, new Color(0.42f, 0.29f, 0.17f, 1f));
                rect(b.x + 4, b.curY + 4, b.w - 8, b.h - 8, COL_CRUMBLE);
            }
        }
    }

    private void drawBombIcon(float x, float y, float r) {
        shapes.setColor(0.1f, 0.1f, 0.1f, 1f);
        shapes.circle(x, y, r, 16);
        shapes.setColor(1f, 0.7f, 0.28f, 1f);
        shapes.circle(x + r * 0.7f, y - r * 1.4f, 3, 8);
    }

    private void drawBombs() {
        for (BombInst b : bombs) {
            if (b.gone) continue;
            if ("warn".equals(b.state)) {
                float pulse = 0.4f + MathUtils.sin(bgAnimT * 11f) * 0.3f;
                if ("sky".equals(b.kind)) {
                    shapes.setColor(1f, 0.55f, 0.2f, 0.25f + pulse * 0.25f);
                    shapes.ellipse(b.x - 34, b.groundY - 13, 68, 18);
                } else {
                    shapes.setColor(1f, 0.55f, 0.2f, 0.5f + pulse * 0.5f);
                    float wx = b.dir == 1 ? camX + 26 : camX + Constants.W - 26;
                    shapes.triangle(wx, b.y - 14, wx + (b.dir == 1 ? 16 : -16), b.y, wx, b.y + 14);
                }
                continue;
            }
            if ("active".equals(b.state)) {
                if ("sky".equals(b.kind)) drawBombIcon(b.x, b.curY, 14);
                else drawBombIcon(b.curX, b.y, 14);
            }
        }
    }

    private void drawTeleporters() {
        for (TeleporterInst tp : teleporters) {
            float cx = tp.x + tp.w / 2f, cy = tp.y + tp.h / 2f;
            shapes.setColor(0.56f, 0.91f, 1f, 0.35f);
            shapes.ellipse(tp.x, tp.y, tp.w, tp.h);
        }
    }

    private void drawRunWall() {
        if (runWall == null) return;
        shapes.setColor(0.04f, 0.02f, 0.08f, 0.95f);
        shapes.rect(camX, runWall.y, runWall.x - camX, runWall.h);
        shapes.setColor(0.7f, 0.4f, 1f, 0.5f);
        shapes.rectLine(runWall.x, runWall.y, runWall.x, runWall.y + runWall.h, 3);
    }

    private void drawGoal() {
        float baseCx = levelDef.goalX + levelDef.goalW / 2f, baseCy = levelDef.goalY + levelDef.goalH / 2f;
        float bob = MathUtils.sin(bgAnimT * 1.1f) * 3;
        float cx = baseCx, cy = baseCy + bob;
        float rx = levelDef.goalW / 2f + 2, ry = levelDef.goalH / 2f + 3;
        float pulse = 0.5f + MathUtils.sin(bgAnimT * 4.5f) * 0.5f;

        // ground light pool
        shapes.setColor(0.7f, 0.4f, 1f, 0.18f + pulse * 0.1f);
        shapes.ellipse(cx - rx * 1.6f, levelDef.goalY + levelDef.goalH, rx * 3.2f, 14);

        drawPortalArch(baseCx, baseCy, rx, ry);

        // back-to-front: soft outer glow -> mid purple ring -> bright core (smallest, on top)
        shapes.setColor(0.7f, 0.4f, 1f, 0.22f + pulse * 0.12f);
        shapes.ellipse(cx - rx * 1.3f, cy - ry * 1.3f, rx * 2.6f, ry * 2.6f);

        shapes.setColor(0.59f, 0.35f, 0.9f, 0.55f + pulse * 0.2f);
        shapes.ellipse(cx - rx * 0.8f, cy - ry * 0.8f, rx * 1.6f, ry * 1.6f);

        shapes.setColor(0.75f, 0.5f, 0.95f, 0.8f + pulse * 0.15f);
        shapes.ellipse(cx - rx * 0.5f, cy - ry * 0.5f, rx, ry);

        shapes.setColor(0.95f, 0.9f, 1f, 0.9f);
        shapes.ellipse(cx - rx * 0.22f, cy - ry * 0.22f, rx * 0.44f, ry * 0.44f);

        for (float[] m : portalMotes) {
            float ang = m[0] + bgAnimT * m[2];
            float px = cx + MathUtils.cos(ang) * m[1];
            float py = cy + MathUtils.sin(ang) * m[1] * 0.5f + MathUtils.sin(bgAnimT * 3.3f + m[3]) * 2;
            float alpha = 0.45f + MathUtils.sin(bgAnimT * 2.8f + m[3]) * 0.35f;
            int ci = (int) m[5];
            Color c = ci == 0 ? new Color(0.79f, 0.64f, 1f, alpha) : ci == 1 ? new Color(0.56f, 0.91f, 1f, alpha) : new Color(1f, 1f, 1f, alpha);
            shapes.setColor(c);
            shapes.circle(px, py, m[4], 8);
        }
    }

    /** Stone arch framing the goal portal, matching the web build's carved pillars + pediment. */
    private void drawPortalArch(float cx, float cy, float rx, float ry) {
        float archW = rx * 2 + 26, archH = ry * 2 + 34;
        float left = cx - archW / 2f, right = cx + archW / 2f;
        float top = cy - archH / 2f + 6, bottom = cy + archH / 2f;
        float pillarW = 12f;

        shapes.setColor(lerpStone(pillarW / (2f * archW)));
        shapes.rect(left, top, pillarW, bottom - top);
        shapes.setColor(lerpStone(1f - pillarW / (2f * archW)));
        shapes.rect(right - pillarW, top, pillarW, bottom - top);

        // pediment peaking above the pillars, closing the arch
        shapes.setColor(lerpStone(0.5f));
        shapes.triangle(left, top + 14, right, top + 14, cx, top - 20);
        shapes.rect(left + pillarW, top + 8, archW - pillarW * 2, 8);

        float t = bgAnimT * 3.85f;
        shapes.setColor(0.7f, 0.4f, 1f, 0.4f + MathUtils.sin(t) * 0.4f);
        shapes.circle(left + pillarW / 2f, top + 26, 3, 10);
        shapes.setColor(0.48f, 0.9f, 1f, 0.4f + MathUtils.sin(t + 1.5f) * 0.4f);
        shapes.circle(right - pillarW / 2f, top + 46, 3, 10);
        shapes.setColor(0.7f, 0.4f, 1f, 0.4f + MathUtils.sin(t + 3f) * 0.4f);
        shapes.circle(left + pillarW / 2f, bottom - 24, 3, 10);
    }

    /** Interpolates the web build's 3-stop stone gradient (#2e2540 -> #3c3055 -> #241d34) at t in [0,1]. */
    private Color lerpStone(float t) {
        if (t <= 0.5f) {
            float f = t / 0.5f;
            return new Color(MathUtils.lerp(0.180f, 0.235f, f), MathUtils.lerp(0.145f, 0.188f, f), MathUtils.lerp(0.251f, 0.333f, f), 1f);
        }
        float f = (t - 0.5f) / 0.5f;
        return new Color(MathUtils.lerp(0.235f, 0.141f, f), MathUtils.lerp(0.188f, 0.114f, f), MathUtils.lerp(0.333f, 0.204f, f), 1f);
    }

    private void drawPlayer() {
        float cx = player.x + player.w / 2f;
        float cy = player.y + player.h / 2f;
        float hw = (player.w / 2f) * player.squashX;
        float hh = (player.h / 2f) * player.squashY;

        Color bodyColor = player.dead ? new Color(0.12f, 0.12f, 0.12f, 0.6f) : new Color(0.08f, 0.08f, 0.08f, 1f);
        shapes.setColor(bodyColor);
        shapes.rect(cx - hw, cy - hh, hw * 2, hh * 2);

        if (!player.dead) {
            shapes.setColor(bodyColor);
            boolean running = player.onGround && Math.abs(player.vx) > 30;
            float phase = running ? MathUtils.sin(player.animTime * 6f) * 5f : 0f;
            shapes.rect(cx - hw + 4 + phase * 0.4f, cy + hh - 2, 7, 6);
            shapes.rect(cx + hw - 11 - phase * 0.4f, cy + hh - 2, 7, 6);

            shapes.setColor(Color.WHITE);
            float ex = player.facing == 1 ? cx + hw - 9 : cx - hw + 5;
            shapes.rect(ex, cy - hh + 9, 4, 4);
        }
    }

    private void drawParticles() {
        for (Particle p : particles) {
            float alpha = Math.max(0, p.life / p.maxLife);
            Color c = new Color(p.color.r, p.color.g, p.color.b, alpha * p.color.a);
            shapes.setColor(c);
            if ("dust".equals(p.type)) {
                shapes.circle(p.x, p.y, p.size * alpha, 8);
            } else if ("debris".equals(p.type)) {
                shapes.rect(p.x - p.size / 2f, p.y - p.size / 2f, p.size, p.size);
            } else {
                shapes.rect(p.x - p.size / 2f, p.y - p.size / 2f, p.size, p.size);
            }
        }
    }

    @Override
    public void dispose() {
        hud.dispose();
        shapes.dispose();
    }
}
