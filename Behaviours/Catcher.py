if self.controller:
    if self.controller.get_press("lctrl"):
        self.x += 8
    elif self.controller.get_press("rctrl"):
        self.x += -8
if self.x +16 <= 0:
    print("player 2 wins!")
    game.BACKGROUND = (255, 0, 0)
elif self.x + 16 >= game.WIDTH/game.scale:
    print("player 1 wins")
    game.BACKGROUND = (0, 0, 255)
else:
    game.BACKGROUND = (255, 255, 255)