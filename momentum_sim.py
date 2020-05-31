import pygame
from pygame.locals import *
import time
import math
from random import randint, random, uniform
from pygame import gfxdraw

pygame.mixer.init()
block_sound = pygame.mixer.Sound("block.wav")


def block():
    pygame.mixer.Sound.play(block_sound)
    pygame.mixer.music.stop()


def text_objects(text, font, color=(0, 0, 0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def addVectors(v1, v2):
    # add angle and speed vectors
    x = math.sin(v1[0]) * v1[1] + math.sin(v2[0]) * v2[1]
    y = math.cos(v1[0]) * v1[1] + math.cos(v2[0]) * v2[1]
    return (0.5 * math.pi - math.atan2(y, x), (x**2+y**2)**0.5)


def collide(s1, s2):
    if (s1.x+s1.w >= s2.x and s1.x <= s2.x + s2.w) or (s2.x + s2.w > s1.x and s2.x <= s1.x + s1.w):
        prev = s1.velocity
        s1.velocity = s1.velocity * \
            (s1.mass - s2.mass)/(s1.mass + s2.mass) + \
            2*s2.velocity * s2.mass/(s1.mass + s2.mass)
        s2.velocity = s2.velocity * \
            (s2.mass - s1.mass)/(s1.mass + s2.mass) + \
            2*prev * s1.mass/(s1.mass + s2.mass)
        block()
        return True


class sq:
    def __init__(self, pos, w, v, m, c):
        self.x = pos[0]
        self.y = pos[1]
        self.w = w
        self.mass = m

        self.velocity = v
        self.c = c

    def display(self, screen):
        r = pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.w))
        pygame.draw.rect(screen, self.c, r)

    def move(self, w, h, speed):
        self.x += self.velocity * speed

        if self.x <= 0:
            self.velocity = -1*self.velocity
            block()
            return True


class Game:
    def __init__(self):
        # vars
        self.exit = False
        self.collisions = 0
        self.speed = 1
        self.cnt = 0

    def run(self):
        accepted = False
        print("\n\nMomentum Simulator: 2 blocks with varying velocity and mass colliding with each other and a wall\n\nUp arrow, down arrow, 0 to increase/decrease/reset simulation speed\n\n")
        while not accepted:
            try:
                s1speed = float(input("square 1 velocity (default 0): "))
                s2speed = float(input("square 2 velocity (default -1): "))
                s1mass = float(input("square 1 mass (default 1): "))
                s2mass = float(input("square 2 mass (default 100): "))
                accepted = True
            except:
                print("Invalid")

        pygame.init()
        pygame.display.set_caption("Physics Sim")
        self.width = 1080
        self.height = 360
        self.screen = pygame.display.set_mode((self.width, self.height))

        square1 = sq((300, self.height - 40), 40, s1speed, s1mass, (255, 0, 0))
        square2 = sq((600, self.height - 60), 60, s2speed, s2mass, (0, 0, 255))

        while not self.exit:
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    self.exit = True

            keys = pygame.key.get_pressed()
            if keys[K_UP]:
                self.speed += 1
            if keys[K_DOWN]:
                self.speed = max(1, self.speed - 1)
            if keys[K_0]:
                self.speed = 1

            # refresh screen
            self.screen.fill((200, 200, 200))
            square1.display(self.screen)
            square2.display(self.screen)
            if square1.move(self.width, self.height, self.speed):
                self.collisions += 1
            if square2.move(self.width, self.height, self.speed):
                self.collisions += 1
            if collide(square1, square2):
                self.collisions += 1

            if square1.velocity >= 0 and square2.velocity >= 0 and square1.velocity <= square2.velocity:
                self.cnt += 1
                if self.cnt == 50:
                    self.exit = True
                    print("\n\nFinished, final collisions: " +
                          str(self.collisions) + "\n\n")

            largeText = pygame.font.Font('freesansbold.ttf', 10)
            TextSurf, TextRect = text_objects(
                "RED VELOCITY: %0.2f" % (square1.velocity), largeText, (255, 0, 0))
            TextRect.topleft = (10, 10)
            self.screen.blit(TextSurf, TextRect)

            largeText = pygame.font.Font('freesansbold.ttf', 10)
            TextSurf, TextRect = text_objects(
                "RED MASS: "+str(square1.mass), largeText, (255, 0, 0))
            TextRect.topleft = (10, 25)
            self.screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = text_objects(
                "BLUE VELOCITY: %0.2f" % (square2.velocity), largeText, (0, 0, 255))
            TextRect.topleft = (10, 50)
            self.screen.blit(TextSurf, TextRect)

            largeText = pygame.font.Font('freesansbold.ttf', 10)
            TextSurf, TextRect = text_objects(
                "BLUE MASS: "+str(square2.mass), largeText, (0, 0, 255))
            TextRect.topleft = (10, 65)
            self.screen.blit(TextSurf, TextRect)

            largeText = pygame.font.Font('freesansbold.ttf', 10)
            TextSurf, TextRect = text_objects(
                "TOTAL MOMENTUM: %0.2f" % (square1.mass * square1.velocity + square2.mass * square2.velocity), largeText)
            TextRect.topleft = (10, 100)
            self.screen.blit(TextSurf, TextRect)

            largeText = pygame.font.Font('freesansbold.ttf', 10)
            TextSurf, TextRect = text_objects(
                "TOTAL KE: %0.2f" % (0.5*square1.mass * square1.velocity**2 + 0.5*square2.mass * square2.velocity**2), largeText)
            TextRect.topleft = (10, 115)
            self.screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = text_objects(
                "COLLISIONS: "+str(self.collisions), largeText)
            TextRect.topleft = (10, 140)
            self.screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = text_objects(
                "SPEED: "+str(self.speed), largeText)
            TextRect.topleft = (10, 165)
            self.screen.blit(TextSurf, TextRect)

            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
