import pygame
import neat
import time 
import os
import random
from bird import Bird
from score import Score
from base import Base
from pipe import Pipe

pygame.font.init()
WIN_WIDTH = 500
WIN_HEIGHT = 800


BG_IMG = pygame.transform.scale2x( pygame.image.load(os.path.join("imgs","bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

def draw_window(win, bird, pipes, base, score):
    
    win.blit(BG_IMG, (0,0))
    
    for pipe in pipes:
        pipe.draw(win)        

    base.draw(win)
   
    bird.draw(win)
    text = STAT_FONT.render("Score: "+str(score.get_score()),1,(255,255,255))
    # win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    win.blit(text, (10, 10))
    pygame.display.update()

def reset_game(bird, pipes, score):
    bird.reset()
    score.reset_score()
    pipes = [Pipe(600)]

def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    score = Score()

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run  = True
    started = False
    
    while run:
        
        clock.tick(30) # sets 30 frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                bird.jump()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not started:
                        started = True

        base.move()
        if started:
            bird.move()
            
            add_pipe = False
            rem = []
            for pipe in pipes:

                if bird.y + bird.img.get_height() >= 730 or bird.y < 0: # if bird hits floor
                    pygame.quit()
                    quit()

                if pipe.collide(bird):
                    # pygame.quit()
                    # quit()
                    reset_game(bird, pipes, score)
                
                    started = False
                    pass

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
                
                pipe.move()


            if add_pipe:
                score.update_score()
                pipes.append(pipe(700))

            for r in rem:
                pipes.remove(r)   
            

        draw_window(win, bird, pipes, base, score)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()