class Settings:
    """A class to store all settings for Alien Invasion"""
    def __init__(self):
        """Initialise the games static settings"""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230,230,230)

        #Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 10

        #Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        #How quickly the game speeds up
        self.speedup_scale = 1.1

        #How quicklythe point values increase
        self.score_scale = 1.5
        
        self.initialise_dynamic_settings()
        

    def initialise_dynamic_settings(self):
        """Initialise settings that change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        #Scoring
        self.alien_points = 50

        #Fleet_direction of 1 right; -1 left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        #Increase points value each hit
        self.alien_points = int(self.alien_points * self.score_scale) 
        