import arcade
import sys

from view_manager import MainMenuView
from view_manager import views

TITLE = "Game"

def main():
    window: arcade.Window
    if "--windowed" in sys.argv:
        window = arcade.Window(title=TITLE, resizable=True)
        window.maximize()
    else:
        window = arcade.Window(title=TITLE, fullscreen=True, vsync=True)
    views["main_menu_view"] = MainMenuView()
    window.show_view(views["main_menu_view"])
    arcade.run()

if __name__ == "__main__":
    main()