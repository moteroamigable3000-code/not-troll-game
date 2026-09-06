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

public class InfoScreen extends ScreenAdapter {
    private final NotTrollGame game;
    private final Screen previous;
    private final Stage stage;

    public InfoScreen(NotTrollGame game, Screen previous) {
        this.game = game;
        this.previous = previous;
        stage = new Stage(new FitViewport(Constants.W, Constants.H));

        Table root = new Table();
        root.setFillParent(true);
        root.top().padTop(30);
        stage.addActor(root);

        root.add(new Label("Info", game.uiSkin.skin, "h2")).padBottom(20).row();

        String body = "Not A Troll Game es un plataformero de precision\n"
            + "pixel-art donde cada salto y cada decision importan.\n\n"
            + "Controles:\n"
            + "Flechas / A-D: moverse\n"
            + "Espacio / Arriba: saltar\n"
            + "R: reiniciar nivel\n"
            + "Esc: abrir mapa de niveles\n\n"
            + "Desarrollado por BFJ Studios";
        Label bodyLabel = new Label(body, game.uiSkin.skin, "body");
        bodyLabel.setAlignment(com.badlogic.gdx.utils.Align.center);
        root.add(bodyLabel).padBottom(24).row();

        Label copyright = new Label("(c) BFJ GAMES PE - Todos los derechos reservados", game.uiSkin.skin, "body");
        copyright.setFontScale(0.6f);
        copyright.setColor(0.54f, 0.5f, 0.66f, 1f);
        root.add(copyright).padBottom(24).row();

        TextButton backBtn = new TextButton("Volver", game.uiSkin.skin);
        backBtn.addListener(new ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                game.sfx.click();
                game.setScreen(previous);
            }
        });
        root.add(backBtn).width(220).height(50);
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
