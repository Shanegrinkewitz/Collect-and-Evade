import arcade
import arcade.gui

from sprites import *

views: dict[str, arcade.View] = {
    "main_menu_view": None,
    "game_view": None,
    "pause_view": None
}

class MainMenuView(arcade.View):
    """ The view that represents the main menu of the game """

    def __init__(self):
        super().__init__()

        arcade.set_background_color((180, 180, 180))

        self.manager = arcade.gui.UIManager()

        self.layout = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="Start Game", width=300)
        self.layout.add(start_button.with_space_around(bottom=30))

        options_button = arcade.gui.UIFlatButton(text="Options", width=300)
        self.layout.add(options_button.with_space_around(bottom=30))

        exit_button = arcade.gui.UIFlatButton(text="Exit to Desktop", width=300)
        self.layout.add(exit_button)

        start_button.on_click = self.on_click_start_game
        options_button.on_click = self.on_click_options
        exit_button.on_click = self.on_click_exit

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.layout))

    def on_click_start_game(self, event):
        if not views["game_view"]:
            views["game_view"] = GameView()
        views["game_view"].setup()
        self.window.show_view(views["game_view"])

    def on_click_options(self, event):
        pass

    def on_click_exit(self, event):
        arcade.exit()
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()
    
    def on_show_view(self):
        self.manager.enable()
    
    def on_hide_view(self):
        self.manager.disable()

class GameView(arcade.View):
    """ The view that represents the running game """

    def __init__(self):
        super().__init__()

        self.width = 0
        self.height = 0
        
        self.player_sprite: arcade.Sprite = None
        self.collectible_sprite: arcade.Sprite = None
        self.hazard_sprite_list: arcade.SpriteList = None
        self.collidable_sprite_list: arcade.SpriteList = None

        self.left_key_down = False
        self.right_key_down = False
        self.first_jump = False

        self.score = 0
        self.score_text: arcade.Text = None

        self.collect_sound = arcade.Sound("assets/463202__kenneth-cooney__one-beep.wav")
        self.die_sound = arcade.Sound("assets/467795__sgak__explosion.wav")
        self.collect_sound.play(volume=0)
        self.die_sound.play(volume=0)

        arcade.set_background_color((180, 180, 180))

    def setup(self):
        self.width, self.height = self.window.get_size()

        self.collectible_sprite = None
        self.hazard_sprite_list = arcade.SpriteList()
        self.collidable_sprite_list = arcade.SpriteList()

        self.player_sprite = arcade.SpriteCircle(30, (0, 0, 0))
        self.player_sprite.center_x = self.width / 2
        self.player_sprite.center_y = self.height / 2

        self.left_key_down = False
        self.right_key_down = False
        self.first_jump = False

        self.score = 0
        self.score_text = arcade.Text(
            text="0",
            start_x=self.width - 100,
            start_y=self.height - 100,
            anchor_x="center",
            anchor_y="center",
            color=(0, 0, 0, 150),
            font_size=60
        )

    def on_draw(self):
        self.clear()
        self.player_sprite.draw()
        self.collidable_sprite_list.draw()
        self.score_text.draw()
    
    def on_update(self, delta_time):
        if not self.first_jump:
            return
        
        # Collision detection
        collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.collidable_sprite_list)
        for collidable_sprite in collision_list:
            if collidable_sprite is self.collectible_sprite:
                self.score += 1
                self.score_text.value = self.score
                self.collect_sound.play()
                self.collectible_sprite.place_randomly_away_from_player(self.player_sprite)
                hazard_sprite = HazardSprite()
                hazard_sprite.place_randomly_away_from_player(self.player_sprite)
                self.hazard_sprite_list.append(hazard_sprite)
                self.collidable_sprite_list.append(hazard_sprite)
            elif collidable_sprite in self.hazard_sprite_list:
                self.game_over()
        
        # Check if player is out of bounds
        if (self.player_sprite.center_x < 0 or
            self.player_sprite.center_x > self.width or
            self.player_sprite.center_y < 0 or
            self.player_sprite.center_y > self.height):
            self.game_over()
        
        # Process motion of sprites
        GRAVITY = 30
        self.player_sprite.change_y -= GRAVITY * delta_time

        TURN_RATE = 6 * delta_time
        MAX_SPEED_X = 300 * delta_time
        if self.left_key_down and not self.right_key_down and self.player_sprite.change_x > -MAX_SPEED_X:
            self.player_sprite.change_x -= TURN_RATE
        elif self.right_key_down and not self.left_key_down and self.player_sprite.change_x < MAX_SPEED_X:
            self.player_sprite.change_x += TURN_RATE

        self.player_sprite.update()
        self.collidable_sprite_list.on_update(delta_time)

    def game_over(self):
        self.die_sound.play()
        self.window.show_view(views["main_menu_view"])
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if not self.first_jump:
                self.first_jump = True
                self.collectible_sprite = CollectibleSprite()
                self.collectible_sprite.place_randomly_away_from_player(self.player_sprite)
                self.collidable_sprite_list.append(self.collectible_sprite)
            self.player_sprite.change_y += 10
        elif key == arcade.key.LEFT:
            self.left_key_down = True
        elif key == arcade.key.RIGHT:
            self.right_key_down = True
        elif key == arcade.key.P:
            if not views["pause_view"]:
                views["pause_view"] = PauseView()
            self.window.show_view(views["pause_view"])
        elif key == arcade.key.ESCAPE:
            arcade.exit()
    
    def on_key_release(self, key, _modifiers):
        if key == arcade.key.LEFT:
            self.left_key_down = False
        elif key == arcade.key.RIGHT:
            self.right_key_down = False

class PauseView(arcade.View):
    
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()

        self.layout = arcade.gui.UIBoxLayout()

        resume_button = arcade.gui.UIFlatButton(text="Resume", width=300)
        self.layout.add(resume_button.with_space_around(bottom=30))

        exit_button = arcade.gui.UIFlatButton(text="Exit to Main Menu", width=300)
        self.layout.add(exit_button)

        resume_button.on_click = self.on_click_resume
        exit_button.on_click = self.on_click_exit

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.layout))

    def on_click_resume(self, event):
        self.window.show_view(views["game_view"])
    
    def on_click_exit(self, event):
        self.window.show_view(views["main_menu_view"])
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self.window.show_view(views["game_view"])
        elif key == arcade.key.ESCAPE:
            arcade.exit()
    
    def on_show_view(self):
        self.manager.enable()
    
    def on_hide_view(self):
        self.manager.disable()