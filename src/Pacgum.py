from pydantic import BaseModel, Field
from .Effect import Effect
from .Entity import Player


class Pacgum(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    score: int = Field(ge=0)

    def action(self, p: Player) -> None:
        p.score += self.score


class SuperPacgum(Pacgum):
    model_config = {
        "arbitrary_types_allowed": True
    }

    duration: int = Field(ge=0)
    effect: Effect
