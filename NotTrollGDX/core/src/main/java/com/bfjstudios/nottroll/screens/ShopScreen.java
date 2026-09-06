package com.bfjstudios.nottroll.screens;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Input;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.ScreenAdapter;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.g2d.TextureRegion;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import com.badlogic.gdx.scenes.scene2d.InputEvent;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.ui.Image;
import com.badlogic.gdx.scenes.scene2d.ui.Label;
import com.badlogic.gdx.scenes.scene2d.ui.Table;
import com.badlogic.gdx.scenes.scene2d.ui.TextButton;
import com.badlogic.gdx.scenes.scene2d.utils.ClickListener;
import com.badlogic.gdx.scenes.scene2d.utils.TextureRegionDrawable;
import com.badlogic.gdx.utils.Array;
import com.badlogic.gdx.utils.viewport.FitViewport;
import com.bfjstudios.nottroll.Constants;
import com.bfjstudios.nottroll.NotTrollGame;
import com.bfjstudios.nottroll.Shop;
import com.bfjstudios.nottroll.UiSkin;

public class ShopScreen extends ScreenAdapter {
    private final NotTrollGame game;
    private final Screen previous;
    private final Stage stage;

    private Label coinLabel;
    private final Array<TextButton> skinButtons = new Array<>();
    private TextButton adsBtn, checkpointBtn;
    private Label checkpointCountLabel;

    public ShopScreen(NotTrollGame game, Screen previous) {
        this.game = game;
        this.previous = previous;
        stage = new Stage(new FitViewport(Constants.W, Constants.H));

        Table root = new Table();
        root.setFillParent(true);
        stage.addActor(root);

        root.add(new Label("Tienda", game.uiSkin.skin, "h2")).padBottom(14).row();

        coinLabel = new Label("", game.uiSkin.skin, "body");
        coinLabel.setColor(UiSkin.GOLD);
        root.add(coinLabel).padBottom(18).row();

        for (Shop.SkinDef skin : Shop.SKINS) {
            Table row = new Table();
            Image swatch = colorImage(skin.color);
            row.add(swatch).size(20, 20).padRight(10);
            row.add(new Label(skin.name, game.uiSkin.skin, "small")).width(170).left();

            TextButton btn = new TextButton("", game.uiSkin.skin);
            btn.addListener(new ClickListener() {
                @Override
                public void clicked(InputEvent event, float x, float y) {
                    game.sfx.click();
                    if (!game.progress.getEquippedSkin().equals(skin.id)) {
                        if (game.progress.ownsSkin(skin.id)) {
                            game.progress.setEquippedSkin(skin.id);
                        } else {
                            game.progress.buySkin(skin.id, skin.price);
                        }
                    }
                    refresh();
                }
            });
            row.add(btn).width(150).height(44).padLeft(10);
            skinButtons.add(btn);
            root.add(row).padBottom(10).row();
        }

        Table adsRow = new Table();
        adsRow.add(new Label("Apoya el juego\n(sin anuncios)", game.uiSkin.skin, "small")).width(230).left();
        adsBtn = new TextButton("", game.uiSkin.skin);
        adsBtn.addListener(new ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                game.sfx.click();
                game.progress.buyAdsRemoved(Shop.ADS_OFF_PRICE);
                refresh();
            }
        });
        adsRow.add(adsBtn).width(150).height(44).padLeft(10);
        root.add(adsRow).padBottom(10).row();

        Table cpRow = new Table();
        checkpointCountLabel = new Label("", game.uiSkin.skin, "small");
        cpRow.add(checkpointCountLabel).width(230).left();
        checkpointBtn = new TextButton("", game.uiSkin.skin);
        checkpointBtn.addListener(new ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                game.sfx.click();
                game.progress.buyCheckpointCharge(Shop.CHECKPOINT_PRICE);
                refresh();
            }
        });
        cpRow.add(checkpointBtn).width(150).height(44).padLeft(10);
        root.add(cpRow).padBottom(24).row();

        TextButton backBtn = new TextButton("Volver", game.uiSkin.skin);
        backBtn.addListener(new ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                game.sfx.click();
                game.setScreen(previous);
            }
        });
        root.add(backBtn).width(280).height(52);

        refresh();
    }

    private void refresh() {
        coinLabel.setText("Monedas: " + game.progress.getCoins());
        for (int i = 0; i < Shop.SKINS.size; i++) {
            Shop.SkinDef skin = Shop.SKINS.get(i);
            TextButton btn = skinButtons.get(i);
            boolean equipped = game.progress.getEquippedSkin().equals(skin.id);
            boolean owned = game.progress.ownsSkin(skin.id);
            if (equipped) {
                btn.setText("Equipado");
                btn.setDisabled(true);
            } else if (owned) {
                btn.setText("Equipar");
                btn.setDisabled(false);
            } else {
                btn.setText("Comprar (" + skin.price + ")");
                btn.setDisabled(game.progress.getCoins() < skin.price);
            }
        }
        if (game.progress.isAdsRemoved()) {
            adsBtn.setText("Comprado");
            adsBtn.setDisabled(true);
        } else {
            adsBtn.setText("Comprar (" + Shop.ADS_OFF_PRICE + ")");
            adsBtn.setDisabled(game.progress.getCoins() < Shop.ADS_OFF_PRICE);
        }
        checkpointCountLabel.setText("Bandera de control (" + game.progress.getCheckpointCharges() + ")");
        checkpointBtn.setText("Comprar (" + Shop.CHECKPOINT_PRICE + ")");
        checkpointBtn.setDisabled(game.progress.getCoins() < Shop.CHECKPOINT_PRICE);
    }

    private Image colorImage(Color c) {
        Image img = new Image(new TextureRegionDrawable(new TextureRegion(game.assets.pixel)));
        img.setColor(c);
        return img;
    }

    @Override
    public void show() {
        Gdx.input.setInputProcessor(stage);
        refresh();
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
            game.shapes.begin(ShapeRenderer.ShapeType.Filled);
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
