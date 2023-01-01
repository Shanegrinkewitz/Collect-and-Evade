import arcade
import random
import math

class CollectibleSprite(arcade.SpriteCircle):

    def __init__(self):
        super().__init__(10, (0, 0, 0))
    
    def place_randomly_away_from_player(self, player_sprite: arcade.Sprite):
        width, height = arcade.get_window().get_size()
        self.center_x = random.random() * width
        self.center_y = random.random() * height

        MIN_DISTANCE = 300
        while math.sqrt((self.center_x - player_sprite.center_x)**2 + (self.center_y - player_sprite.center_y)**2) < MIN_DISTANCE:
            self.center_x = random.random() * width
            self.center_y = random.random() * height

class HazardSprite(arcade.SpriteCircle):

    def __init__(self):
        super().__init__(10, (255, 0, 0))

        self.MIN_SPEED = 40
        self.MAX_SPEED = 200
    
    def place_randomly_away_from_player(self, player_sprite: arcade.Sprite):
        width, height = arcade.get_window().get_size()
        self.center_x = random.random() * width
        self.center_y = random.random() * height

        MIN_DISTANCE = 300
        while math.sqrt((self.center_x - player_sprite.center_x)**2 + (self.center_y - player_sprite.center_y)**2) < MIN_DISTANCE:
            self.center_x = random.random() * width
            self.center_y = random.random() * height
        
        # Set the velocity
        speed = random.random() * (self.MAX_SPEED - self.MIN_SPEED) + self.MIN_SPEED
        angle = random.random() * 360
        self.change_x = speed * math.cos(math.radians(angle))
        self.change_y = speed * math.sin(math.radians(angle))

    
    def on_update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        width, height = arcade.get_window().get_size()
        if self.left < 0 and self.change_x < 0 or self.right > width and self.change_x > 0:
            self.change_x *= -1
        if self.bottom < 0 and self.change_y < 0 or self.top > height and self.change_y > 0:
            self.change_y *= -1