import pygame.mixer_music as music_player


class Jukebox:
    def __init__(self):
        self.now_playing = None

    # play music
    def play(self, music):
        if not music:
            return
        if self.now_playing != music:
            music_player.load(music)
            music_player.play(-1)
            # music_player.set_volume(0.5)
            self.now_playing = music

    # stop music
    def stop_music(self):
        music_player.stop()
        self.now_playing = None
