from pydantic import BaseModel, Field, model_validator
from abc import ABC, abstractmethod
from typing import Optional, List
import pygame
from .World import World
from .State import GUIState, SceneState, GameState
from .Menu import Button


class Scene(ABC):
    state: Optional[SceneState] = Field(default=None)

    @abstractmethod
    def on_event(self, event: pygame.event.Event) -> GUIState:
        ...

    @abstractmethod
    def on_loop(self) -> None:
        ...

    @abstractmethod
    def on_render(self, s: pygame.SurfaceType) -> None:
        ...


class Game(Scene, BaseModel):
    world: World

    @model_validator(mode="after")
    def validator(self) -> "Game":
        self.state = GameState.NOT
        return self

    def on_event(self, event: pygame.event.Event) -> GUIState:
        return GUIState.GAME

    def on_loop(self) -> None:
        pass

    def on_render(self, s: pygame.SurfaceType) -> None:
        try:
            if self.state == GameState.PLAYING:
                self.__draw_world(s)
        except Exception as e:
            raise ValueError(e)

    def __draw_world(self, s: pygame.SurfaceType) -> None:
        self.__draw_map(s)
        self.__draw_entity(s)
        self.__draw_objects(s)

    def __draw_map(self, s: pygame.SurfaceType) -> None:
        map = self.world.map
        w, h = s.get_width(), s.get_height()
        if w > h:
            case_size = h / map.height
            game_w, game_h = map.width * case_size, map.height * case_size
            top = 0.0
            left = w / 2 - game_w / 2
        else:
            case_size = w / map.width
            game_w, game_h = map.width * case_size, map.height * case_size
            top = game_h / 2.0 - game_h / 2.0
            left = 0.0

        pygame.draw.rect(
            s,
            map.bg_color,
            rect=pygame.Rect(left, top, game_w, game_h)
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
                            s,
                            map.w_color,
                            start_pos=(start_x, start_y),
                            end_pos=(end_x, end_y)
                        )

    def __draw_entity(self, s: pygame.SurfaceType) -> None:
        self.__draw_player(s)
        self.__draw_ghosts(s)

    def __draw_player(self, s: pygame.SurfaceType) -> None:
        pass

    def __draw_ghosts(self, s: pygame.SurfaceType) -> None:
        pass

    def __draw_objects(self, s: pygame.SurfaceType) -> None:
        pass


class Menu(Scene, BaseModel):
    def on_event(self, event: pygame.event.Event) -> GUIState:
        if event == pygame.KEYDOWN:
            if event == pygame.K_ESCAPE:
                return GUIState.QUIT
        return GUIState.MAIN_MENU

    def on_loop(self) -> None:
        pass

    def on_render(self, s: pygame.SurfaceType) -> None:
        b = Button(x=150, y=50, text="Boutton oui")
        b.draw(s)
