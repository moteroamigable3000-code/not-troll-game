package com.bfjstudios.nottroll.screens;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Input;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.ScreenAdapter;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.scenes.scene2d.InputEvent;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.ui.Container;
import com.badlogic.gdx.scenes.scene2d.ui.Label;
import com.badlogic.gdx.scenes.scene2d.ui.ScrollPane;
import com.badlogic.gdx.scenes.scene2d.ui.Stack;
import com.badlogic.gdx.scenes.scene2d.ui.Table;
import com.badlogic.gdx.scenes.scene2d.ui.TextButton;
import com.badlogic.gdx.scenes.scene2d.utils.ClickListener;
import com.badlogic.gdx.utils.Array;
import com.badlogic.gdx.utils.viewport.FitViewport;
import com.bfjstudios.nottroll.Constants;
import com.bfjstudios.nottroll.NotTrollGame;

/** Vertical, winding level trail — a functional + visual analogue of the web build's zig-zag SVG map. */
public class LevelMapScreen extends ScreenAdapter {
    private static final float NODE_STEP = 92f;
    private static final float TOP_PAD = 60f;
    private static final float BOTTOM_PAD = 70f;
    private static final float BOX_W = 860f;
    private static final float BOX_H = 390f;

    private final NotTrollGame game;
    private final Screen returnScreen; // non-null when opened from a paused GameScreen
    private final Stage stage;
    private final ScrollPane scrollPane;
    private float focusScrollY;

    public LevelMapScreen(NotTrollGame game) {
        this(game, null);
    }

    public LevelMapScreen(NotTrollGame game, Screen returnScreen) {
        this.game = game;
        this.returnScreen = returnScreen;
        stage = new Stage(new FitViewport(Constants.W, Constants.H));

        Table root = new Table();
        root.setFillParent(true);
        stage.addActor(root);

        Label title = new Label("Selecciona un nivel", game.uiSkin.skin, "h2");
        root.add(title).padTop(10).row();

        int count = game.assets.levels.size;
        int unlocked = game.progress.getUnlockedLevels();
        float viewportW = BOX_W - 8;
        float viewportH = BOX_H - 8;
        float contentH = Math.max(viewportH, TOP_PAD + BOTTOM_PAD + Math.max(0, count - 1) * NODE_STEP);

        Array<TrailActor.NodeInfo> infos = new Array<>();
        for (int i = 0; i < count; i++) {
            double xPct = 50 + 30 * Math.sin(i * 0.85 + 0.6) + 9 * Math.sin(i * 2.3 + 1.4);
            xPct = Math.min(86, Math.max(14, xPct));
            float topY = contentH - BOTTOM_PAD - i * NODE_STEP;

            TrailActor.NodeInfo n = new TrailActor.NodeInfo();
            n.x = (float) (xPct / 100.0) * viewportW;
            n.y = contentH - topY;
            n.index = i;
            n.locked = i >= unlocked || game.assets.levels.get(i).locked;
            n.current = !n.locked && i == unlocked - 1;
            infos.add(n);
            if (n.current) {
                focusScrollY = Math.max(0, Math.min(contentH - viewportH, (contentH - n.y) - viewportH / 2f));
            }
        }

        TrailActor trail = new TrailActor(infos, game.assets, game.shapes, game.assets.pxSmall, index -> {
            game.sfx.click();
            game.goToGame(index);
        });
        trail.setSize(viewportW, contentH);

        scrollPane = new ScrollPane(trail, game.uiSkin.skin);
        scrollPane.setScrollingDisabled(true, false);
        scrollPane.setFadeScrollBars(false);
        scrollPane.setOverscroll(false, true);

        MapBackdropActor backdrop = new MapBackdropActor(game.shapes);

        Stack mapStack = new Stack();
        mapStack.add(backdrop);
        mapStack.add(scrollPane);

        Container<Stack> framed = new Container<>(mapStack);
        framed.setBackground(game.uiSkin.panel());
        framed.size(BOX_W, BOX_H);
        framed.fill();

        root.add(framed).padTop(6).row();

        TextButton backBtn = new TextButton("Volver", game.uiSkin.skin);
        backBtn.addListener(new ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                game.sfx.click();
                goBack();
            }
        });
        root.add(backBtn).width(220).height(46).padTop(12);
    }

    private void goBack() {
        if (returnScreen != null) game.setScreen(returnScreen);
        else game.goToMainMenu();
    }

    @Override
    public void show() {
        Gdx.input.setInputProcessor(stage);
        stage.getRoot().addAction(com.badlogic.gdx.scenes.scene2d.actions.Actions.delay(0.01f,
            com.badlogic.gdx.scenes.scene2d.actions.Actions.run(() -> {
                scrollPane.layout();
                scrollPane.setScrollY(focusScrollY);
                scrollPane.updateVisualScroll();
            })));
    }

    @Override
    public void render(float delta) {
        Gdx.gl.glClearColor(0.06f, 0.05f, 0.09f, 1f);
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT);

        boolean pausedGame = returnScreen instanceof GameScreen;
        game.sfx.updateMusic(!pausedGame, false);

        stage.act(delta);
        stage.draw();

        if (Gdx.input.isKeyJustPressed(Input.Keys.ESCAPE) || Gdx.input.isKeyJustPressed(Input.Keys.BACK)) {
            goBack();
        }
    }

    @Override
    public void resize(int width, int height) {
        stage.getViewport().update(width, height, true);
    }

    @Override
    public void dispose() {
        stage.dispose();
    }
}
