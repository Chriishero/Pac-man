from pydantic import BaseModel, Field, PrivateAttr, model_validator
from typing import List, Dict, Tuple
from mazegenerator import MazeGenerator  # type:ignore


class MapError(ValueError):
    pass


class Map(BaseModel):
    width: int = Field(ge=1, default=15)
    height: int = Field(ge=1, default=15)
    perfect: bool = Field(default=False)
    seed: int = Field(ge=0, default=42)
    bg_color: Tuple[int, int, int] = Field(default=(128, 128, 128))
    w_color: Tuple[int, int, int] = Field(default=(255, 255, 255))

    __maze: List[List[int]] = PrivateAttr()

    @model_validator(mode="after")
    def validator(self) -> "Map":
        try:
            gen = MazeGenerator(
                size=(self.width, self.height),
                perfect=self.perfect,
            )
            self.__maze = gen.maze
        except Exception as e:
            raise MapError(e)

        return self

    @property
    def maze(self) -> List[List[int]]:
        return self.__maze

    def get_walls(self, x: int, y: int) -> Dict[str, bool]:
        try:
            v = self.maze[y][x]
        except IndexError as e:
            raise IndexError(e)

        return {
            "N": bool(v & 1),
            "S": bool(v & 2),
            "E": bool(v & 4),
            "W": bool(v & 8)
        }
