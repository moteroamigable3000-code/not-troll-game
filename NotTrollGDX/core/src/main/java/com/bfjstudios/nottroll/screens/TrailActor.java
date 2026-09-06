package com.bfjstudios.nottroll.screens;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.g2d.Batch;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import com.badlogic.gdx.math.MathUtils;
import com.badlogic.gdx.math.Vector2;
import com.badlogic.gdx.scenes.scene2d.Actor;
import com.badlogic.gdx.scenes.scene2d.InputEvent;
import com.badlogic.gdx.scenes.scene2d.InputListener;
import com.badlogic.gdx.utils.Align;
import com.badlogic.gdx.utils.Array;
import com.bfjstudios.nottroll.Assets;

/** Draws the winding level trail (path + circular nodes) in one pass, scrolled inside a ScrollPane. */
public class TrailActor extends Actor {
    public static final float NODE_RADIUS = 28f;
    private static final int CIRCLE_SEGMENTS = 96;
    private static final int SMALL_CIRCLE_SEGMENTS = 48;

    public static class NodeInfo {
        public float x, y;
        public int index;
        public boolean locked;
        public boolean current;
    }

    public interface OnSelect { void select(int index); }

    private final Array<NodeInfo> nodes;
    private final Assets assets;
    private final ShapeRenderer shapes;
    private final BitmapFont numberFont;
    private final Vector2 stageOrigin = new Vector2();
    private float time;

    public TrailActor(Array<NodeInfo> nodes, Assets assets, ShapeRenderer shapes, BitmapFont numberFont, OnSelect onSelect) {
        this.nodes = nodes;
        this.assets = assets;
        this.shapes = shapes;
        this.numberFont = numberFont;

        addListener(new InputListener() {
            @Override
            public boolean touchDown(InputEvent event, float x, float y, int pointer, int button) {
                return true;
            }

            @Override
            public void touchUp(InputEvent event, float x, float y, int pointer, int button) {
                for (NodeInfo n : nodes) {
                    if (Vector2Dist(x, y, n.x, n.y) <= NODE_RADIUS && !n.locked) {
                        onSelect.select(n.index);
                        return;
                    }
                }
            }
        });
    }

    private static float Vector2Dist(float x1, float y1, float x2, float y2) {
        return (float) Math.hypot(x1 - x2, y1 - y2);
    }

    @Override
    public void act(float delta) {
        super.act(delta);
        time += delta;
    }

    @Override
    public void draw(Batch batch, float parentAlpha) {
        localToStageCoordinates(stageOrigin.set(0f, 0f));
        float ox = stageOrigin.x;
        float oy = stageOrigin.y;

        batch.end();
        // batch.end() always disables GL_BLEND as part of its own cleanup, so it must be
        // re-enabled here or these alpha-blended shapes (glow halos, dim path) render fully opaque.
        Gdx.gl.glEnable(GL20.GL_BLEND);
        Gdx.gl.glBlendFunc(GL20.GL_SRC_ALPHA, GL20.GL_ONE_MINUS_SRC_ALPHA);
        shapes.setTransformMatrix(batch.getTransformMatrix());
        shapes.setProjectionMatrix(batch.getProjectionMatrix());

        // path — dim full trail first, then a glowing gold "traveled" overlay up to the current node
        shapes.begin(ShapeRenderer.ShapeType.Filled);
        drawPath(new Color(1f, 1f, 1f, 0.22f), 1.6f, nodes.size, ox, oy);
        int traveled = 1;
        for (int i = 0; i < nodes.size; i++) if (!nodes.get(i).locked) traveled = i + 1;
        float glowA = 0.75f + MathUtils.sin(time * 3f) * 0.2f;
        drawPath(new Color(1f, 0.82f, 0.4f, glowA), 2.4f, traveled, ox, oy);

        shapes.end();
        Gdx.gl.glDisable(GL20.GL_BLEND);

        batch.begin();
        for (NodeInfo n : nodes) {
            drawNode(batch, n, ox, oy);
        }
        batch.end();

        Gdx.gl.glEnable(GL20.GL_BLEND);
        Gdx.gl.glBlendFunc(GL20.GL_SRC_ALPHA, GL20.GL_ONE_MINUS_SRC_ALPHA);
        shapes.begin(ShapeRenderer.ShapeType.Filled);
        for (NodeInfo n : nodes) drawNodeOverlay(n, ox, oy);
        shapes.end();
        Gdx.gl.glDisable(GL20.GL_BLEND);

        batch.begin();
        for (NodeInfo n : nodes) {
            if (n.locked) continue;
            String label = String.valueOf(n.index + 1);
            numberFont.setColor(n.current ? Color.valueOf("2b1a0aff") : Color.valueOf("1a0f2eff"));
            numberFont.draw(batch, label, ox + n.x - NODE_RADIUS, oy + n.y + 8, NODE_RADIUS * 2, Align.center, false);
        }
        numberFont.setColor(Color.WHITE);
    }

    private void drawPath(Color c, float width, int count, float ox, float oy) {
        shapes.setColor(c);
        for (int i = 0; i < count - 1 && i + 1 < nodes.size; i++) {
            NodeInfo a = nodes.get(i), b = nodes.get(i + 1);
            shapes.rectLine(ox + a.x, oy + a.y, ox + b.x, oy + b.y, width);
        }
    }

    private void drawNode(Batch batch, NodeInfo n, float ox, float oy) {
        float x = ox + n.x;
        float y = oy + n.y;
        if (n.locked) {
            assets.drawCircle(batch, new Color(0.02f, 0.02f, 0.04f, 0.42f), x, y, NODE_RADIUS + 7);
            assets.drawCircle(batch, Color.valueOf("171326ff"), x, y, NODE_RADIUS + 4);
            assets.drawCircle(batch, Color.valueOf("292338ff"), x, y, NODE_RADIUS);
            assets.drawCircle(batch, Color.valueOf("151121ff"), x, y, NODE_RADIUS * 0.62f);
            return;
        }

        float pulse = n.current ? 0.5f + MathUtils.sin(time * 4f) * 0.5f : 0f;
        if (n.current) {
            assets.drawCircle(batch, new Color(1f, 0.82f, 0.4f, 0.18f + pulse * 0.24f), x, y, NODE_RADIUS + 14 + pulse * 5);
        }
        assets.drawCircle(batch, new Color(0f, 0f, 0f, 0.5f), x, y, NODE_RADIUS + 7);
        assets.drawCircle(batch, Color.BLACK, x, y, NODE_RADIUS + 3);
        assets.drawCircle(batch, Color.valueOf("2b1750ff"), x, y, NODE_RADIUS);
        assets.drawCircle(batch, Color.valueOf("7d45dbff"), x, y, NODE_RADIUS * 0.8f);
        assets.drawCircle(batch, new Color(0.84f, 0.71f, 1f, 0.92f), x - NODE_RADIUS * 0.28f, y + NODE_RADIUS * 0.3f, NODE_RADIUS * 0.32f);
    }

    private void drawNodeOverlay(NodeInfo n, float ox, float oy) {
        float x = ox + n.x;
        float y = oy + n.y;
        if (n.locked) {
            shapes.setColor(0.6f, 0.56f, 0.78f, 0.9f);
            shapes.circle(x, y - 2, 7, SMALL_CIRCLE_SEGMENTS);
            shapes.setColor(0.16f, 0.14f, 0.22f, 1f);
            shapes.circle(x, y - 2, 4.2f, SMALL_CIRCLE_SEGMENTS);
            shapes.setColor(0.2f, 0.18f, 0.3f, 1f);
            shapes.rect(x - 9, y - 12, 18, 14);
            shapes.setColor(0.6f, 0.56f, 0.78f, 0.9f);
            shapes.circle(x, y - 5, 2, SMALL_CIRCLE_SEGMENTS);
            return;
        }
        if (n.current) {
            shapes.setColor(1f, 0.82f, 0.4f, 1f);
            float ty = y + NODE_RADIUS + 6 + MathUtils.sin(time * 5f) * 2;
            shapes.triangle(x - 6, ty + 8, x + 6, ty + 8, x, ty);
        }
    }
}
