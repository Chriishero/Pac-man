from pydantic import BaseModel, Field
from enum import Enum


class Behavior(Enum):
    CHASE_VIEW = 0
    CHASE_DISTANCE = 1
    CHASE_RANDOM = 2
    PASSIF = 3
    RUNAWAY = 4


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
