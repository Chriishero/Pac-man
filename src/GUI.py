from pydantic import BaseModel, Field, PrivateAttr
import pygame
import sys
from .Scene import Game, GameState


class GUI(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True
    }

    width: float = Field(ge=256, default=800)
    height: float = Field(ge=144, default=600)
    fps: float = Field(ge=5, default=5)
    game: Game

    __state: bool = PrivateAttr()
    __screen: pygame.SurfaceType = PrivateAttr()
    __clock: pygame.time.Clock = PrivateAttr()

    def init(self) -> None:
        try:
            pygame.init()
            self.__screen = pygame.display.set_mode((self.width, self.height))
            self.__clock = pygame.time.Clock()
        except Exception as e:
            raise ValueError("Failed to initialize pygame:", e)

    def run(self) -> None:
        self.__state = True
        while self.__state is True:
            for event in pygame.event.get():
                self.__on_event(event)
            self.__on_loop()
            self.__on_render()
        self.__on_cleanup()

    def __on_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.__state = False

    def __on_loop(self) -> None:
        pass

    def __on_render(self) -> None:
        if self.game.state == GameState.PLAYING:
            self.__render_game()
        pygame.display.flip()
        self.__clock.tick(self.fps)

    def __render_game(self) -> None:
        try:
            self.__draw_world()
        except Exception as e:
            raise ValueError(e)

    def __draw_world(self) -> None:
        self.__draw_map()
        self.__draw_entity()
        self.__draw_objects()

    def __draw_map(self) -> None:
        map = self.game.world.map
        if self.width > self.height:
            case_size = self.height / map.height
            w, h = map.width * case_size, map.height * case_size
            top = 0.0
            left = self.width / 2 - w / 2
        else:
            case_size = self.width / map.width
            w, h = map.width * case_size, map.height * case_size
            top = self.height / 2.0 - h / 2.0
            left = 0.0

        pygame.draw.rect(
            self.__screen,
            map.bg_color,
            rect=pygame.Rect(left, top, w, h)
        )
        for y in range(0, map.height, 1):
            for x in range(0, map.width, 1):
                walls = map.get_walls(x, y)
                for w, v in walls.items():
                    if w == "N" or w == "W":
                        start_x = left + case_size * x
                        start_y = top + case_size * y
                        if w == "N":
                            end_x = start_x + case_size
                            end_y = start_y
                        else:
                            end_x = start_x
                            end_y = start_y + case_size
                    else:
                        start_x = left + case_size * (x + 1) - 1
                        start_y = top + case_size * (y + 1) - 1
                        if w == "S":
                            end_x = start_x - case_size
                            end_y = start_y
                        else:
                            end_x = start_x
                            end_y = start_y - case_size
                    if v is True:
                        pygame.draw.line(
                            self.__screen,
                            map.w_color,
                            start_pos=(start_x, start_y),
                            end_pos=(end_x, end_y)
                        )

    def __draw_entity(self) -> None:
        self.__draw_player()
        self.__draw_ghosts()

    def __draw_player(self) -> None:
        pass

    def __draw_ghosts(self) -> None:
        pass

    def __draw_objects(self) -> None:
        pass

    def __on_cleanup(self) -> None:
        pygame.quit()
        sys.exit()
