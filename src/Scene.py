from pydantic import BaseModel, Field
from abc import ABCMeta, ABC, abstractmethod
from enum import Enum, EnumMeta, auto
import pygame
from .World import World


class MetaState(ABCMeta, EnumMeta):
    ...


class State(Enum, metaclass=MetaState):
    ...


class GameState(State):
    MAIN_MENU = auto()
    GAME_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    CUTSCENE = auto()


class GameType(State):
    PAC_MAN = "PAC-MAN"
    MS_PAC_MAN = "MS PAC-MAN"
    COOKIE_MAN = "COOKIE-MAN"
    LEARN = "LEARN"


class GameMode(State):
    PLAY = "PLAY"
    PLAY_TURBO = "PLAY_TURBO"
    PRACTICE = "PRACTICE"
    CUTSCENES = "CUTSCENES"
    ABOUT = "ABOUT"


class Scene(ABC):
    @abstractmethod
    def on_event(self, event: pygame.event.Event) -> None:
        ...

    @abstractmethod
    def on_loop(self) -> None:
        ...

    @abstractmethod
    def on_render(self) -> None:
        ...


class Game(BaseModel):
    world: World
    state: State = Field(default=GameState.MAIN_MENU)
