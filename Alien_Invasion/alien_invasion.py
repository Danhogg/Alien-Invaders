import sys #We use toolds in this module to quit the game once we are done
from time import sleep # This is a function in a standard python library
import pygame #This module contains the functionality to create a game

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from buttons import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialise the game, and create game resources"""
        pygame.init() #This initialises background settings that Pygame needs to work properly
        self.settings = Settings()

        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) These settings are for fullscreen mode
        #self.settings.screen_width = self.screen.get_rect().width        but have been commented out as i prefer 
        #self.settings.screen_height = self.screen.get_rect().height       windowed mode

        self.screen = pygame.display.set_mode(
           (self.settings.screen_width, self.settings.screen_height)) #This creates a display window for the game
        pygame.display.set_caption("Alien Invasion") 

        #Create an instance to store game statistics
        #  and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self) #Make an instance of ship
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet() #This is a group for the fleet of aliens
        
        #Make play button
        self.play_button = Button(self, "Play")

        #Set the background colour
        self.bg_colour = (230,230,230) #Colours defined by a mix of RGB this mixes equal of all

    def run_game(self):
        """Start the main loop for the game"""
        while True: #This while loop and code manages screen updates
            self._check_events() #This is the way to call a method within a class, with the method name
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
    
    def _create_fleet(self):
        """Make the fleet of aliens"""
        #Create an alien and find the number of aliens in the row
        #Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
        (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        
    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in a row"""    
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _check_events(self): #We moved the check for the mouse click to quit the game into
                             #its own method
        """Respond to keypresses and mouse events"""
        # Watch for keyboard and mouse events
        for event in pygame.event.get(): #This is an event loop looking for user inputs
            if event.type == pygame.QUIT: #This detects for if the quit button is clicked 
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event) #This links to the _check_keydown_events function
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event) #This links to the _check_keyup_events function
            
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset the game settings
            self.settings.initialise_dynamic_settings()
            #Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            #Hide the mouse cursor
            pygame.mouse.set_visible(False)

        #Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        #Create new fleet and centre the ship
        self._create_fleet()
        self.ship.centre_ship()


    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create new bullet and addit to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
         #Get rid of bullets that have disappeared
            self.bullets.update()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            # print(len(self.bullets)) use this to check the bullets are deleting like they should

            self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        #Check for any bullets that have hit aliens
        # If so get rid of the bullet and alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens: #Check the alien group is empty
            #Destroy existing bullets and create new fleet
            self.bullets.empty() # The empty function removes all sprites from a group
            self._create_fleet()
            self.settings.increase_speed()

            #Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at an edge
        then update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
        # This takes two arguements and looks for if a member of the group has collided with the sprite
        # It loops through the group aliens and returns the first alien found that makes contact
        # with the ship
            self._ship_hit()
        #Look for if aliens have hit the bottom of the screen
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and centre the ship
            self._create_fleet()
            self.ship.centre_ship

            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as a ship hit
                self._ship_hit()
                break

    def _update_screen(self):
        #Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_colour) #This fill() method fills the screen a certain colour
                                             #and it only takes a colour arguement
        self.ship.blitme()#This makes the ship appear on top of the background
        # Make the most recently drawn screen visible 
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #Draw the score information
        self.sb.show_score()

        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip() #This shows the updated screen after the user input


if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()