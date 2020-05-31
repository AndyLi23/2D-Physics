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


def find(particles, x, y):
    # find if mouse clicked on particle
    for p in particles:
        if ((p.x-x)**2 + (p.y-y)**2)**0.5 <= p.size:
            return p


# constants
gravity = (math.pi, 0.1)
drag = 0.999
elasticity = 0.8
mass_of_air = 0.2


class Particle:
    def __init__(self, pos, size, speed, angle, mass, color):
        # x,y coordinates
        self.x = pos[0]
        self.y = pos[1]
        #size, color
        self.size = size
        self.color = color
        #speed, angle, mass
        self.speed = speed
        self.angle = angle
        self.mass = mass
        self.drag = (self.mass/(self.mass + mass_of_air)) ** self.size

    def display(self, screen):
        # display on screen
        gfxdraw.filled_circle(screen, int(self.x), int(
            self.y), int(self.size), self.color)

    def move(self):
        # move according to speed and angle
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        # move according to gravity
        self.angle, self.speed = addVectors((self.angle, self.speed), gravity)
        # add drag
        self.speed *= self.drag

    def bounce(self, width, height):
        if self.x <= self.size:  # left
            self.x = 2 * self.size - self.x
            self.angle = -1 * self.angle
            self.speed *= elasticity
        elif self.x >= width-self.size:  # right
            self.x = 2 * (width - self.size) - self.x
            self.angle = -1 * self.angle
            self.speed *= elasticity
        if self.y <= self.size:  # top
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity
        elif self.y >= height-self.size:  # bottom
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity
            if self.speed < 0.9:
                self.speed = 0  # clamp down to prevent infinite bouncing

    def collide(self, p2):
        dx = self.x - p2.x
        dy = self.y - p2.y

        distance = (dx**2 + dy**2)**0.5
        if distance < self.size + p2.size:
            angle = math.atan2(dy, dx) + 0.5 * math.pi
            total_mass = self.mass + p2.mass
            self.angle, self.speed = addVectors(
                (self.angle, self.speed*(self.mass-p2.mass)/total_mass), (angle, 2*p2.speed*p2.mass/total_mass))
            p2.angle, p2.speed = addVectors(
                (p2.angle, p2.speed*(p2.mass-self.mass)/total_mass), (angle+math.pi, 2*self.speed*self.mass/total_mass))
            self.speed *= elasticity
            p2.speed *= elasticity

            overlap = 0.5 * (self.size + p2.size - distance + 1)
            self.x += math.sin(angle) * overlap
            self.y -= math.cos(angle) * overlap
            p2.x -= math.sin(angle) * overlap
            p2.y += math.cos(angle) * overlap


class Game:
    def __init__(self):
        # initialize
        pygame.init()
        pygame.display.set_caption("Physics Sim")
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.exit = False
        self.selected_particle = None
        self.dx, self.dy = 0, 0
        self.prevcolor = None

    def run(self):
        # particles
        circles = []
        for i in range(10):
            density = randint(1, 20)
            size = randint(20, 40)
            circles.append(
                Particle((randint(0, self.width), randint(0, self.height)), randint(20, 40), random()*30, uniform(0, math.pi*2), size ** 2 * density, (density * 5, density * 5, density * 5)))

        while not self.exit:
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    pygame.quit()

                # if clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    temp = find(
                        circles, mouseX, mouseY)
                    # if clicked particle

                    if self.selected_particle == temp:
                        if self.selected_particle:
                            self.selected_particle.color = self.prevcolor
                        self.selected_particle = None
                        self.dx, self.dy = 0, 0
                    elif temp:
                        if self.selected_particle:
                            self.selected_particle.color = self.prevcolor
                        self.selected_particle = temp
                        self.prevcolor = self.selected_particle.color
                        self.selected_particle.color = (255, 0, 0)
                    else:
                        if self.selected_particle:
                            self.selected_particle.color = self.prevcolor
                        self.selected_particle = None
                        self.dx, self.dy = 0, 0

                keys = pygame.key.get_pressed()
                if keys[K_SPACE]:
                    for i in circles:
                        i.speed = i.speed + random()*30
                if keys[K_a]:
                    for i in circles:
                        i.speed = i.speed + random()*30
                        i.angle = uniform(0, math.pi*2)

            # refresh screen
            self.screen.fill((200, 200, 200))

            # update and display particles
            for ind, i in enumerate(circles):
                if i != self.selected_particle:
                    i.move()
                    i.bounce(self.width, self.height)
                    for i2 in circles[ind+1:]:
                        i.collide(i2)
                else:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    self.dx = mouseX - i.x
                    self.dy = mouseY - i.y
                    i.angle = math.atan2(self.dy, self.dx) + 0.5*math.pi
                    i.speed = math.hypot(self.dx, self.dy) * 0.1
                    i.move()
                    i.bounce(self.width, self.height)

                i.display(self.screen)

            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
