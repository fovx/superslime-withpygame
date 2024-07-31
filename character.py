import pygame
from sound import Sound

GRAVITY = 0.5
PLAYER_RUN_SPEED = 5
PLAYER_JUMP_SPEED = 10
PLAYER_MASS = 1

class Character:
    def __init__(self, screen_height, sound):
        self.original_image = pygame.image.load("C:/Users/USER/Desktop/study/game/image/slime_1.png")
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.movement = 0
        self.direction = 1
        self.run_speed = PLAYER_RUN_SPEED
        self.jump_speed = 0
        self.vertical_speed = 0
        self.rect.x = 100
        self.rect.y = screen_height - self.image.get_height()
        self.screen_height = screen_height
        self.on_ground = True
        self.invincible = False
        self.invincible_start_time = 0
        self.sound = sound

    def jump(self):
        if self.on_ground:
            self.vertical_speed = -PLAYER_JUMP_SPEED
            self.on_ground = False
            self.sound.play_jump()

    def apply_gravity(self):
        if not self.on_ground:
            self.vertical_speed += GRAVITY
            self.rect.y += self.vertical_speed

    def move(self):
        self.rect.x += self.movement
        if self.movement != 0:
            self.direction = 1 if self.movement > 0 else -1
            self.flip_image()

    def flip_image(self):
        if self.direction == -1:
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.image = self.original_image.copy()

    def check_collision_with_platforms(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vertical_speed > 0:  # 떨어짐 
                    self.rect.bottom = platform.rect.top
                    self.vertical_speed = 0
                    self.on_ground = True
                elif self.vertical_speed < 0:  # Jump
                    self.rect.top = platform.rect.bottom
                    self.vertical_speed = 0

    def update(self, platforms, monsters):
        self.apply_gravity()
        self.move()
        self.check_collision_with_platforms(platforms)
        return self.check_collision_with_monsters(monsters)

    def check_collision_with_monsters(self, monsters):
        for monster in monsters:
            if monster.alive and self.rect.colliderect(monster.rect):
                if self.rect.bottom <= monster.rect.top + 10 and self.vertical_speed > 0:
                    # 몬스터 위를 밟음
                    monster.kill()
                    self.vertical_speed = -PLAYER_JUMP_SPEED / 2 # 반동을 줘야함. 몬스터를 밟을 때 잠깐의 멈춤이 발생해야 판정이 잘 됨
                    return "kill"  # 몬스터 처치
                elif not self.invincible:
                    # 몬스터와 충돌
                    self.invincible = True
                    self.invincible_start_time = pygame.time.get_ticks()  
                    return "hit"  # 플레이어가 피격됨
        return "none"  # 충돌 없음

    def draw(self, screen):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if (current_time // 200) % 2 == 0:  # 깜빡임 효과를 더 빠르게
                return  # Skip drawing to create a blink effect
        screen.blit(self.image, self.rect)

class Camera:
    def __init__(self, width, height, world_width, world_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height

    def apply(self, entity):
        if isinstance(entity, pygame.Rect):
            return entity.move(self.camera.topleft)
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # 카메라가 맵 밖으로 나가지 않도록 제한
        x = min(0, x)  # 왼쪽 끝
        y = min(0, y)  # 위쪽 끝
        x = max(-(self.world_width - self.width), x)  # 오른쪽 끝
        y = max(-(self.world_height - self.height), y)  # 아래쪽 끝

        self.camera = pygame.Rect(x, y, self.width, self.height)