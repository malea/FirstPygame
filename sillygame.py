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
    
    
    

