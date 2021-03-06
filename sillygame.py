import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

#LOAD IMAGE FUNCTION
def load_image(name, colorkey=None):
    #create full pathname to the file (assume resource in "data" subdir)
    fullname = os.path.join('data', name) 
    #load image using pygame load. wrapped in try/except block, so if problem
    #exit gracefully
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    #makes a new copy of a Surface and converts its color format and depth to
    #match the display
    image = image.convert()
    #set colorkey for image
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

#LOAD SOUND FUNCTION   
def load_sound(name):
    class NoneSound:
        #check pygame.mixer running properly
        def play(self): pass
    #if pygame.mixer not running properly, make Dummy play method
    if not pygame.mixer:
        return NoneSound()
    #full path to the sound image, and load the sound file
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound
    
class Fist(pygame.sprite.Sprite):
    #moves a clenched fist on the screen, following the mouse
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('fist.jpg', -1)
        self.punching = 0

    def update(self):
        #move the fist based on the mouse position
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        #returns true if the fist collides with the target"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        #called to pull the fist back"
        self.punching = 0

class Clown(pygame.sprite.Sprite):
    #move clown around screen
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('clown.jpg', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        if self.dizzy: #if punched
            self._spin()
        else: #if not punched
            self._walk()

    def _walk(self):
        #move clown around and turn if at edge
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
	        if self.rect.left < self.area.left or \
	        self.rect.right > self.area.right:
                    self.move = -self.move
                    newpos = self.rect.move((self.move, 0))
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.rect = newpos

    def _spin(self):
        #spin the clown
        center = self.rect.center
        self.dizzy += 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        #this makes the clow spin
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image

def main():
  
    #initialize stuff         
    pygame.init()
    screen = pygame.display.set_mode((400,400))
    pygame.display.set_caption('Clowning Around')
    pygame.mouse.set_visible(0)

    #create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250,250,250))

    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Punch the Clown...Clowns are EVIL!", 1, (10,10,10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)
    
    #create objects
    whiff_sound = load_sound('creepysong.mp3')
    punch_sound = load_sound('punch.mp3')
    clown = Clown()
    fist = Fist()
    allsprites = pygame.sprite.RenderPlain((fist, clown))
    clock = pygame.time.Clock()

    #game runs on infinite loop
    while 1:
        #whiff_sound.play()
        clock.tick(60)

        #simple working event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(clown):
                    punch_sound.play() #punch
                    clown.punched()
                else:
                    whiff_sound.play() #miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        #update sprites
        allsprites.update()

        #draw scene
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()
        
#Game Over
    
#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
