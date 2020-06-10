import arcade


class Zombie(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super(Zombie, self).__init__(*args, **kwargs)
        self.health = 100