import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialise the ship and its starting poition"""
        super().__init__()
        self.screen = ai_game.screen #Assign screen to an attribute ship.
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect() #Acces screens rect attribute
        #using get_rect() and assign to self.screen_rect. Allows ships to be placed
        #in current location on screen

        #Load the ship and get its rect
        self.image = pygame.image.load('images/ship.bmp')#Loads image and attributes it to self.image
        self.rect = self.image.get_rect()

        #Start each new ship at bottom centre of screen
        self.rect.midbottom = self.screen_rect.midbottom #by matching the position of the ship to the midbottom
        # part of the screen if positions the ship at exactly centre bottom of the screen

        #Store a decimal value for the ships horizontal position
        self.x = float(self.rect.x)

        #Movement flag
        self.moving_right = False #We added an attribute for moving right and set it to false
        self.moving_left = False
    
    def update(self): #This will move the ship right if self.moving_right = True
        """Update the ships poistion based on the movement flag."""
        #Updating ships x value not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #Update rect object from self.x
        self.rect.x = self.x

    def blitme(self): #This draws the image to the screenat the position specified
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
    
    def centre_ship(self):
        """Centre the ship on screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
# Pygame is efficient because every game element can be treated as a rectagle