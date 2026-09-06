package com.bfjstudios.nottroll;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Preferences;

import java.util.UUID;

/** Local persistence, equivalent to the web build's localStorage usage. */
public class Progress {
    private final Preferences prefs;

    public Progress() {
        prefs = Gdx.app.getPreferences(Constants.PREFS_NAME);
        if (!prefs.contains("playerId")) {
            prefs.putString("playerId", "p-" + UUID.randomUUID());
            prefs.flush();
        }
    }

    public int getUnlockedLevels() {
        return Math.max(1, prefs.getInteger("unlockedLevels", 1));
    }

    public void setUnlockedLevels(int value) {
        int current = getUnlockedLevels();
        if (value > current) {
            prefs.putInteger("unlockedLevels", value);
            prefs.flush();
        }
    }

    public boolean isSoundOn() {
        return prefs.getBoolean("soundOn", true);
    }

    public void setSoundOn(boolean on) {
        prefs.putBoolean("soundOn", on);
        prefs.flush();
    }

    public boolean isMusicOn() {
        return prefs.getBoolean("musicOn", true);
    }

    public void setMusicOn(boolean on) {
        prefs.putBoolean("musicOn", on);
        prefs.flush();
    }

    public String getPlayerId() {
        return prefs.getString("playerId");
    }
}
