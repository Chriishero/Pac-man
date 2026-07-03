from pydantic import BaseModel, Field, PrivateAttr
import pygame
from typing import Dict
import sys
from .World import World
from .Scene import Scene, Game
from .State import GUIState


class GUI(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True
    }

    width: float = Field(ge=256, default=800)
    height: float = Field(ge=144, default=600)
    fps: float = Field(ge=5, default=5)
    world: World

    __state: GUIState = PrivateAttr()
    __screen: pygame.SurfaceType = PrivateAttr()
    __clock: pygame.time.Clock = PrivateAttr()
    __scene: Dict[GUIState, Scene] = PrivateAttr()

    def init(self) -> None:
        try:
            pygame.init()
            self.__screen = pygame.display.set_mode((self.width, self.height),
                                                    pygame.RESIZABLE)
            self.__clock = pygame.time.Clock()
            self.__scene = {
                GUIState.MAIN_MENU: Game(world=self.world),
                GUIState.MODE_MENU: Game(world=self.world),
                GUIState.GAME: Game(world=self.world)
            }
        except Exception as e:
            raise ValueError("Failed to initialize pygame:", e)

    def run(self) -> None:
        self.__state = GUIState.MAIN_MENU
        while self.__state is not GUIState.QUIT:
            scene = self.__scene[self.__state]
            for event in pygame.event.get():
                self.__on_event(scene, event)
            self.__on_loop(scene)
            self.__on_render(scene)
        self.__on_cleanup()

    def __on_event(self, s: Scene, event: pygame.event.EventType) -> None:
        if event.type == pygame.QUIT:
            self.__state = GUIState.QUIT
            s.on_event(event)

    def __on_loop(self, s: Scene) -> None:
        s.on_loop()

    def __on_render(self, s: Scene) -> None:
        s.on_render(self.__screen)
        pygame.display.flip()
        self.__clock.tick(self.fps)

    def __on_cleanup(self) -> None:
        pygame.quit()
        sys.exit()
