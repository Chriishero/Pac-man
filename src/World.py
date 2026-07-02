from pydantic import BaseModel, PrivateAttr
from typing import List
from .Entity import Player, Ghost
from .Object import Pacgum, SuperPacgum
from .Map import Map
from .effect.Effect import Effect


class World(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True
    }

    map: Map
    player: Player
    ghosts: List[Ghost]
    pacgums: List[Pacgum]

    __effects: List[Effect] = PrivateAttr(default_factory=list)

    def apply_effect(self, p: Player, gum: Pacgum) -> None:
        gum.action(p)
        if isinstance(gum, SuperPacgum):
            self.__effects.append(gum.effect)
            gum.effect.apply(self)

    def cleanup_effect(self) -> None:
        for effect in self.__effects:
            if hasattr(effect, "remove"):
                effect.remove(self)
