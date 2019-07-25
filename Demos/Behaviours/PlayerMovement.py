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
    print("yes respawn")
    self.x = game.WIDTH//4
    self.y = game.HEIGHT//4

if self.test_collision_stay("t"):
    print("It's hot!!!")
    self.sprite.setpalette(pal_load("Palettes/torch.pal"))

if self.test_collision_quit("t"):
    print("Hooo that's better.")
    self.sprite.setpalette(pal_load("Palettes/palette.pal"))


self.x += self.vx
self.y += self.vy
#self.vy += game.gravity