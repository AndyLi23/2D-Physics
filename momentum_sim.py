import pygame
from pygame.locals import *
import time
import math
from random import randint, random, uniform
from pygame import gfxdraw


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
        r = pygame.Rect(self.x, self.y, self.w, self.w)
        pygame.draw.rect(screen, self.c, r)

    def move(self, w, h):
        self.x += self.velocity

        if self.x <= 0:
            self.velocity = -1*self.velocity
            return True


class Game:
    def __init__(self):
        # initialize
        pygame.init()
        pygame.display.set_caption("Physics Sim")
        self.width = 720
        self.height = 360
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.exit = False
        self.collisions = 0

    def run(self):

        square1 = sq((300, self.height - 40), 40, 0, 1, (255, 0, 0))
        square2 = sq((600, self.height - 60), 60, -2, 100, (0, 0, 255))

        while not self.exit:
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    self.exit = True

            # refresh screen
            self.screen.fill((200, 200, 200))
            square1.display(self.screen)
            square2.display(self.screen)
            if square1.move(self.width, self.height):
                self.collisions += 1
            if square2.move(self.width, self.height):
                self.collisions += 1
            if collide(square1, square2):
                self.collisions += 1

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
                "TOTAL MOMENTUM: %0.2f" % (square1.mass * abs(square1.velocity) + square2.mass * abs(square2.velocity)), largeText)
            TextRect.topleft = (10, 100)
            self.screen.blit(TextSurf, TextRect)

            largeText = pygame.font.Font('freesansbold.ttf', 10)
            TextSurf, TextRect = text_objects(
                "TOTAL KE: %0.2f" % (0.5*square1.mass * abs(square1.velocity)**2 + 0.5*square2.mass * abs(square2.velocity)**2), largeText)
            TextRect.topleft = (10, 115)
            self.screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = text_objects(
                "COLLISIONS: "+str(self.collisions), largeText)
            TextRect.topleft = (10, 140)
            self.screen.blit(TextSurf, TextRect)

            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
