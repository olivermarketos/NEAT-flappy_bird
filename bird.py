import pygame
import os

class Bird:
    IMGS = [pygame.transform.scale2x( pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x( pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x( pygame.image.load(os.path.join("imgs","bird3.png")))] # make images double the size they usually are

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
    
    def reset(self):
        self.x = 230
        self.y = 350
