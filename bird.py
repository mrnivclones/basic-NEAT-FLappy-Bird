import pygame
import numpy as np
import random
vec = pygame.math.Vector2


class Bird(pygame.sprite.Sprite):
    def __init__(self,pipes, game, W1, W2):
        pygame.sprite.Sprite.__init__(self)
        self.pipes = pipes
        self.game = game
        self.sideLen = 30
        #self.image = pygame.Surface((self.sideLen,self.sideLen))
        #self.image.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        self.image = pygame.image.load("bird_sprite.png")
        self.rect = self.image.get_rect()
        self.rect.center = (130,320)
        self.acc = 1.5
        self.vel = 1
        self.maxVel = 20
        self.old_time = 0
        self.fitness = 0
        self.time = self.time = round(pygame.time.get_ticks()/1000,0)
        self.alive = True
        self.death_time = 0

        #_________________________________________
        #NeuralNet __init__
        self.W1 = W1
        self.W2 = W2

    def recenter(self):
        self.rect.center = (130,320)
        self.acc = 1.5
        self.vel = 1
        self.maxVel = 20

    def update(self):
        self.get_fitness()
        self.position_and_movement()

        #______________________________________________________________
        #NeuralNet decision

        self.distancePipe = self.game.distancePipe
        self.pipeHeight = self.game.random_height_list[0]
        self.X = [self.distancePipe/370,(self.pipeHeight - 250)/150,self.rect.y/720, self.vel/720]
        #self.X = [self.distancePipe/370,(self.pipeHeight-160/2)/400,(self.pipeHeight+160/2-self.sideLen)/400,self.rect.y/720]
        self.decision = round(self.forward(self.X)[0],0)

        if self.decision > 0.5 and self.vel < self.maxVel:
            self.vel = -10

        #______________________________________________________________

        self.collision()

    def position_and_movement(self):
        #reset pos y si hors de l'écran
        if self.rect.y + self.sideLen > 720:
            self.vel = 0
            self.rect.y = 720 - self.sideLen - 1

        if self.rect.y < 0:
            self.rect.y = 0
        #____________________________________

        #gravité
        if self.vel < self.maxVel:
            self.vel += self.acc

        self.rect.y += self.vel

    def get_fitness(self):
        self.time = round(pygame.time.get_ticks()/100,0)
        if self.time > self.old_time and self.alive:
            self.old_time = self.time
            self.fitness += 1


    def collision(self):
        for pipe in self.pipes:
            if (self.rect.x < pipe.rect[0] + pipe.WIDTH) and (self.rect.x + self.sideLen > pipe.rect[0]) and (self.rect.y < pipe.rect[1] + pipe.HEIGHT) and (self.sideLen + self.rect.y > pipe.rect[1]):
                self.vel = 0
                self.acc = 0
                self.rect.x -= 4

    #____________________________________
    #neural net

    def sigmoid(self, s):
        return 1 / (1 + np.exp(-s))
    """
    On va essayer de rajouter un hidden layer.

    def forward(self,X):
        self.z = np.dot(X, self.W)
        return self.sigmoid(self.z)
    """

    def forward(self,X):
        self.z = np.dot(X, self.W1)
        self.z2 = self.sigmoid(self.z)
        self.z3 = np.dot(self.z2, self.W2)
        return self.sigmoid(self.z3)
