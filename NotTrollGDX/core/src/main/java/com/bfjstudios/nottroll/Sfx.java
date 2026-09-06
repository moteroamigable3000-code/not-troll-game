package com.bfjstudios.nottroll;

public class Sfx {
    private final Assets assets;
    private final Progress progress;

    public Sfx(Assets assets, Progress progress) {
        this.assets = assets;
        this.progress = progress;
    }

    private boolean on() { return progress.isSoundOn(); }

    public void jump() { if (on()) assets.sndJump.play(0.6f); }
    public void land() { if (on()) assets.sndLand.play(0.6f); }
    public void death() { if (on()) assets.sndDeath.play(0.7f); }
    public void goal() { if (on()) assets.sndGoal.play(0.7f); }
    public void pop() { if (on()) assets.sndPop.play(0.6f); }
    public void crumble() { if (on()) assets.sndCrumble.play(0.6f); }
    public void boom() { if (on()) assets.sndBoom.play(0.8f); }
    public void click() { if (on()) assets.sndClick.play(0.5f); }

    /** menuVisible: main menu or level map currently shown. playing: gameplay screen active and not paused. */
    public void updateMusic(boolean menuVisible, boolean playingGameplay) {
        boolean musicOn = progress.isMusicOn();
        boolean wantGameplay = musicOn && playingGameplay;
        boolean wantMenu = musicOn && menuVisible;

        if (wantGameplay && !assets.musicGameplay.isPlaying()) assets.musicGameplay.play();
        else if (!wantGameplay && assets.musicGameplay.isPlaying()) assets.musicGameplay.pause();

        if (wantMenu && !assets.musicMenu.isPlaying()) assets.musicMenu.play();
        else if (!wantMenu && assets.musicMenu.isPlaying()) assets.musicMenu.pause();
    }

    public void stopAll() {
        assets.musicGameplay.stop();
        assets.musicMenu.stop();
        assets.splashSound.stop();
    }
}
