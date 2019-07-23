if self.controller:
    if self.controller.get_hold("left"):
        self.vx = -2
    elif self.controller.get_hold("right"):
        self.vx = 2
    else:
        self.vx = 0

    if self.controller.get_press("up"):
        self.vy = -5
if self.y > game.width:
    self.vy = -10

for c in self.collisions:
    if c[1] == "b":
        self.x = game.WIDTH//4
        self.y = game.HEIGHT//4

self.x += self.vx
self.y += self.vy
self.vy += game.gravity