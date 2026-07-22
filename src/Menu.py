from pydantic import BaseModel, Field
import pygame
from pygame.font import Font
from typing import Union, Tuple


class Label(BaseModel):
    text: str = Field(min_length=1)
    font: Font
    color: Union[str, Tuple[int, int, int]]
    x: int
    y: int

    def draw(self, s: pygame.Surface) -> None:
        text = self.font.render(self.text, True, self.color)
        s.blit(text, (self.x, self.y))


class Button(BaseModel):
    x: int
    y: int
    label: Label

    def draw(self, s: pygame.Surface) -> None:
        w, h = s.get_size()
        pygame.draw.rect(
            s, 'light gray', [w/2, h/2, self.x, self.y], 0, 5
        )
        pygame.draw.rect(s, "dark gray", [w/2, h/2, self.x, self.y], 5, 5)
        self.label.draw(s)
