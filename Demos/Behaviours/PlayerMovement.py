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
if self.y > game.width:
    self.vy = -10

if self.test_collision_enter("b"):
    self.x = game.WIDTH//4
    self.y = game.HEIGHT//4

if self.test_collision_enter("t"):
    self.sprite.setpalette(pal_load("Palettes/torch.pal"))
    self.light.change_radius(500, 15, 512)

if self.test_collision_quit("t"):
    self.sprite.setpalette(pal_load("Palettes/palette.pal"))
    self.light.change_radius(400, 15, 412)


self.x += self.vx
self.y += self.vy
#self.vy += game.gravity