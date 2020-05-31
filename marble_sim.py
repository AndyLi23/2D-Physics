import pygame
from pygame.locals import *
import time
import math
from random import randint, random, uniform
from pygame import gfxdraw


def addVectors(v1, v2):
    # add angle and speed vectors
    x = math.sin(v1[0]) * v1[1] + math.sin(v2[0]) * v2[1]
    y = math.cos(v1[0]) * v1[1] + math.cos(v2[0]) * v2[1]
    return (0.5 * math.pi - math.atan2(y, x), (x**2+y**2)**0.5)


gravity = (math.pi, 0.2)
drag = 0.999
elasticity = 0.8
mass_of_air = 0.2


class Particle:
    def __init__(self, pos, size, speed, angle, color):
        # x,y coordinates
        self.x = pos[0]
        self.y = pos[1]
        #size, color
        self.size = size
        self.color = color
        #speed, angle, mass
        self.speed = speed
        self.angle = angle

    def display(self, screen):
        # display on screen
        gfxdraw.filled_circle(screen, int(self.x), int(
            self.y), int(self.size), self.color)

    def move(self, w, h, keys):
        # move according to speed and angle
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        # move according to gravity
        self.angle, self.speed = addVectors((self.angle, self.speed), gravity)
        # add drag
        self.speed *= drag

        if self.x <= self.size:
            self.x = self.size
        elif self.x >= w-self.size:
            self.x = w-self.size
        if self.y <= self.size:
            self.y = self.size
        elif self.y >= h-self.size:
            self.y = h-self.size
            if not (keys[K_LEFT] or keys[K_RIGHT]):
                self.speed *= 0.94
            else:
                self.speed *= 0.98

        if keys[K_LEFT]:
            if self.touching(w, h):
                self.angle, self.speed = addVectors(
                    (self.angle, self.speed), (1.5*math.pi, 0.1))

        if keys[K_RIGHT]:
            if self.touching(w, h):
                self.angle, self.speed = addVectors(
                    (self.angle, self.speed), (0.5*math.pi, 0.1))

        if keys[K_UP]:
            if self.touching(w, h):
                if keys[K_RIGHT]:
                    self.angle = 0.15 * math.pi
                elif keys[K_LEFT]:
                    self.angle = -0.15 * math.pi
                else:
                    self.angle = 0
                self.speed = 6

    def touching(self, w, h):
        if self.y >= h-self.size:
            return True
        return False


class Game:
    def __init__(self):
        # initialize
        pygame.init()
        pygame.display.set_caption("Physics Sim")
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.exit = False

    def run(self):

        marble = Particle((20, 20), 20, 0, 0, (255, 0, 0))

        while not self.exit:
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    pygame.quit()

            keys = pygame.key.get_pressed()

            # refresh screen
            self.screen.fill((200, 200, 200))

            # update and display particles

            marble.move(self.width, self.height, keys)
            marble.display(self.screen)

            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
