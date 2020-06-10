import arcade

RIGHT_FACING = 0
LEFT_FACING = 1

CHARACTER_SCALING = 1.0
UPDATES_PER_FRAME = 7



def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]


class Player(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        self.health = 100
        self.idle_texture_pair = load_texture_pair("images/player/malePerson_idle.png")

        main_path = "images/player/malePerson"
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return


        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
