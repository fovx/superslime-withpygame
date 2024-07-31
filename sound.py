import pygame

class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.bgm = pygame.mixer.Sound("C:/Users/USER/Desktop/study/game/sound/mainmenu.mp3")
        self.jump_sound = pygame.mixer.Sound("C:/Users/USER/Desktop/study/game/sound/jump.mp3")
        self.mainmenu_bgm = pygame.mixer.Sound("C:/Users/USER/Desktop/study/game/sound/good.mp3")

    def play_bgm(self, loops=-1):
        pygame.mixer.Sound.stop(self.mainmenu_bgm)  # 메인 메뉴 BGM 중지
        self.bgm.play(loops)

    def play_jump(self, loops=0):
        self.jump_sound.play(loops)

    def play_mainmenubgm(self, loops=-1):
        self.mainmenu_bgm.play(loops)

    def stop_mainmenubgm(self):
        pygame.mixer.Sound.stop(self.mainmenu_bgm)

    def stop_all(self):
        pygame.mixer.stop()
