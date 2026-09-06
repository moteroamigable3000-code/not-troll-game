package com.bfjstudios.nottroll;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import com.bfjstudios.nottroll.screens.GameScreen;
import com.bfjstudios.nottroll.screens.LevelMapScreen;
import com.bfjstudios.nottroll.screens.MainMenuScreen;
import com.bfjstudios.nottroll.screens.SplashScreen;

public class NotTrollGame extends Game {
    public Assets assets;
    public Progress progress;
    public Sfx sfx;
    public UiSkin uiSkin;

    public SpriteBatch batch;
    public ShapeRenderer shapes;

    /** How many levels of total_levels are unlocked/attempted, mirrors totalDeaths across a run. */
    public int totalDeaths = 0;

    @Override
    public void create() {
        batch = new SpriteBatch();
        shapes = new ShapeRenderer();
        assets = new Assets();
        progress = new Progress();
        sfx = new Sfx(assets, progress);
        uiSkin = new UiSkin(assets);

        setScreen(new SplashScreen(this));
    }

    public void goToMainMenu() {
        setScreen(new MainMenuScreen(this));
    }

    public void goToLevelMap() {
        setScreen(new LevelMapScreen(this));
    }

    public void goToGame(int levelIndex) {
        setScreen(new GameScreen(this, levelIndex));
    }

    @Override
    public void dispose() {
        com.badlogic.gdx.Screen current = getScreen();
        if (current != null) current.dispose();
        uiSkin.dispose();
        assets.dispose();
        batch.dispose();
        shapes.dispose();
    }
}
