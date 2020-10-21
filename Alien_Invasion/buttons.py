import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        """Initialise button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50 #Set the button dimensions and then colour
        self.button_colour = (0, 255, 0)
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48) #Prepare font attribute for text rendering
        #The none attribute specifies the default font


        #Build buttons rect object and centre it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center #Create a rect button and a set its attribute to center

        #The button message needs to be prepped only once
        self._prep_msg(msg) #This part handles the rendering of the image

    def _prep_msg(self, msg):
        """Turn message into a rendered image and center on text button"""
        self.msg_image = self.font.render(msg, True, self.text_colour, 
        self.button_colour) #Turns text in msg into an image
        self.msg_image_rect = self.msg_image.get_rect() #Centre image around the button
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw blank button and then draw message 
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)