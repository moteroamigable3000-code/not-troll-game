package com.bfjstudios.nottroll.screens;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.g2d.Batch;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import com.badlogic.gdx.math.MathUtils;
import com.badlogic.gdx.math.Vector2;
import com.badlogic.gdx.scenes.scene2d.Actor;
import com.badlogic.gdx.utils.Array;

/** Fixed (non-scrolling) starfield + mountain silhouette behind the level trail. */
public class MapBackdropActor extends Actor {
    private final ShapeRenderer shapes;
    private final Array<float[]> stars = new Array<>();
    private final Vector2 stageOrigin = new Vector2();
    private float time;

    public MapBackdropActor(ShapeRenderer shapes) {
        this.shapes = shapes;
        for (int i = 0; i < 26; i++) {
            stars.add(new float[]{MathUtils.random(), MathUtils.random(0.15f, 0.55f), MathUtils.random(0.6f, 1.6f), MathUtils.random(MathUtils.PI2)});
        }
    }

    @Override
    public void act(float delta) {
        super.act(delta);
        time += delta;
    }

    @Override
    public void draw(Batch batch, float parentAlpha) {
        float w = getWidth(), h = getHeight();
        localToStageCoordinates(stageOrigin.set(0f, 0f));
        float x = stageOrigin.x, y = stageOrigin.y;
        batch.end();
        // batch.end() always disables GL_BLEND as part of its own cleanup, so it must be
        // re-enabled here or the twinkling stars' alpha renders fully opaque instead of fading.
        Gdx.gl.glEnable(GL20.GL_BLEND);
        Gdx.gl.glBlendFunc(GL20.GL_SRC_ALPHA, GL20.GL_ONE_MINUS_SRC_ALPHA);
        shapes.setTransformMatrix(batch.getTransformMatrix());
        shapes.setProjectionMatrix(batch.getProjectionMatrix());

        shapes.begin(ShapeRenderer.ShapeType.Filled);
        int bands = 10;
        for (int i = 0; i < bands; i++) {
            float t0 = i / (float) bands, t1 = (i + 1) / (float) bands;
            shapes.setColor(
                0.067f + (0.20f - 0.067f) * t0,
                0.078f + (0.157f - 0.078f) * t0,
                0.176f + (0.306f - 0.176f) * t0,
                1f);
            shapes.rect(x, y + h * t0, w, h * (t1 - t0));
        }

        for (float[] s : stars) {
            float alpha = 0.4f + MathUtils.sin(time * 1.6f + s[3]) * 0.35f;
            shapes.setColor(1f, 1f, 1f, Math.max(0, alpha));
            shapes.circle(x + s[0] * w, y + h * 0.55f + s[1] * h, s[2], 10);
        }

        shapes.setColor(Color.valueOf("251d43"));
        drawMountainRow(x, y, w, h, 0.42f, 7);
        shapes.setColor(Color.valueOf("3a2b62"));
        drawMountainRow(x, y, w, h, 0.26f, 5);
        shapes.end();
        Gdx.gl.glDisable(GL20.GL_BLEND);

        batch.begin();
    }

    private void drawMountainRow(float ox, float oy, float w, float h, float heightPct, int peaks) {
        float rowH = h * heightPct;
        float step = w / peaks;
        float prevX = ox, prevPeakY = oy + rowH * 0.5f;
        for (int i = 0; i <= peaks; i++) {
            float x = ox + i * step;
            float peakY = oy + rowH * (0.45f + 0.5f * ((i * 37) % 7) / 7f);
            if (i > 0) {
                shapes.triangle(prevX, oy, x, oy, prevX, prevPeakY);
                shapes.triangle(x, oy, prevX, prevPeakY, x, peakY);
            }
            prevX = x;
            prevPeakY = peakY;
        }
    }
}
