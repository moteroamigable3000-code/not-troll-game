package com.bfjstudios.nottroll.screens;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.g2d.Batch;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import com.badlogic.gdx.scenes.scene2d.Actor;

/** Pennant/chevron-shaped on-screen control, matching the web build's clip-path touch buttons. */
public class TouchButtonActor extends Actor {
    public enum Kind { LEFT, RIGHT, JUMP }

    private final Kind kind;
    private final ShapeRenderer shapes;
    public boolean pressed;

    public TouchButtonActor(Kind kind, ShapeRenderer shapes) {
        this.kind = kind;
        this.shapes = shapes;
    }

    @Override
    public void draw(Batch batch, float parentAlpha) {
        float w = getWidth(), h = getHeight();
        float x = getX(), y = getY();
        float[] poly = polygonFor(kind, w, h);

        batch.end();
        // batch.end() always disables GL_BLEND as part of its own cleanup, so it must be
        // re-enabled here or these alpha-blended shapes render fully opaque instead of translucent.
        Gdx.gl.glEnable(GL20.GL_BLEND);
        Gdx.gl.glBlendFunc(GL20.GL_SRC_ALPHA, GL20.GL_ONE_MINUS_SRC_ALPHA);
        shapes.setTransformMatrix(batch.getTransformMatrix());
        shapes.setProjectionMatrix(batch.getProjectionMatrix());
        shapes.begin(ShapeRenderer.ShapeType.Filled);
        shapes.setColor(1f, 1f, 1f, pressed ? 0.4f : 0.16f);
        int n = poly.length / 2;
        for (int i = 1; i < n - 1; i++) {
            shapes.triangle(x + poly[0], y + poly[1], x + poly[i * 2], y + poly[i * 2 + 1], x + poly[(i + 1) * 2], y + poly[(i + 1) * 2 + 1]);
        }
        shapes.end();
        Gdx.gl.glDisable(GL20.GL_BLEND);
        batch.begin();
    }

    private static float[] polygonFor(Kind k, float w, float h) {
        switch (k) {
            case LEFT:
                return new float[]{w, h, w, 0, 0.22f * w, 0, 0, 0.5f * h, 0.22f * w, h};
            case RIGHT:
                return new float[]{0, h, 0, 0, 0.78f * w, 0, w, 0.5f * h, 0.78f * w, h};
            case JUMP:
            default:
                return new float[]{0, 0, w, 0, w, 0.6f * h, 0.5f * w, h, 0, 0.6f * h};
        }
    }
}
