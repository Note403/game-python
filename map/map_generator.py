import pygame
import random
from map.room import Room


class MapGenerator:
    def __init__(self):
        self.rooms_count = random.randint(4, 8)
        self.rooms = []
        self.room_layout = self.generate_default_layout()
        self.loaded_room = None
        self.spawn_room = [2, 0]
        self.room_atm = [2, 0]
        self.boss_room = None

    def generate_default_layout(self):
        layout = []

        for row in range(self.rooms_count):
            if row == 0:
                layout.append([0, 0, 1, 0, 0])
            else:
                layout.append([0, 0, 0, 0, 0])

        return layout

    def generate_room_layout(self):
        rooms_set = 1
        room_pos = self.spawn_room

        while rooms_set < self.rooms_count:
            position_data = self.get_possible_positions(room_pos[0], room_pos[1])
            for position_index, position in enumerate(position_data):
                if not position['val']:
                    position['val'] = random.randint(0, 1)

                    if position['val']:
                        rooms_set += 1
                        self.room_layout[position['pos'][1]][position['pos'][0]] = 1
                        room_pos = [position['pos'][0], position['pos'][1]]

        self.remove_empty_rows()
        self.create_rooms()
        self.choose_boss_room()

    def get_possible_positions(self, x, y):
        positions = []
        position_data = []

        if y > 0:
            positions.append([x, y - 1])

        if y < (self.rooms_count - 1):
            positions.append([x, y + 1])

        if x > 0:
            positions.append([x - 1, y])

        if x < 5:
            positions.append([x + 1, y])

        for position in positions:
            try:
                position_data.append(
                    {
                        'pos': position,
                        'val': self.room_layout[position[1]][position[0]]
                    }
                )
            except:
                continue

        return position_data

    def remove_empty_rows(self):
        for row in self.room_layout:
            has_room = 0
            for room in row:
                if room:
                    has_room = 1

            if not has_room:
                self.room_layout.remove(row)

    # DEBUG FUNCTIONS #########

    def debug_layout(self):
        for row in self.room_layout:
            print(row)

    def debug_doors(self):
        for room in self.rooms:
            print(room.doors)

    ##########################

    def create_rooms(self):
        for y, row in enumerate(self.room_layout):
            for x, room in enumerate(row):
                if room:
                    self.rooms.append(Room(x, y, self.room_layout))

    def get_room(self):
        for room in self.rooms:
            if room.x == self.room_atm[0] and room.y == self.room_atm[1]:
                return room

    def player_in_door(self, player, room):
        if room.enemies_alive != 0:
            return False

        for cords in room.door_cords:
            door_rect = pygame.rect.Rect(cords[0], cords[1], 32, 32)
            player_rect = pygame.rect.Rect(player.f_x, player.f_y, player.width, player.height)

            if door_rect.colliderect(player_rect):
                return cords

        return False

    def choose_boss_room(self):
        for room in self.rooms:
            if len(room.door_cords) == 1:
                if room.x != self.spawn_room[0] and room.y != self.spawn_room[1]:
                    self.boss_room = [room.x, room.y]
                    room.boss_room = True

        if self.boss_room is None:
            for room in self.rooms:
                if len(room.door_cords) >= 2:
                    if room.x != self.spawn_room[0] and room.y != self.spawn_room[1]:
                        self.boss_room = [room.x, room.y]
                        room.boss_room = True

