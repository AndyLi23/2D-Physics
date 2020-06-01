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
FRICTION = 0.96
FRICTION2 = 0.99


class Particle:
    def __init__(self, pos, size, speed, angle, color):
        # x,y coordinates
        self.x = pos[0]
        self.y = pos[1]
        # size, color
        self.size = size
        self.color = color
        # speed, angle, mass
        self.speed = speed
        self.angle = angle
        self.incontact = False

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
            self.speed *= FRICTION


class Barrier:
    def __init__(self, topleft, w, h, angle):
        self.topleft = topleft
        self.w = w
        self.h = h
        self.angle = angle

    def display(self, screen):
        pygame.draw.line(screen, (0, 0, 0), self.topleft, (self.topleft[0] + self.w*math.cos(
            self.angle), self.topleft[1] + self.w * math.sin(self.angle)), self.h)

    def collide(self, particle):
        m = min(((particle.x - self.topleft[0] - i*math.cos(
                self.angle))**2 + (particle.y - self.topleft[1] - i*math.sin(self.angle)) ** 2)**0.5 for i in range(particle.size + self.h//2, self.w+1-particle.size - self.h//2))
        if m <= particle.size + self.h/2:
            if not self.incontact:
                self.incontact = True
                if not self.angle == 0:
                    particle.speed = particle.speed * math.sin(abs(self.angle))
            if self.angle < 0:
                if particle.x <= particle.size:
                    particle.speed = 0
                particle.angle = 3*math.pi/2 + self.angle
                particle.speed *= 0.99
            elif self.angle > 0:
                if particle.x >= 1000-particle.size:
                    particle.speed = 0
                particle.angle = math.pi/2 + self.angle
                particle.speed *= 0.99
            else:
                particle.y = self.topleft[1] - (particle.size + self.h/2)
                particle.speed *= FRICTION
        else:
            self.incontact = False


class Game:
    def __init__(self):
        # initialize
        pygame.init()
        pygame.display.set_caption("Physics Sim")
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.exit = False
        self.selected = False

    def run(self):

        marble = Particle((20, 20), 20, 0, 0, (255, 0, 0))
        barriers = []

        barrier = Barrier((200, 500), 500, 20, -math.pi/6)
        barrier2 = Barrier((-10, 200), 300, 20, math.pi/6)
        barrier3 = Barrier((0, 600), 500, 20, 0)

        barriers.append(barrier)
        barriers.append(barrier2)
        barriers.append(barrier3)

        while not self.exit:
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if ((marble.x-x)**2 + (marble.y-y)**2)**0.5 <= marble.size:
                        if not self.selected:
                            self.selected = True
                            marble.color = (0, 0, 255)
                        else:
                            self.selected = False
                            marble.color = (255, 0, 0)

            if self.selected:
                x, y = pygame.mouse.get_pos()
                marble.x = x
                marble.y = y
                marble.speed = 0
                marble.angle = 0

            keys = pygame.key.get_pressed()

            # refresh screen
            self.screen.fill((200, 200, 200))

            # update and display particles

            if not self.selected:
                marble.move(self.width, self.height, keys)
                for barrier in barriers:
                    barrier.collide(marble)

            marble.display(self.screen)
            for barrier in barriers:
                barrier.display(self.screen)

            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
