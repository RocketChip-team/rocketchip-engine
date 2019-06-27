from Engine import *

if __name__ == "__main__":
    sheet = Sheet("Sheets/bank1.chr")
    game = Game(25*16, 4/5.0, (255, 255, 255), 60, "Pygame Boilerplate", sheet, scale=2)
    game.fog_instensity = 255
    palette = pal_load("Palettes/palette.pal")
    torchpal = pal_load("Palettes/torch.pal")

    player = GameObject(0, 0, sheet, palette, 0, (2, 2), False, "p", {"Move":open("Behaviours/PlayerMovement.py", "r").read()})
    player.sprite.setiles([22, 22, 22, 22], [0, 4, 2, 6])
    player.controller = Controller(1)
    player.light = FogLight(player, 300)
    dupli = GameObject(127, 127, sheet, torchpal, 0, (1, 1), True, "p", {}, latency=20)
    dupli.sprite.addframe([[27]])
    dupli.sprite.addframe([[28]])
    dupli.sprite.addanimation("IDLE",  indexes=[1, 2])
    dupli.sprite.playanimation("IDLE")
    dupli.light = FogLight(dupli, 200)
    game.add_object(player)
    game.add_object(dupli)
    while game.RUNNING:
        game.events()
        game.update()
        game.draw()
    pygame.quit()