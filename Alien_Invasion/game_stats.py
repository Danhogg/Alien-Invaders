class GameStats:
    """Track statistics for alien invasion"""

    def __init__(self, ai_game):
        """Initialise statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        #Start alien invasion in an inactive stat
        self.game_active = False
        # High score should never be reset so we intitialise here not in reset stats
        self.high_score = 0

    def reset_stats(self):
        """Initialise statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
