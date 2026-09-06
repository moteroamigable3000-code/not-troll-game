package com.bfjstudios.nottroll.screens;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.InputAdapter;
import com.badlogic.gdx.ScreenAdapter;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.graphics.glutils.ShaderProgram;
import com.badlogic.gdx.math.Interpolation;
import com.badlogic.gdx.math.MathUtils;
import com.badlogic.gdx.utils.viewport.FitViewport;
import com.badlogic.gdx.utils.viewport.Viewport;
import com.bfjstudios.nottroll.Constants;
import com.bfjstudios.nottroll.NotTrollGame;

/** Studio splash: scale/fade entrance + looping diagonal shine sweep, matching the web build's CSS animation. */
public class SplashScreen extends ScreenAdapter {
    private final NotTrollGame game;
    private final OrthographicCamera camera = new OrthographicCamera();
    private final Viewport viewport;
    private float timer = 0f;
    private boolean dismissed = false;
    private float dismissedAt = 0f;
    private boolean soundPlayed = false;
    private ShaderProgram shineShader;

    private static final float ENTER_DUR = 0.5f;
    private static final float DURATION = 2.2f;
    private static final float FADE = 0.4f;
    private static final float SWEEP_PERIOD = 3.2f;
    private static final float SWEEP_ACTIVE = 1.28f;
    private static final float SWEEP_DELAY = 0.7f;

    private static final String VERT =
        "attribute vec4 a_position;\n" +
        "attribute vec4 a_color;\n" +
        "attribute vec2 a_texCoord0;\n" +
        "uniform mat4 u_projTrans;\n" +
        "varying vec4 v_color;\n" +
        "varying vec2 v_texCoords;\n" +
        "void main() {\n" +
        "    v_color = a_color;\n" +
        "    v_texCoords = a_texCoord0;\n" +
        "    gl_Position = u_projTrans * a_position;\n" +
        "}\n";

    private static final String FRAG =
        "#ifdef GL_ES\n" +
        "precision mediump float;\n" +
        "#endif\n" +
        "varying vec4 v_color;\n" +
        "varying vec2 v_texCoords;\n" +
        "uniform sampler2D u_texture;\n" +
        "uniform float u_sweep;\n" +
        "void main() {\n" +
        "    vec4 tex = texture2D(u_texture, v_texCoords);\n" +
        "    float diag = v_texCoords.x + (1.0 - v_texCoords.y);\n" +
        "    float band = smoothstep(u_sweep - 0.22, u_sweep, diag) - smoothstep(u_sweep, u_sweep + 0.22, diag);\n" +
        "    gl_FragColor = vec4(1.0, 0.97, 1.0, tex.a * band * 0.85 * v_color.a);\n" +
        "}\n";

    public SplashScreen(NotTrollGame game) {
        this.game = game;
        viewport = new FitViewport(Constants.W, Constants.H, camera);
    }

    @Override
    public void show() {
        Gdx.input.setInputProcessor(new InputAdapter() {
            @Override
            public boolean keyDown(int keycode) { dismiss(); return true; }

            @Override
            public boolean touchDown(int screenX, int screenY, int pointer, int button) { dismiss(); return true; }
        });
        ShaderProgram.pedantic = false;
        shineShader = new ShaderProgram(VERT, FRAG);
        playSound();
    }

    private void playSound() {
        if (soundPlayed || !game.progress.isSoundOn()) return;
        soundPlayed = true;
        game.assets.splashSound.play(0.75f);
    }

    private void dismiss() {
        if (dismissed) return;
        dismissed = true;
        dismissedAt = timer;
    }

    @Override
    public void render(float delta) {
        timer += delta;

        boolean exiting = dismissed || timer >= DURATION - FADE;
        float exitStart = dismissed ? dismissedAt : (DURATION - FADE);
        float exitProgress = exiting ? MathUtils.clamp((timer - exitStart) / FADE, 0f, 1f) : 0f;
        if (exitProgress >= 1f) {
            game.goToMainMenu();
            return;
        }

        Gdx.gl.glClearColor(0.047f, 0.039f, 0.086f, 1f);
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT);

        camera.update();
        SpriteBatch batch = game.batch;
        batch.setProjectionMatrix(camera.combined);

        float enterT = Interpolation.pow2Out.apply(MathUtils.clamp(timer / ENTER_DUR, 0f, 1f));
        float scale = MathUtils.lerp(0.92f, 1f, enterT);
        float alpha = enterT * (1f - exitProgress);

        float logoW = 420 * scale;
        float logoH = logoW * game.assets.splashLogo.getHeight() / game.assets.splashLogo.getWidth();
        float lx = (Constants.W - logoW) / 2f, ly = (Constants.H - logoH) / 2f;

        Gdx.gl.glEnable(GL20.GL_BLEND);
        batch.begin();
        batch.setColor(1, 1, 1, alpha);
        batch.draw(game.assets.splashLogo, lx, ly, logoW, logoH);

        float cyclePos = (timer - SWEEP_DELAY) % SWEEP_PERIOD;
        if (cyclePos >= 0 && cyclePos <= SWEEP_ACTIVE) {
            float sweepT = cyclePos / SWEEP_ACTIVE;
            float sweep = MathUtils.lerp(-0.3f, 1.3f, sweepT);
            batch.setShader(shineShader);
            batch.setColor(1, 1, 1, alpha);
            shineShader.setUniformf("u_sweep", sweep);
            batch.draw(game.assets.splashLogo, lx, ly, logoW, logoH);
            batch.setShader(null);
        }

        batch.setColor(1, 1, 1, 1);
        batch.end();
        Gdx.gl.glDisable(GL20.GL_BLEND);
    }

    @Override
    public void resize(int width, int height) {
        viewport.update(width, height, true);
    }

    @Override
    public void hide() {
        if (shineShader != null) shineShader.dispose();
    }
}
