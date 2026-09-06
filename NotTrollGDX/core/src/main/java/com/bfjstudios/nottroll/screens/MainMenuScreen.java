package com.bfjstudios.nottroll.screens;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Input;
import com.badlogic.gdx.ScreenAdapter;
import com.badlogic.gdx.graphics.Color;
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

public class MainMenuScreen extends ScreenAdapter {
    private final NotTrollGame game;
    private final Stage stage;

    public MainMenuScreen(NotTrollGame game) {
        this.game = game;
        stage = new Stage(new FitViewport(Constants.W, Constants.H));

        Table root = new Table();
        root.setFillParent(true);
        stage.addActor(root);

        Label tagline = new Label("Evil Devil", game.uiSkin.skin, "tagline");
        Label title = new Label("Not A Troll Game", game.uiSkin.skin, "h1");

        root.add(tagline).height(40).padBottom(2).row();
        root.add(title).height(34).padBottom(20).row();

        root.add(button("Jugar", () -> {
            game.goToGame(Math.max(0, game.progress.getUnlockedLevels() - 1));
        })).width(270).height(44).padBottom(9).row();

        root.add(button("Niveles", () -> game.goToLevelMap())).width(270).height(44).padBottom(9).row();

        root.add(button("Opciones", () ->
            game.setScreen(new OptionsScreen(game, MainMenuScreen.this)))).width(270).height(44).padBottom(9).row();

        root.add(button("Perfil", () ->
            game.setScreen(new ProfileScreen(game, MainMenuScreen.this)))).width(270).height(44).padBottom(9).row();

        root.add(button("Info", () ->
            game.setScreen(new InfoScreen(game, MainMenuScreen.this)))).width(270).height(44).row();
    }

    private TextButton button(String text, Runnable onClick) {
        TextButton btn = new TextButton(text, game.uiSkin.skin);
        btn.addListener(new ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                game.sfx.click();
                onClick.run();
            }
        });
        return btn;
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

        game.batch.setProjectionMatrix(stage.getViewport().getCamera().combined);
        game.batch.begin();
        game.batch.draw(game.assets.backgroundMenu, 0, 0, Constants.W, Constants.H);
        game.batch.end();

        game.shapes.setProjectionMatrix(stage.getViewport().getCamera().combined);
        Gdx.gl.glEnable(com.badlogic.gdx.graphics.GL20.GL_BLEND);
        game.shapes.begin(com.badlogic.gdx.graphics.glutils.ShapeRenderer.ShapeType.Filled);
        game.shapes.setColor(0.05f, 0.04f, 0.09f, 0.68f);
        game.shapes.rect(0, 0, Constants.W, Constants.H);
        game.shapes.end();
        Gdx.gl.glDisable(com.badlogic.gdx.graphics.GL20.GL_BLEND);

        stage.act(delta);
        stage.draw();

        if (Gdx.input.isKeyJustPressed(Input.Keys.ESCAPE) || Gdx.input.isKeyJustPressed(Input.Keys.BACK)) {
            Gdx.app.exit();
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
