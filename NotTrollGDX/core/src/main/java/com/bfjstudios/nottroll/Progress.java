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

    // ---------------------------------------------------------------- shop
    // Local-only, like everything else here — no backend sync, so spending
    // on this device can't be "restored" by a stale balance from elsewhere.

    public int getCoins() {
        return prefs.getInteger("coins", 0);
    }

    public void addCoins(int amount) {
        prefs.putInteger("coins", getCoins() + amount);
        prefs.flush();
    }

    private boolean spendCoins(int price) {
        int coins = getCoins();
        if (coins < price) return false;
        prefs.putInteger("coins", coins - price);
        prefs.flush();
        return true;
    }

    private java.util.Set<String> ownedSkinSet() {
        String raw = prefs.getString("ownedSkins", "default");
        java.util.Set<String> set = new java.util.HashSet<>();
        for (String id : raw.split(",")) if (!id.isEmpty()) set.add(id);
        return set;
    }

    public boolean ownsSkin(String id) {
        return "default".equals(id) || ownedSkinSet().contains(id);
    }

    /** Returns true if the purchase succeeded (enough coins, not already owned). */
    public boolean buySkin(String id, int price) {
        if (ownsSkin(id) || !spendCoins(price)) return false;
        java.util.Set<String> set = ownedSkinSet();
        set.add(id);
        prefs.putString("ownedSkins", String.join(",", set));
        prefs.flush();
        return true;
    }

    public String getEquippedSkin() {
        return Shop.skin(prefs.getString("equippedSkin", "default")).id;
    }

    public void setEquippedSkin(String id) {
        prefs.putString("equippedSkin", id);
        prefs.flush();
    }

    public boolean isAdsRemoved() {
        return prefs.getBoolean("adsRemoved", false);
    }

    /** Returns true if the purchase succeeded. */
    public boolean buyAdsRemoved(int price) {
        if (isAdsRemoved() || !spendCoins(price)) return false;
        prefs.putBoolean("adsRemoved", true);
        prefs.flush();
        return true;
    }

    public int getCheckpointCharges() {
        return prefs.getInteger("checkpointCharges", 0);
    }

    /** Returns true if the purchase succeeded. */
    public boolean buyCheckpointCharge(int price) {
        if (!spendCoins(price)) return false;
        prefs.putInteger("checkpointCharges", getCheckpointCharges() + 1);
        prefs.flush();
        return true;
    }

    public boolean useCheckpointCharge() {
        int charges = getCheckpointCharges();
        if (charges <= 0) return false;
        prefs.putInteger("checkpointCharges", charges - 1);
        prefs.flush();
        return true;
    }
}
