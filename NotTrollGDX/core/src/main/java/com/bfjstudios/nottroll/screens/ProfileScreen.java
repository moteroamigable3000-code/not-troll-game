package com.bfjstudios.nottroll.screens;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Input;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.ScreenAdapter;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.scenes.scene2d.InputEvent;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.ui.Label;
import com.badlogic.gdx.scenes.scene2d.ui.Table;
import com.badlogic.gdx.scenes.scene2d.ui.TextButton;
import com.badlogic.gdx.scenes.scene2d.utils.ClickListener;
import com.badlogic.gdx.utils.viewport.FitViewport;
import com.bfjstudios.nottroll.Constants;
import com.bfjstudios.nottroll.NotTrollGame;
import com.bfjstudios.nottroll.UiSkin;

/** Local-only profile summary — cloud accounts from the web build aren't wired up yet. */
public class ProfileScreen extends ScreenAdapter {
    private final NotTrollGame game;
    private final Screen previous;
    private final Stage stage;

    public ProfileScreen(NotTrollGame game, Screen previous) {
        this.game = game;
        this.previous = previous;
        stage = new Stage(new FitViewport(Constants.W, Constants.H));

        Table root = new Table();
        root.setFillParent(true);
        stage.addActor(root);

        root.add(new Label("Perfil", game.uiSkin.skin, "h2")).padBottom(24).row();

        Label welcome = new Label("Jugador local", game.uiSkin.skin, "pxMed");
        welcome.setColor(UiSkin.GOLD);
        root.add(welcome).padBottom(10).row();

        Label hint = new Label("Tu progreso se guarda en este dispositivo.", game.uiSkin.skin, "body");
        root.add(hint).padBottom(6).row();

        Label unlocked = new Label("Niveles desbloqueados: " + game.progress.getUnlockedLevels(), game.uiSkin.skin, "body");
        root.add(unlocked).padBottom(24).row();

        TextButton backBtn = new TextButton("Volver", game.uiSkin.skin);
        backBtn.addListener(new ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                game.sfx.click();
                game.setScreen(previous);
            }
        });
        root.add(backBtn).width(220).height(48);
    }

    @Override
    public void show() {
        Gdx.input.setInputProcessor(stage);
    }

    @Override
    public void render(float delta) {
        Gdx.gl.glClearColor(0.09f, 0.07f, 0.14f, 1f);
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT);
        game.sfx.updateMusic(true, false);
        stage.act(delta);
        stage.draw();
        if (Gdx.input.isKeyJustPressed(Input.Keys.ESCAPE) || Gdx.input.isKeyJustPressed(Input.Keys.BACK)) {
            game.setScreen(previous);
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
