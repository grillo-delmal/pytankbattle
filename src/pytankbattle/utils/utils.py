import pygame

playerColors = [
    (0x33, 0xBB, 0x33),
    (0xBB, 0x33, 0x33),
    (0x33, 0x33, 0xBB),
    (0x33, 0xBB, 0xBB),
    (0xBB, 0xBB, 0x33),
    (0xBB, 0x33, 0xBB),
    (0x33, 0x33, 0x33),
    (0xBB, 0xBB, 0xBB),
]

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (255, 255, 255))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10
