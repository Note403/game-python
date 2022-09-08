import pygame


class Room:
    def __init__(self, x, y, room_layout):
        self.x = x
        self.y = y

        self.sprite_img = pygame.image.load(
            'assets/dungeon_tiles.png').convert()
        self.floor = self.sprite_img.subsurface(31, 31, 82, 93)
        self.floor = pygame.transform.scale(self.floor, (350, 350))

        self.wall_front = self.sprite_img.subsurface(32, 211, 31, 32)
        self.wall_front = pygame.transform.scale(self.wall_front, (100, 100))

        self.wall_side = self.sprite_img.subsurface(140, 160, 17, 47)
        self.wall_side = pygame.transform.scale(self.wall_side, (75, 100))

        self.doors = {
            'top': 0,
            'bottom': 0,
            'left': 0,
            'right': 0
        }

        self.set_doors(room_layout)

    def set_doors(self, room_layout):
        if self.x > 0:
            self.doors['left'] = room_layout[self.y][self.x - 1]
        else:
            self.doors['left'] = 0

        if self.x < 4:
            self.doors['right'] = room_layout[self.y][self.x + 1]
        else:
            self.doors['right'] = 0

        if self.y > 0:
            self.doors['top'] = room_layout[self.y - 1][self.x]
        else:
            self.doors['top'] = 0

        if self.y < (len(room_layout) - 1):
            self.doors['bottom'] = room_layout[self.y + 1][self.x]
        else:
            self.doors['bottom'] = 0

    def draw(self, display):
        display.blit(
            self.floor,
            (
                (display.get_width() / 2) - (self.floor.get_width() / 2),
                (display.get_height() / 2) - (self.floor.get_height() / 2)
            )
        )

    def get_top_wall_cords(self, display):
        last_x = (display.get_width() / 2) - (self.floor.get_width() / 2)
        final_x = last_x + self.floor.get_width()
        wall_y = (display.get_height() / 2) - (self.floor.get_height() /
                                               2) - (self.wall_front.get_height() / 2)

        cords = []

        while last_x < final_x:
            dist_left = self.floor.get_width() - (len(cords) * 100)

            if dist_left >= 100:
                cords.append([last_x, wall_y])
                last_x += 100
            else:
                cords.append([last_x - dist_left, wall_y])
                last_x += dist_left

        return cords

    def get_side_wall_cords(self, display):
        last_y = (display.get_height() / 2) - (self.floor.get_height() / 2)
        final_y = last_y + self.floor.get_height() - (self.wall_front.get_height() / 2)
        wall_x = (display.get_width() / 2) - \
            (self.floor.get_width() / 2) - (self.wall_side.get_width() / 2)

        cords = []

        while last_y < final_y:
            dist_left = self.floor.get_height() - (len(cords) * self.wall_side.get_height())

            if dist_left >= 100:
                cords.append([wall_x, last_y])
                last_y += self.wall_side.get_height()
            else:
                cords.append([wall_x, last_y - dist_left])
                last_y += dist_left

        return cords
