#   2022/03/29 -Sasen Perera
#   <----------------------->
#   \-----------------------/
#    \      PlatFormer     /
#     \-------------------/
#
#

import pyxel as px

TRANSPARENT_COLOR = 2
SCROLL_BORDER_X = 80
TILE_FLOOR = (0, 1)
LAVA = (2, 0)
ROCK = (1, 1)
PLAYER = (1, 0)
WALL_TILE_X = 4

scroll_x = 0
player = None
enemies = []

def get_tile(tile_x, tile_y):
    return px.tilemap(0).pget(tile_x, tile_y)

def detect_collision(x, y, dy):
    x1 = x // 8
    y1 = y // 8
    x2 = (x + 8 - 1) // 8
    y2 = (y + 8 - 1) // 8
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if get_tile(xi, yi)[0] >= WALL_TILE_X:
                return True
    if dy > 0 and y % 8 == 1:
        for xi in range(x1, x2 + 1):
            if get_tile(xi, y1 + 1) == TILE_FLOOR:
                return True
    return False

def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if elem.is_alive:
            i += 1
        else:
            list.pop(i)

def push_back(x, y, dx, dy):
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    if abs_dx > abs_dy:
        sign = 1 if dx > 0 else -1
        for _ in range(abs_dx):
            if detect_collision(x + sign, y, dy):
                break
            x += sign
        sign = 1 if dy > 0 else -1
        for _ in range(abs_dy):
            if detect_collision(x, y + sign, dy):
                break
            y += sign
    else:
        sign = 1 if dy > 0 else -1
        for _ in range(abs_dy):
            if detect_collision(x, y + sign, dy):
                break
            y += sign
        sign = 1 if dx > 0 else -1
        for _ in range(abs_dx):
            if detect_collision(x + sign, y, dy):
                break
            x += sign
    return x, y, dx, dy

def is_wall(x, y):
    tile = get_tile(x // 8, y // 8)
    return tile == TILE_FLOOR or tile[0] >= WALL_TILE_X

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.direction = 1
        self.is_falling = False

    def update(self):
        global scroll_x
        last_y = self.y
        if px.btn(px.KEY_LEFT):
            self.dx = -2
            self.direction = -1
        if px.btn(px.KEY_RIGHT):
            self.dx = 2
            self.direction = 1
        self.dy = min(self.dy + 1, 3)
        if px.btnp(px.KEY_SPACE):
            self.dy = -6
            px.play(3, 8)
        self.x, self.y, self.dx, self.dy = push_back(self.x, self.y, self.dx, self.dy)
        if self.x < scroll_x:
            self.x = scroll_x
        if self.y < 0:
            self.y = 0
        self.dx = int(self.dx * 0.8)
        self.is_falling = self.y > last_y

        if self.x > scroll_x + SCROLL_BORDER_X:
            last_scroll_x = scroll_x
            scroll_x = min(self.x - SCROLL_BORDER_X, 240 * 8)

    def draw(self):
        u = (2 if self.is_falling else px.frame_count // 3 % 2) * 8
        w = 8 if self.direction > 0 else -8
        px.blt(self.x, self.y, 0, u, 16, w, 8, TRANSPARENT_COLOR)

class app():
    def __init__(self):
        px.init(128, 128, title="Platformer")
        px.load("assets/assets.pyxres")
        px.image(0).load(0, 0, "assets/player.png")
        global player
        player = Player(0, 0)
        px.playm(0, loop=True)
        px.run(self.update, self.draw)

    def update(self):
        if px.btn(px.KEY_Q):
            px.quit()

        player.update()

    def draw(self):
        px.cls(0)

        px.camera()
        px.bltm(0, 0, 0, (scroll_x // 4) % 128, 128, 128, 128)
        px.bltm(0, 0, 0, scroll_x, 0, 128, 128, TRANSPARENT_COLOR)

        px.camera(scroll_x, 0)
        player.draw()

def game_over():
    global scroll_x, enemies
    scroll_x = 0
    player.x = 0
    player.y = 0
    player.dx = 0
    player.dy = 0
    px.play(3, 9)

app()