import random

BOMB_NUM = 10


class Map:
    around = [
        (-1, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1)
    ]

    def __init__(self):
        self.map = []

    def makeMap(self, size: int):
        self.map = [[0 for x in range(size)] for x in range(size)]
        bomb = []

        while True:
            x = random.randrange(size)
            y = random.randrange(size)
            if [x, y] in bomb:
                continue
            bomb.append([x, y])
            self.map[y][x] = 5
            if len(bomb) >= BOMB_NUM:
                break

        for x in range(size):
            for y in range(size):
                if self.map[y][x] == 5:
                    for dx, dy in self.around:
                        if (y + dy) < 0 or (y + dy) >= size or (x + dx) < 0 or (x + dx) >= size:
                            continue
                        if self.map[y + dy][x + dx] != 5:
                            self.map[y + dy][x + dx] += 1

        return self.map
