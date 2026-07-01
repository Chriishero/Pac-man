from pydantic import BaseModel, Field, PrivateAttr
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import threading

if TYPE_CHECKING:
    from .World import World


class Effect(ABC):
    @abstractmethod
    def apply(self, world: World) -> None:
        pass

    @abstractmethod
    def remove(self, world: World) -> None:
        pass


class MakeGhostsEdibleEffect(Effect, BaseModel):
    model_config = {
        "arbitrary_types_allowed": True
    }
    duration: int = Field(ge=0)

    __timer: threading.Timer = PrivateAttr()

    def apply(self, world: World) -> None:
        for g in world.ghosts:
            g.edible = True

        self.__timer = threading.Timer(self.duration, self.remove)
        self.__timer.start()

    def remove(self, world: World) -> None:
        for g in world.ghosts:
            g.edible = False
