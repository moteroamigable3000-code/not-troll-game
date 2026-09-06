package com.bfjstudios.nottroll;

import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.utils.Array;

/** Coin-shop catalog — mirrors the SKINS table in the web build's game.js. */
public class Shop {
    public static final int ADS_OFF_PRICE = 150;
    public static final int CHECKPOINT_PRICE = 25;
    public static final int COINS_PER_LEVEL = 15;

    public static class SkinDef {
        public final String id, name;
        public final Color color;
        public final int price;
        public SkinDef(String id, String name, Color color, int price) {
            this.id = id; this.name = name; this.color = color; this.price = price;
        }
    }

    public static final Array<SkinDef> SKINS = new Array<>();
    static {
        SKINS.add(new SkinDef("default", "Negro clasico", new Color(0.08f, 0.08f, 0.08f, 1f), 0));
        SKINS.add(new SkinDef("white", "Blanco fantasma", Color.valueOf("f2eefcff"), 60));
    }

    public static SkinDef skin(String id) {
        for (SkinDef s : SKINS) if (s.id.equals(id)) return s;
        return SKINS.first();
    }

    public static Color skinColor(String id) {
        return skin(id).color;
    }
}
