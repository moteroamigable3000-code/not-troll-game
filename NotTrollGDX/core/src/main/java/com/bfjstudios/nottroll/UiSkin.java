package com.bfjstudios.nottroll;

import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.Pixmap;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.NinePatch;
import com.badlogic.gdx.graphics.g2d.TextureRegion;
import com.badlogic.gdx.scenes.scene2d.ui.Label;
import com.badlogic.gdx.scenes.scene2d.ui.ScrollPane;
import com.badlogic.gdx.scenes.scene2d.ui.Skin;
import com.badlogic.gdx.scenes.scene2d.ui.TextButton;
import com.badlogic.gdx.scenes.scene2d.ui.TextField;
import com.badlogic.gdx.scenes.scene2d.utils.Drawable;
import com.badlogic.gdx.scenes.scene2d.utils.NinePatchDrawable;
import com.badlogic.gdx.scenes.scene2d.utils.TextureRegionDrawable;
import com.badlogic.gdx.utils.Array;
import com.badlogic.gdx.utils.Disposable;

/** Procedural pixel-art UI skin (no external atlas) matching the original CSS look. */
public class UiSkin implements Disposable {
    public static final Color GOLD = Color.valueOf("ffd166");
    public static final Color RED = Color.valueOf("ff6b6b");
    public static final Color RED_TAGLINE = Color.valueOf("ff5757");
    public static final Color TEXT = Color.valueOf("f2eefc");
    public static final Color PANEL_FILL = Color.valueOf("1c1730e0");
    public static final Color PANEL_RING = Color.valueOf("4a3a70");
    public static final Color BTN_FILL = Color.valueOf("2b2246");
    public static final Color BTN_FILL_OVER = Color.valueOf("3a2e5e");
    public static final Color BTN_FILL_DISABLED = Color.valueOf("1c1830");

    public final Skin skin = new Skin();
    private final Array<Texture> owned = new Array<>();
    private final Texture whiteTex;

    public UiSkin(Assets assets) {
        Pixmap pm = new Pixmap(4, 4, Pixmap.Format.RGBA8888);
        pm.setColor(1, 1, 1, 1);
        pm.fill();
        whiteTex = new Texture(pm);
        pm.dispose();
        owned.add(whiteTex);

        skin.add("pxHuge", assets.pxHuge);
        skin.add("pxLarge", assets.pxLarge);
        skin.add("pxMed", assets.pxMed);
        skin.add("pxSmall", assets.pxSmall);
        skin.add("pxTiny", assets.pxTiny);
        skin.add("vtBody", assets.vtBody);

        addLabelStyle("h1", assets.pxLarge, Color.WHITE);
        addLabelStyle("h2", assets.pxMed, GOLD);
        addLabelStyle("tagline", assets.pxHuge, RED_TAGLINE);
        addLabelStyle("hud", assets.pxTiny, TEXT);
        addLabelStyle("body", assets.vtBody, TEXT);
        addLabelStyle("small", assets.pxTiny, TEXT);
        addLabelStyle("node", assets.pxSmall, Color.valueOf("1a0f2e"));

        TextButton.TextButtonStyle btnStyle = new TextButton.TextButtonStyle();
        btnStyle.up = buttonPatch(BTN_FILL, true);
        btnStyle.down = buttonPatch(BTN_FILL_OVER, false);
        btnStyle.over = buttonPatch(BTN_FILL_OVER, true);
        btnStyle.disabled = buttonPatch(BTN_FILL_DISABLED, false);
        btnStyle.font = assets.pxSmall;
        btnStyle.fontColor = TEXT;
        btnStyle.disabledFontColor = new Color(1, 1, 1, 0.5f);
        skin.add("default", btnStyle);

        TextButton.TextButtonStyle hudBtnStyle = new TextButton.TextButtonStyle();
        hudBtnStyle.up = buttonPatch(BTN_FILL, true, 1, 12);
        hudBtnStyle.down = buttonPatch(BTN_FILL_OVER, false, 1, 12);
        hudBtnStyle.over = buttonPatch(BTN_FILL_OVER, true, 1, 12);
        hudBtnStyle.font = assets.pxTiny;
        hudBtnStyle.fontColor = TEXT;
        skin.add("hud", hudBtnStyle);

        ScrollPane.ScrollPaneStyle scrollStyle = new ScrollPane.ScrollPaneStyle();
        scrollStyle.background = null;
        scrollStyle.vScroll = flat(new Color(0, 0, 0, 0.2f));
        scrollStyle.vScrollKnob = flat(new Color(0.7f, 0.4f, 1f, 0.6f));
        scrollStyle.hScroll = flat(new Color(0, 0, 0, 0.2f));
        scrollStyle.hScrollKnob = flat(new Color(0.7f, 0.4f, 1f, 0.6f));
        skin.add("default", scrollStyle);

        TextField.TextFieldStyle fieldStyle = new TextField.TextFieldStyle();
        fieldStyle.font = assets.vtBody;
        fieldStyle.fontColor = TEXT;
        fieldStyle.background = buttonPatch(Color.valueOf("17132a"), false);
        fieldStyle.cursor = flat(Color.WHITE);
        fieldStyle.selection = flat(new Color(0.4f, 0.3f, 0.7f, 0.6f));
        skin.add("default", fieldStyle);
    }

    private void addLabelStyle(String name, BitmapFont font, Color color) {
        skin.add(name, new Label.LabelStyle(font, color));
    }

    /** A dark bordered panel, approximating .screenOverlay (border 3 black + purple ring + dark fill). */
    public Drawable panel() {
        int border = 3, ring = 3, inner = 24;
        int total = border * 2 + ring * 2 + inner;
        Pixmap p = new Pixmap(total, total, Pixmap.Format.RGBA8888);
        p.setColor(PANEL_FILL);
        p.fill();
        p.setColor(PANEL_RING);
        p.fillRectangle(border, border, total - border * 2, total - border * 2);
        p.setColor(PANEL_FILL);
        p.fillRectangle(border + ring, border + ring, total - (border + ring) * 2, total - (border + ring) * 2);
        Texture tex = new Texture(p);
        p.dispose();
        owned.add(tex);
        int fixed = border + ring;
        return new NinePatchDrawable(new NinePatch(tex, fixed, fixed, fixed, fixed));
    }

    private Drawable buttonPatch(Color fill, boolean withShadow) {
        return buttonPatch(fill, withShadow, 2, 32);
    }

    private Drawable buttonPatch(Color fill, boolean withShadow, int border, int inner) {
        int shadow = withShadow ? Math.max(2, border * 2) : 0;
        int total = inner + border * 2 + shadow;
        Pixmap p = new Pixmap(total, total, Pixmap.Format.RGBA8888);
        p.setColor(0, 0, 0, 0);
        p.fill();
        if (withShadow) {
            p.setColor(0, 0, 0, 1);
            p.fillRectangle(shadow, shadow, inner + border * 2, inner + border * 2);
        }
        p.setColor(0, 0, 0, 1);
        p.fillRectangle(0, 0, inner + border * 2, inner + border * 2);
        p.setColor(fill);
        p.fillRectangle(border, border, inner, inner);
        Texture tex = new Texture(p);
        p.dispose();
        owned.add(tex);
        int rightBottom = border + shadow;
        return new NinePatchDrawable(new NinePatch(tex, border, rightBottom, border, rightBottom));
    }

    private Drawable flat(Color c) {
        TextureRegionDrawable d = new TextureRegionDrawable(new TextureRegion(whiteTex));
        return d.tint(c);
    }

    @Override
    public void dispose() {
        skin.dispose();
        for (Texture t : owned) t.dispose();
    }
}
