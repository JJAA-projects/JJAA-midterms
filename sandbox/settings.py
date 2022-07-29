
class Settings:
    """Class to store all settings"""

    def __init__(self):
        """Initializes the game's settings"""

        self.screen_width = 160
        self.screen_height = 160
        self.tile_size = 16
        self.bg_color = (255, 255, 255)  # background color RGB 0-255

        self.tilemap = [
            'EEEEEEEEEE',
            'E........E',
            'E........E',
            'E........E',
            'E...0....E',
            'E........E',
            'E........E',
            'E........E',
            'E........E',
            'EEEEEEEEEE',
        ]
