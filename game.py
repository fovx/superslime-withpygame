import pygame
from character import Character, Camera
import entity

def run_game(screen, clock, screen_width, screen_height, sound_instance):
    sound_instance.play_bgm()  # 게임 BGM 시작

    player = Character(screen_height, sound_instance)
    background_width = screen_width * 2
    background_height = screen_height
    camera = Camera(screen_width, screen_height, background_width, background_height)
    
    game_background = pygame.image.load("C:/Users/USER/Desktop/study/game/image/background.png")
    game_background = pygame.transform.scale(game_background, (background_width, background_height))

    # 맵 전체 하단에 발판 추가
    ground_height = 20
    platforms = [
        entity.Platform(0, screen_height - ground_height, background_width, ground_height),
        entity.Platform(300, 300, 200, 20),
        entity.Platform(500, 250, 200, 20),
        entity.Platform(600, 250, 200, 20),
        entity.Platform(900, 200, 200, 20),
        entity.Platform(1200, 300, 200, 20),
        entity.Platform(1500, 250, 200, 20),
        entity.Platform(1800, 200, 200, 20)
    ]

    monsters = [
        entity.Monster(400, 270, 50, 50, platforms[1]),
        entity.Monster(700, 220, 50, 50, platforms[2]),
        entity.Monster(1000, 170, 50, 50, platforms[3]),
        entity.Monster(1300, 270, 50, 50, platforms[4]),
        entity.Monster(1600, 220, 50, 50, platforms[5]),
        entity.Monster(1900, 170, 50, 50, platforms[6])
    ]

    hearts = [
        entity.LifeHeart(10, 10, 30, 30),
        entity.LifeHeart(50, 10, 30, 30),
        entity.LifeHeart(90, 10, 30, 30)
    ]
    player_lives = len(hearts)
    score = 0
    game_over = False
    goal_reached = False

    font = pygame.font.SysFont(None, 36)

    # Goal 객체 생성
    goal = entity.Goal(background_width - 100, screen_height - 100, 50, 50)

    run_game_loop = True
    while run_game_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game_loop = False

        if game_over or goal_reached:
            continue  # 게임 오버 또는 골 도달 상태에서는 추가 입력을 받지 않음

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.movement = -player.run_speed
        elif keys[pygame.K_RIGHT]:
            player.movement = player.run_speed
        else:
            player.movement = 0

        if keys[pygame.K_SPACE]:
            player.jump()

        collision_result = player.update(platforms, monsters)
        camera.update(player)

        # Move monsters
        for monster in monsters:
            if monster.alive:
                monster.move()

        # Check collisions with monsters and update score/life
        if collision_result == "kill":
            score += 100
        elif collision_result == "hit":
            player_lives -= 1
            if hearts:
                hearts.pop()  # Remove one heart
            if player_lives <= 0:
                game_over = True

        # Check if player reached the goal
        if player.rect.colliderect(goal.rect):
            goal_reached = True

        # Clear the screen
        screen.fill((0, 0, 0))  # Fill with black

        # Draw background
        background_rect = pygame.Rect(0, 0, background_width, background_height)
        screen.blit(game_background, camera.apply(background_rect))

        # Draw platforms
        for platform in platforms:
            screen.blit(platform.image, camera.apply(platform))

        # Draw monsters
        for monster in monsters:
            if monster.alive:
                screen.blit(monster.image, camera.apply(monster))

        # Draw goal
        screen.blit(goal.image, camera.apply(goal))

        # Draw player
        screen.blit(player.image, camera.apply(player))

        # Draw hearts (UI, not affected by camera)
        for i, heart in enumerate(hearts):
            heart.rect.x = 10 + (i * 40)
            screen.blit(heart.image, (heart.rect.x, heart.rect.y))

        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (screen_width - 150, 10))

        pygame.display.flip()
        clock.tick(60)

        if game_over:
            # Show Game Over message
            game_over_font = pygame.font.SysFont(None, 55)
            game_over_text = game_over_font.render(f"Game Over - Score: {score}", True, (255, 0, 0))
            screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(3000)  # Show Game Over message for 3 seconds
            run_game_loop = False

        if goal_reached:
            # Show Goal message
            goal_font = pygame.font.SysFont(None, 55)
            goal_text = goal_font.render("Goal!", True, (0, 255, 0))
            screen.blit(goal_text, (screen_width // 2 - goal_text.get_width() // 2, screen_height // 2 - goal_text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(300)  # Show Goal message for 3 seconds
            run_game_loop = False

    sound_instance.stop_all()  # 모든 사운드 중지
    pygame.quit()
