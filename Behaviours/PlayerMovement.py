if self.controller:
    if self.controller.get_hold("left"):
        self.vx = -2
    elif self.controller.get_hold("right"):
        self.vx = 2
    else:
        self.vx = 0

    if self.controller.get_hold("up"):
        self.vy = -2
    elif self.controller.get_hold("down"):
        self.vy = 2
    else:
        self.vy = 0

self.x += self.vx
self.y += self.vy