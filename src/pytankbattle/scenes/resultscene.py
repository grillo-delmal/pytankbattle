import pygame

from .scene import Scene
from ..controller import Controller
from ..utils.data import GameState

class ResultScene(Scene):
    def __init__(self, engine, data):
        super().__init__()
        self.engine = engine
        self.data = data

    def winners(self):
        win_score = -1
        win_pid = []

        for pid in range(len(self.data.players)):
            score = self.data.players[pid].score
            if score > win_score:
                win_pid = [pid]
                win_score = score
            elif score == win_score:
                win_pid.append(pid)
        return win_pid

    def run(self):
        win_pid = self.winners()
        self.engine.screen.fill("black")

        font = pygame.font.Font(None, 64)
        title_bmp = None
        if len(win_pid) > 1:
            title_bmp = font.render(
                "It's a Tie! Players %s won!" % (
                    ", ".join(
                        ["%d" % (pid + 1) for pid in win_pid])
                    ),
                True, 
                (255, 255, 255))
        elif len(win_pid) == 1:
            title_bmp = font.render(
                "Player %d won!" % (win_pid[0] + 1), 
                True, 
                (255, 255, 255))
        else:
            title_bmp = font.render(
                "¯\_(ツ)_/¯", 
                True, 
                (255, 255, 255))
        self.engine.screen.blit(
            title_bmp,
            (400 - title_bmp.get_width()/2, 250))

        font = pygame.font.Font(None, 32)
        text_bmp = font.render(
            "Press A / Enter button to go back to the title screen",
            True, 
            (255, 255, 255))
        self.engine.screen.blit(
            text_bmp,
            (400 - text_bmp.get_width()/2, 350))
        text_bmp = font.render(
            "B / Backspace to quit", 
            True, 
            (255, 255, 255))
        self.engine.screen.blit(
            text_bmp,
            (400 - text_bmp.get_width()/2, 380))


        for CD in self.data.controllers:
            p = CD.player
            if p is None or CD.mode is None:
                continue

            # Return to menu
            if CD.btns_d[Controller.Buttons.A]:
                return GameState.MENU

            # Quit game
            if CD.btns_d[Controller.Buttons.B]:
                return GameState.CREDITS

        return GameState.RESULT

