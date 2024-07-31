import pygame
import startmain
import sound
import game

# 화면 설정
screen_width = 1400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Start slime!")

# 색상 설정
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

# 배경 이미지 로드
mainback_image = pygame.image.load("C:/Users/USER/Desktop/study/game/image/mainback.jpg")
mainback_image = pygame.transform.scale(mainback_image, (screen_width, screen_height))

# 버튼 생성
start_button = startmain.Button(screen_width//2 - 100, screen_height//2 - 25, 200, 50, 'Start', white)
quit_button = startmain.Button(screen_width//2 - 100, screen_height//2 + 75, 200, 50, 'Quit', white)

# 게임 상태 플래그
game_start = False

run = True
sound_instance = sound.Sound()
sound_instance.play_mainmenubgm()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if start_button.isOver(pos):
                game_start = True
                sound_instance.stop_mainmenubgm()  # 메인 메뉴 BGM 중지
                game.run_game(screen, clock, screen_width, screen_height, sound_instance)  # sound_instance를 전달
            if quit_button.isOver(pos):
                run = False

    if not game_start:
        screen.blit(mainback_image, (0, 0))
        start_button.draw(screen, white)
        quit_button.draw(screen, white)
    else:
        pass

    pygame.display.update()

pygame.quit()