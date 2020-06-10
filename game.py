
import random
import time

import arcade

from player import Player
from zombie import Zombie

SPRITE_SCALING_PLAYER = 1.0
SPRITE_SCALING_BULLET = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_PACE = 5

RIGHT_FACING = 0
LEFT_FACING = 1

BULLET_SPEED = 10



class MyGame(arcade.Window):
    def __init__(self):
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Zombie Horror")

        # Variables that will hold sprite lists
        self.player_list = None
        self.zombie_list = None
        self.bullet_list = None

        # Set up the player info
        self.player = None
        self.zombie = None
        self.game_status = "Game is on"

        self.laser_sound = arcade.load_sound("laser.ogg")

        # Don't show the mouse cursor
        self.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        self.game_status = "Game is on"

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player = Player()
        self.player.center_x = 50
        self.player.center_y = 50
        self.player_list.append(self.player)

        self.zombie = Zombie("images/zombie/zombie_stand.png", SPRITE_SCALING_PLAYER)
        self.zombie.center_x = 500
        self.zombie.center_y = 200
        self.zombie_list.append(self.zombie)

    def on_draw(self):
        arcade.start_render()

        self.zombie_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()

        arcade.draw_text(self.game_status, 10, 20, arcade.color.BLACK, 14)
        arcade.draw_text("Player health: " + str(self.player.health), 10, 40, arcade.color.BLACK, 14)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_PACE
            if self.player.left < 0:
                self.player.left = 0
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_PACE
            if self.player.right > SCREEN_WIDTH:
                self.player.right = SCREEN_WIDTH
        elif key == arcade.key.UP:
            self.player.change_y = PLAYER_PACE
            if self.player.top > SCREEN_HEIGHT:
                self.player.top = SCREEN_HEIGHT
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_PACE
            if self.player.bottom < 0:
                self.player.bottom = 0
        elif key == arcade.key.SPACE:
            # Create a bullet
            bullet = arcade.Sprite("bullet.png", SPRITE_SCALING_BULLET)
            bullet.center_x = self.player.center_x + 20
            bullet.center_y = self.player.center_y
            bullet.change_x = BULLET_SPEED
            arcade.play_sound(self.laser_sound)

            # Add the bullet to the appropriate list
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0


    def update(self, delta_time):

        self.bullet_list.update()
        self.player_list.update()
        self.player_list.update_animation(delta_time)
        self.zombie_list.update()

        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.zombie_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            zombie: Zombie
            for zombie in hit_list:
                zombie.health -= 10
                print(f"Zombie health: {zombie.health}")
            if bullet.left > SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

        zombie_bite_list = arcade.check_for_collision_with_list(self.player,
                                                                self.zombie_list)

        if len(zombie_bite_list) > 0:
            # self.game_status = "You lose!"
            self.player.health -= 10


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
