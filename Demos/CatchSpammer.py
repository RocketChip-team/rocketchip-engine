from Engine import *

if __name__ == "__main__":
    sheet = Sheet("Sheets/bank1.chr")
    game = Game(10*16, 4/5.0, (255, 255, 255), 60, "Pygame Boilerplate", sheet, scale=2)
    game.fog_instensity = 0
    palette = pal_load("Palettes/palette.pal")
    torchpal = pal_load("Palettes/torch.pal")

    player = GameObject(game.WIDTH/2/game.scale-16, game.HEIGHT/2/game.scale-16, sheet, palette, [4, 2], False, "p", {"Move":open("Behaviours/Catcher.py", "r").read()})
    player.sprite.setiles([22, 22, 1, 1, 22, 22, 1, 1], [0, 4, 0, 4, 2, 6, 2, 6])
    player.controller = Controller(1)
    player.controller.bind("lctrl", pygame.K_LCTRL)
    player.controller.bind("rctrl", pygame.K_RCTRL)
    game.add_object(player)
    while game.RUNNING:
        game.events()
        game.update()
        game.draw()
    pygame.quit()
    quit()
