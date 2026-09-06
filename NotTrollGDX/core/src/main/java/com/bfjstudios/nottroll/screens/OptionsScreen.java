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

public class OptionsScreen extends ScreenAdapter {
    private final NotTrollGame game;
    private final Screen previous;
    private final Stage stage;
    private TextButton soundBtn, musicBtn;

    public OptionsScreen(NotTrollGame game, Screen previous) {
        this.game = game;
        this.previous = previous;
        stage = new Stage(new FitViewport(Constants.W, Constants.H));

        Table root = new Table();
        root.setFillParent(true);
        stage.addActor(root);

        root.add(new Label("Opciones", game.uiSkin.skin, "h2")).padBottom(28).row();

        soundBtn = new TextButton(soundLabel(), game.uiSkin.skin);
        soundBtn.addListener(new ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                game.progress.setSoundOn(!game.progress.isSoundOn());
                soundBtn.setText(soundLabel());
                game.sfx.click();
            }
        });
        root.add(soundBtn).width(280).height(52).padBottom(14).row();

        musicBtn = new TextButton(musicLabel(), game.uiSkin.skin);
        musicBtn.addListener(new ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                game.progress.setMusicOn(!game.progress.isMusicOn());
                musicBtn.setText(musicLabel());
                game.sfx.click();
            }
        });
        root.add(musicBtn).width(280).height(52).padBottom(24).row();

        TextButton menuBtn = new TextButton("Menu principal", game.uiSkin.skin);
        menuBtn.addListener(new ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                game.sfx.click();
                game.goToMainMenu();
            }
        });
        root.add(menuBtn).width(280).height(52).padBottom(14).row();

        TextButton backBtn = new TextButton("Volver", game.uiSkin.skin);
        backBtn.addListener(new ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                game.sfx.click();
                game.setScreen(previous);
            }
        });
        root.add(backBtn).width(280).height(52);
    }

    private String soundLabel() { return "Sonido: " + (game.progress.isSoundOn() ? "ON" : "OFF"); }
    private String musicLabel() { return "Musica: " + (game.progress.isMusicOn() ? "ON" : "OFF"); }

    @Override
    public void show() {
        Gdx.input.setInputProcessor(stage);
    }

    @Override
    public void render(float delta) {
        Gdx.gl.glClearColor(0.09f, 0.07f, 0.14f, 1f);
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT);
        boolean gameplayActive = previous instanceof GameScreen && !(previous instanceof LevelMapScreen);

        if (!gameplayActive) {
            game.batch.setProjectionMatrix(stage.getViewport().getCamera().combined);
            game.batch.begin();
            game.batch.draw(game.assets.backgroundMenu, 0, 0, Constants.W, Constants.H);
            game.batch.end();

            game.shapes.setProjectionMatrix(stage.getViewport().getCamera().combined);
            Gdx.gl.glEnable(GL20.GL_BLEND);
            game.shapes.begin(com.badlogic.gdx.graphics.glutils.ShapeRenderer.ShapeType.Filled);
            game.shapes.setColor(0.05f, 0.04f, 0.09f, 0.68f);
            game.shapes.rect(0, 0, Constants.W, Constants.H);
            game.shapes.end();
            Gdx.gl.glDisable(GL20.GL_BLEND);
        }

        game.sfx.updateMusic(!gameplayActive, false);
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
