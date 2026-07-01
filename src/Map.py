from pydantic import BaseModel, Field, PrivateAttr, model_validator
from typing import List, Dict
from mazegenerator import MazeGenerator  # type:ignore


class MapError(ValueError):
    pass


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
