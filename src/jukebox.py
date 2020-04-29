import pygame.mixer_music as music_player

class JukeBox():
    def __init__(self):
        self.now_playing = None

    def play(self, music):
        if self.now_playing != music:
            music_player.load(music)
            music_player.play(-1)
            self.now_playing = music

    def stop_music():
        music_player.stop()
        self.now_playing = None