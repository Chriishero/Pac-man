from pydantic import BaseModel, Field
import pygame


class Button(BaseModel):
    x: int
    y: int
    text: str = Field(default="Menu")

    def draw(self, s: pygame.Surface) -> None:
        w, h = s.get_size()
        pygame.draw.rect(
            s, 'light gray', [w/2, h/2, self.x, self.y], 0, 5
        )
        pygame.draw.rect(s, "dark gray", [w/2, h/2, self.x, self.y], 5, 5)
        font = pygame.font.SysFont(name=None, size=24)
        text = font.render(self.text, True, "red")
        s.blit(text, (w/2, h/2))
        