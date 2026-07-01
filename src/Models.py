from pydantic import BaseModel, Field, PrivateAttr, model_validator
from typing import List, Dict, TYPE_CHECKING
from enum import Enum
from mazegenerator import MazeGenerator
from .CustomExceptions import MapError

if TYPE_CHECKING:
    from .Effect import Effect


class Behavior(Enum):
    CHASE_VIEW = 0
    CHASE_DISTANCE = 1
    CHASE_RANDOM = 2
    PASSIF = 3
    RUNAWAY = 4


class Map(BaseModel):
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    perfect: bool = Field(default=False)
    seed: int = Field(ge=0, default=42)

    __maze: List[List[int]] = PrivateAttr()

    @model_validator(mode="after")
    def validator(self) -> "Map":
        try:
            gen = MazeGenerator(
                size=(self.width, self.height),
                perfect=self.perfect,
            )
            self._maze = gen.maze
        except Exception as e:
            raise MapError(e)

        return self

    @property
    def maze(self) -> List[List[int]]:
        return self.__maze

    def get_walls(self, x: int, y: int) -> Dict[str, bool]:
        try:
            v = self.__maze[y][x]
        except IndexError as e:
            raise IndexError(e)

        return {
            "N": bool(v & 1),
            "S": bool(v & 2),
            "E": bool(v & 4),
            "W": bool(v & 8)
        }


class Entity(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    v: int = Field(ge=0)


class Player(Entity):
    n_live: int = Field(ge=1, default=3)
    x_respawn: int = Field(ge=0)
    y_respawn: int = Field(ge=0)
    score: int = Field(ge=0, default=0)


class Ghost(Entity):
    model_config = {
        "arbitrary_types_allowed": True
    }

    edible: bool = Field(default=False)
    behavior: Behavior = Field(default=Behavior.PASSIF)


class Pacgum(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    score: int = Field(ge=0)

    def action(self, p: Player) -> None:
        p.score += self.score


class SuperPacgum(Pacgum):
    duration: int = Field(ge=0)
    effect: Effect


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
