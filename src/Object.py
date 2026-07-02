from pydantic import BaseModel, Field
from abc import ABC
from .effect.Effect import Effect
from .Entity import Player


class Object(ABC):
    x: int
    y: int


class Pacgum(Object, BaseModel):
    score: int = Field(ge=0)

    def action(self, p: Player) -> None:
        p.score += self.score


class SuperPacgum(Pacgum):
    model_config = {
        "arbitrary_types_allowed": True
    }

    duration: int = Field(ge=0)
    effect: Effect


class Cherry(Object, BaseModel):
    score: int = Field(ge=0)


class Stawberry(Object, BaseModel):
    score: int = Field(ge=0)
