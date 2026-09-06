package com.bfjstudios.nottroll;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.audio.Music;
import com.badlogic.gdx.audio.Sound;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.freetype.FreeTypeFontGenerator;
import com.badlogic.gdx.graphics.g2d.freetype.FreeTypeFontGenerator.FreeTypeFontParameter;
import com.badlogic.gdx.utils.Array;
import com.badlogic.gdx.utils.Disposable;
import com.bfjstudios.nottroll.data.LevelDef;
import com.bfjstudios.nottroll.data.LevelLoader;

public class Assets implements Disposable {
    public final Texture backgroundGame;
    public final Texture backgroundMenu;
    public final Texture splashLogo;
    public final Texture iconStore;
    public final Texture pixel; // 1x1 white, tinted for shape drawing
    public final Texture softCircle; // white radial disc, tinted for smooth UI nodes

    // Pixel-art fonts (baked white + black border/shadow; tint per Label for color)
    public final BitmapFont pxHuge;   // 36 — "Evil Devil" tagline
    public final BitmapFont pxLarge;  // 30 — h1 titles
    public final BitmapFont pxMed;    // 18 — h2 headings
    public final BitmapFont pxSmall;  // 13 — buttons, node numbers
    public final BitmapFont pxTiny;   // 10 — HUD labels, small hud buttons
    public final BitmapFont vtBody;   // 26 — hints / body text (VT323)

    public final Sound sndJump, sndLand, sndDeath, sndGoal, sndPop, sndCrumble, sndBoom, sndClick;
    public final Music musicGameplay, musicMenu;
    public final Sound splashSound;

    public final Array<LevelDef> levels;

    public Assets() {
        backgroundGame = new Texture(Gdx.files.internal("FONDO_JUEGO.png"));
        backgroundMenu = new Texture(Gdx.files.internal("FONDO_MENU_OPCIONES.png"));
        splashLogo = new Texture(Gdx.files.internal("EMPRESA.png"));
        iconStore = new Texture(Gdx.files.internal("ICON_STORE.png"));
        backgroundGame.setFilter(Texture.TextureFilter.Linear, Texture.TextureFilter.Linear);
        backgroundMenu.setFilter(Texture.TextureFilter.Linear, Texture.TextureFilter.Linear);
        splashLogo.setFilter(Texture.TextureFilter.Linear, Texture.TextureFilter.Linear);
        iconStore.setFilter(Texture.TextureFilter.Linear, Texture.TextureFilter.Linear);

        com.badlogic.gdx.graphics.Pixmap pm = new com.badlogic.gdx.graphics.Pixmap(1, 1, com.badlogic.gdx.graphics.Pixmap.Format.RGBA8888);
        pm.setColor(1, 1, 1, 1);
        pm.fill();
        pixel = new Texture(pm);
        pm.dispose();
        softCircle = makeSoftCircleTexture(192);

        FreeTypeFontGenerator pixelGen = new FreeTypeFontGenerator(Gdx.files.internal("fonts/PressStart2P-Regular.ttf"));
        pxHuge = genFont(pixelGen, 36, 1, 3);
        pxLarge = genFont(pixelGen, 30, 1, 3);
        pxMed = genFont(pixelGen, 18, 1, 2);
        pxSmall = genFont(pixelGen, 13, 1, 2);
        pxTiny = genFont(pixelGen, 11, 1, 1);
        pixelGen.dispose();

        FreeTypeFontGenerator vtGen = new FreeTypeFontGenerator(Gdx.files.internal("fonts/VT323-Regular.ttf"));
        FreeTypeFontParameter vtParam = new FreeTypeFontParameter();
        vtParam.size = 28;
        vtParam.color = Color.WHITE;
        vtParam.shadowColor = new Color(0, 0, 0, 0.9f);
        vtParam.shadowOffsetX = 2;
        vtParam.shadowOffsetY = 2;
        vtParam.minFilter = com.badlogic.gdx.graphics.Texture.TextureFilter.Linear;
        vtParam.magFilter = com.badlogic.gdx.graphics.Texture.TextureFilter.Linear;
        vtBody = vtGen.generateFont(vtParam);
        vtGen.dispose();

        sndJump = Gdx.audio.newSound(Gdx.files.internal("sfx/jump.wav"));
        sndLand = Gdx.audio.newSound(Gdx.files.internal("sfx/land.wav"));
        sndDeath = Gdx.audio.newSound(Gdx.files.internal("sfx/death.wav"));
        sndGoal = Gdx.audio.newSound(Gdx.files.internal("sfx/goal.wav"));
        sndPop = Gdx.audio.newSound(Gdx.files.internal("sfx/pop.wav"));
        sndCrumble = Gdx.audio.newSound(Gdx.files.internal("sfx/crumble.wav"));
        sndBoom = Gdx.audio.newSound(Gdx.files.internal("sfx/boom.wav"));
        sndClick = Gdx.audio.newSound(Gdx.files.internal("sfx/clic.wav"));

        musicGameplay = Gdx.audio.newMusic(Gdx.files.internal("sfx/musica_indie_gameplay.wav"));
        musicGameplay.setLooping(true);
        musicGameplay.setVolume(0.35f);
        musicMenu = Gdx.audio.newMusic(Gdx.files.internal("sfx/musica_menu_y_mapa.wav"));
        musicMenu.setLooping(true);
        musicMenu.setVolume(0.35f);
        splashSound = Gdx.audio.newSound(Gdx.files.internal("sfx/splash_inicio.mp3"));

        levels = LevelLoader.loadAll("levels.json");
    }

    private BitmapFont genFont(FreeTypeFontGenerator gen, int size, int border, int shadow) {
        FreeTypeFontParameter p = new FreeTypeFontParameter();
        p.size = size;
        p.color = Color.WHITE;
        p.borderWidth = border;
        p.borderColor = Color.BLACK;
        p.shadowColor = new Color(0, 0, 0, 0.8f);
        p.shadowOffsetX = shadow;
        p.shadowOffsetY = shadow;
        p.minFilter = com.badlogic.gdx.graphics.Texture.TextureFilter.Linear;
        p.magFilter = com.badlogic.gdx.graphics.Texture.TextureFilter.Linear;
        return gen.generateFont(p);
    }

    private Texture makeSoftCircleTexture(int size) {
        com.badlogic.gdx.graphics.Pixmap pm = new com.badlogic.gdx.graphics.Pixmap(size, size, com.badlogic.gdx.graphics.Pixmap.Format.RGBA8888);
        float center = (size - 1) * 0.5f;
        float radius = center - 2f;
        for (int y = 0; y < size; y++) {
            for (int x = 0; x < size; x++) {
                float dx = x - center;
                float dy = y - center;
                float dist = (float) Math.sqrt(dx * dx + dy * dy);
                float alpha = Math.max(0f, Math.min(1f, radius + 1f - dist));
                pm.setColor(1f, 1f, 1f, alpha);
                pm.drawPixel(x, y);
            }
        }
        Texture texture = new Texture(pm);
        texture.setFilter(Texture.TextureFilter.Linear, Texture.TextureFilter.Linear);
        pm.dispose();
        return texture;
    }

    public void drawCircle(com.badlogic.gdx.graphics.g2d.Batch batch, Color color, float cx, float cy, float radius) {
        batch.setColor(color);
        batch.draw(softCircle, cx - radius, cy - radius, radius * 2f, radius * 2f);
        batch.setColor(Color.WHITE);
    }

    @Override
    public void dispose() {
        backgroundGame.dispose();
        backgroundMenu.dispose();
        splashLogo.dispose();
        iconStore.dispose();
        pixel.dispose();
        softCircle.dispose();
        pxHuge.dispose(); pxLarge.dispose(); pxMed.dispose(); pxSmall.dispose(); pxTiny.dispose(); vtBody.dispose();
        sndJump.dispose(); sndLand.dispose(); sndDeath.dispose(); sndGoal.dispose();
        sndPop.dispose(); sndCrumble.dispose(); sndBoom.dispose(); sndClick.dispose();
        musicGameplay.dispose(); musicMenu.dispose(); splashSound.dispose();
    }
}
