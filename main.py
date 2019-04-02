# general constants
SCREEN_WIDTH = 420
SCREEN_HEIGHT = 720
FRAME_RATE = 200
SPACE_BET_PIPES = 180 #120
BIRD_SELECTED = 140 #toujours une population paire
POPULATION_SIZE = 300
NN_INPUT = 4
NN_HIDDEN = 5
NN_OUTPUT = 1

import sys
import pygame
from pygame.locals import *
from bird import *
from pipe import *
import random


class Game():
    def __init__(self):
        #init sprite group
        self.bird_sprites = pygame.sprite.Group()
        self.pipe_sprites = pygame.sprite.Group()

        #init var
        self.score = 0
        self.pipeIndex = 0 #pour la distance a la prochaine pipe
        self.random_height_list = []
        self.dead_bird_pop = []
        self.nextGen_birds = []
        self.dead_bird_nb = 0
        self.fitness_best_score = -1
        self.previousBestScore = 0
        self.generation = 0
        self.bestScore = 0

        #init first pipe
        self.pipes = []
        #on creer une list single_pipe pour les data pcq sinon ca supprime deux trucs au lieu  d'un a cause des deux pipe_sprites
        self.single_pipes = []
        self.spawn_pipes(400, random.randint(250,400))


        #init bird
        self.birds = []
        self.spawn_birds()
        self.next_population_weight = []



        self.scoreFont = pygame.font.SysFont("monospace", 40)
        self.smallFont = pygame.font.SysFont("monospace", 16)

    def spawn_birds(self):
        """
        if len(self.nextGen_birds) == 0 or self.previousBestScore < 2:
            for nb_bird in range(POPULATION_SIZE):
                player = Bird(self.pipes, self, np.random.randn(NN_INPUT, NN_HIDDEN),  np.random.randn(NN_HIDDEN, NN_OUTPUT))
                self.birds.append(player)
                self.bird_sprites.add(player)
        """

        if self.previousBestScore > 1:
            #on fait spawn les oiseaux qu'on selectionne
            for bird in self.nextGen_birds:
                bird.alive = True
                self.birds.append(bird)
                self.bird_sprites.add(bird)

        if self.generation > 0:
                #on fait spawn l'ancian best oiseau
                #je devrais sauvegarder les weight du best bird et le faire
                #pcq pour l'instant ça bug.
                bestBird = Bird(self.pipes, self, self.overallBestBirdW1, self.overallBestBirdW2)
                self.birds.append(bestBird)
                self.bird_sprites.add(bestBird)
                bestBird.image = pygame.image.load("win_bird_sprite.png")

        while int(len(self.birds)) < POPULATION_SIZE:
            player = Bird(self.pipes, self, np.random.randn(NN_INPUT, NN_HIDDEN),  np.random.randn(NN_HIDDEN, NN_OUTPUT))
            self.birds.append(player)
            self.bird_sprites.add(player)


        #reset bird setting pour ceux qui sont cloné
        #ils sont bougés un peu quand ils meurent et ça crée des bugs
        for bird in self.birds:
            bird.recenter()

    def restart(self):
        self.generation+=1
        if self.bestScore < self.score:
            self.bestScore = self.score

        del(self.pipes[:])
        del(self.single_pipes[:])
        del(self.random_height_list[:])
        self.pipe_sprites.empty()
        self.previousBestScore = self.score
        self.score = 0
        self.spawn_pipes(500, random.randint(250,400))
        self.pipeIndex = 0

        self.dead_bird_nb = 0
        del(self.birds[:])
        del(self.dead_bird_pop[:])
        self.bird_sprites.empty()
        self.spawn_birds()
        del(self.nextGen_birds[:])



    def mutate(self):
        """
        Dans cette méthode de mutation, on prend le meilleur
        bird. On prend ses weights et on additionne à ceux-ci
        des nouveaux weights aléatoire.
        """
        for i in range(BIRD_SELECTED):
            mutationValuesWeights1 = np.random.rand(NN_INPUT, NN_HIDDEN) / random.randint(1,20) #nouveau random weight que l'on va additionner
            mutationValuesWeights2 = np.random.rand(NN_HIDDEN, NN_OUTPUT) / random.randint(1,20)
            newBirdWeight1 = self.nextGen_birds[0].W1 + mutationValuesWeights1
            newBirdWeight2 = self.nextGen_birds[0].W2 + mutationValuesWeights2
            self.nextGen_birds.append(Bird(self.pipes,self,newBirdWeight1, newBirdWeight2))

    """
    #### Version de mutate sans le hidden layer
    def mutate(self):
        self.nb_couple = len(self.nextGen_birds)
        for bird_index in range(0,self.nb_couple,2):
            self.couple = [self.nextGen_birds[bird_index].W, self.nextGen_birds[bird_index+1].W]
            self.new_born_weight = np.mean(self.couple,axis=0)
            self.nextGen_birds.append(Bird(self.pipes,self,self.new_born_weight))

    def mutate(self):
        self.nb_couple = len(self.nextGen_birds)
        for bird_index in range(0,self.nb_couple,2):
            self.couple1 = [self.nextGen_birds[bird_index].W1, self.nextGen_birds[bird_index+1].W1]
            self.couple2 = [self.nextGen_birds[bird_index].W2, self.nextGen_birds[bird_index+1].W2]
            self.new_born_weight1 = np.mean(self.couple1,axis=0)
            self.new_born_weight2 = np.mean(self.couple2,axis=0)
            self.nextGen_birds.append(Bird(self.pipes,self,self.new_born_weight1, self.new_born_weight2))
    """

    def spawn_pipes(self,x,y):
        self.random_height_list.append(y)

        self.pipe_up = Pipe()
        self.pipe_down = Pipe()

        self.pipes.append(self.pipe_up)
        self.pipes.append(self.pipe_down)
        self.pipe_sprites.add(self.pipe_up)
        self.pipe_sprites.add(self.pipe_down)

        self.single_pipes.append(self.pipe_up)

        self.pipe_up.x = x
        self.pipe_up.y = y - SPACE_BET_PIPES/2 - self.pipe_up.HEIGHT

        self.pipe_down.x = x
        self.pipe_down.y = y + SPACE_BET_PIPES/2

        self.last_pipe = self.pipe_up

    """
    def selection(self):
        i=0
        self.fitness_best_score  = -1
        for bird in self.dead_bird_pop:
            if self.fitness_best_score == -1:
                self.fitness_best_score = bird.fitness
                self.best_bird = bird
                bird_index = i
            if bird.fitness >= self.fitness_best_score:
                self.fitness_best_score = bird.fitness
                self.best_bird = bird
                bird_index = i
            i+=1

        self.nextGen_birds.append(self.best_bird)
        """


    def selection(self):
        """
        Quand les birds meurent on les met dans la "dead_bird_pop" puis on les
        select et les met dans "nextGen_birds"

        On prend aussi l'ancien meilleur oiseau que l'on fait respawn.
        """
        for nb_bird_to_reproduce in range(BIRD_SELECTED):
            i = 0
            self.fitness_best_score  = -1
            for bird in self.dead_bird_pop:
                if self.fitness_best_score == -1:
                    self.fitness_best_score = bird.fitness
                    self.best_bird = bird
                    bird_index = i
                if bird.fitness >= self.fitness_best_score:
                    self.fitness_best_score = bird.fitness
                    self.best_bird = bird
                    bird_index = i
                i+=1

            self.nextGen_birds.append(self.best_bird)
            self.dead_bird_pop.pop(bird_index) #on retire le meilleur bird pour pas le selec plusieurs fois

        #select old best bird pour le faire respawn
        self.fitness_best_score  = -1
        for bird in self.nextGen_birds:
            if self.fitness_best_score < bird.fitness:
                self.overallBestBirdW1 = bird.W1
                self.overallBestBirdW2 = bird.W2
                self.fitness_best_score = bird.fitness



    def loop(self, screen):
        clock = pygame.time.Clock()

        while True:
            delta_t = clock.tick( FRAME_RATE )

            # handle input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return # closing the window, end of the game loop
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
                    if event.key == pygame.K_r:
                        self.restart()

            # render game screen
            screen.fill( (255, 255, 255) ) # black background
            #background image
            """
            bg = pygame.image.load("background.png")
            screen.blit(bg, (0, 0))
            """

            #update des pipes
            #si une pipe dépasse une certaine limite on en fait spawn une autre
            if self.last_pipe.x < 380:
                self.random_height = random.randint(250,400)
                self.spawn_pipes(500, self.random_height)

            #si une pipe sort de l'ecran on la su
            for pipe in self.pipes:
                if pipe.x < -100:
                    self.pipes.remove(pipe)

            #on update la height list pipe pour les data du nn
            for pipe in self.single_pipes:
                if pipe.x == 72:
                    del(self.random_height_list[0])
                    self.pipeIndex+=1

            #distance par rapport a la prochaine pipe
            self.distancePipe = self.single_pipes[self.pipeIndex].x - 75

            #_________________________________________________________



            #update
            for bird in self.birds:
                bird.update()


            for pipe in self.pipes:
                pipe.update()
                #check score
                if pipe.x == 128:
                    self.score += 0.5


            for bird in self.birds:
                if bird.rect.x < 100:
                    bird.alive = False
                    self.dead_bird_pop.append(bird)
                    self.birds.remove(bird)
                    self.bird_sprites.remove(bird)

            if len(self.birds) ==  0:
                self.selection()
                self.mutate()
                self.restart()


            #draw
            self.bird_sprites.draw(screen)
            self.pipe_sprites.draw(screen)

            # render text
            #score
            self.score_label = self.scoreFont.render(str(self.score), 1, (255,0,0))
            screen.blit(self.score_label, (SCREEN_WIDTH/2 - 10, 100))
            #pipe height
            self.height_label = self.smallFont.render("Pipe height: "+str(self.random_height_list[0]), 1 , (255,0,0))
            screen.blit(self.height_label, (10,10))
            #pipe distance
            self.distance_label = self.smallFont.render("Pipe distance: "+str(self.distancePipe), 1 , (255,0,0))
            screen.blit(self.distance_label, (10,25))
            #nb bird vivant
            self.vivant_label = self.smallFont.render("Vivant: "+ str(len(self.birds)), 1 , (255,0,0))
            screen.blit(self.vivant_label, (10,40))
            #generation
            self.generation_label = self.smallFont.render("Generation: "+ str(self.generation), 1 , (255,0,0))
            screen.blit(self.generation_label, (10,55))
            #best score
            self.bestScore_label = self.smallFont.render("Best Score: "+ str(self.bestScore), 1 , (255,0,0))
            screen.blit(self.bestScore_label, (10,70))


            # update display
            pygame.display.update()
            # or pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
    pygame.display.set_caption( 'NEAT Flappy Bird' )
    #pygame.mouse.set_visible( False )

    game = Game()
    game.loop( screen )
    pygame.quit()

if __name__ == '__main__':
    main()
