from .World import World
from .Map import Map
from .Entity import Player
from .GUI import GUI


def main() -> None:
    world = World(
        map=Map(),
        player=Player(x=0, y=0, v=1, x_respawn=0, y_respawn=0),
        ghosts=list(),
        pacgums=list()
    )
    gui = GUI(world=world)
    gui.init()
    gui.run()


if __name__ == "__main__":
    main()
