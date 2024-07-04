import pygame 
import neat
import time 
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

# load the 3 different bird images
BIRD_IMGS = [pygame.transform.scale2x( pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x( pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x( pygame.image.load(os.path.join("imgs","bird3.png")))] # make images double the size they usually are
PIPE_IMG = pygame.transform.scale2x( pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x( pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x( pygame.image.load(os.path.join("imgs","bg.png")))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5 # how long we show each bird animation

    def __init__(self, x,y):
        self.x =x # starting posistion of bird
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0 # velocity
        self.height = self.y
        self.img_count = 0 # to keep track of which bird image is being shown, for animation
        self.img = self.IMGS[0]


    def jump(self):
        self.vel = -10.5 # 0,0 is top left corner, therefore to go up one needs negative Y direction
        self.tick_count = 0
        self.height = self.y  # where the bird is jumping from

    # called every single frame to move bird
    def move(self):
        self.tick_count += 1

        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2 # tick count represents time, how many seconds have been moving for. Gets set to 0 everytime jump() is called
        # disp = Vi + 1/2 a*t^2, the 1.5 means accelerating down by 1.5 because the positive is down and negative is up, tick count is time

        if displacement >= 16: # terminal velocity, i.e if moving down or up by 16 pixels then set d to be 16 pixels
            displacement = 16

        if displacement <0: #fine tunes jump 
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0  or self.y < self.height +50: # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        
        else: # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY



    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4+1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft= (self.x,self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False # for collision purposes
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        if t_point or b_point:
            return True
        
        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -=self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
        
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        

def draw_window(win, bird, pipes, base):
    
    win.blit(BG_IMG, (0,0))
    
    for pipe in pipes:
        pipe.draw(win)        

    base.draw(win)
   
    bird.draw(win)
   
    pygame.display.update()

def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    score = 0

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run  = True

    while run:
        clock.tick(30) # sets 30 frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                bird.jump()

        bird.move()
        base.move()
        add_pipe = False
        rem = []
        for pipe in pipes:

            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                pygame.quit()
                quit()

            if pipe.collide(bird):
                pygame.quit()
                quit()
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            
            pipe.move()


        if add_pipe:
            score +=1 
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)   
        

        draw_window(win, bird, pipes, base)
    pygame.quit()
    quit()

main()