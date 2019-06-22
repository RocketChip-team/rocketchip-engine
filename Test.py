from Engine import *

if __name__ == "__main__":
    sheet = Sheet("bank1.chr")
    game = Game(25*16, 4/5.0, (0, 0, 0), 60, "Pygame Boilerplate", sheet, scale=2)
    palette = [(0, 0, 0), (255, 255, 255), (225, 255, 225), (200, 255, 200), (100, 255, 100), (150, 255, 150)]

    player = GameObject(0, 0, sheet, palette, 0, (2, 2), False, "p", {"Move":open("Behaviours/PlayerMovement.py", "r").read()})
    player.sprite.setiles([22, 22, 22, 22], [0, 4, 2, 6])
    player.controller = Controller(1)
    game.add_object(player)
    while game.RUNNING:
        game.events()
        game.update()
        game.draw()
    pygame.quit()
    quit()