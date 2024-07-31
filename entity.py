import pygame
import random

class Platform:
    def __init__(self, x, y, width, height):
        self.image = pygame.image.load("C:/Users/USER/Desktop/study/game/image/platform.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Monster:
    def __init__(self, x, y, width, height, platform):
        self.image = pygame.image.load("C:/Users/USER/Desktop/study/game/image/monster.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction = random.choice([-1, 1])  # 랜덤한 초기 방향
        self.alive = True
        self.platform = platform
        self.rect.bottom = platform.rect.top  # 몬스터를 플랫폼 위에 위치시킴

    def move(self):
        if not self.alive:
            return

        # 이동
        self.rect.x += self.speed * self.direction

        # 플랫폼 끝에 도달하면 방향 전환
        if self.direction == -1 and self.rect.left <= self.platform.rect.left:
            self.rect.left = self.platform.rect.left
            self.direction = 1
        elif self.direction == 1 and self.rect.right >= self.platform.rect.right:
            self.rect.right = self.platform.rect.right
            self.direction = -1

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def kill(self):
        self.alive = False


class LifeHeart:
    def __init__(self, x, y, width, height):
        self.image = pygame.image.load("C:/Users/USER/Desktop/study/game/image/heart.jpg")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Goal:
    def __init__(self, x, y, width, height):
        self.image = pygame.image.load("C:/Users/USER/Desktop/study/game/image/goal.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))