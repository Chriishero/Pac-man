from enum import EnumMeta, Enum, auto
from abc import ABC, ABCMeta


class GUIState(Enum):
    MAIN_MENU = auto()
    MODE_MENU = auto()
    GAME = auto()
    QUIT = auto()


class SceneStateMeta(ABCMeta, EnumMeta):
    ...


class SceneState(ABC, Enum, metaclass=SceneStateMeta):
    ...


class GameState(SceneState):
    PLAYING = auto()
    PAUSE = auto()
    NOT = auto()
