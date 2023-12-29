from enum import Enum, auto

from ..controller import Controller
from ..map import mstps
from ..entities import Player
from ..utils import *
from .scene import Scene


class State(Enum):
    ADD_TANK = auto()
    REMOVE_TANK = auto()
    SELECT_TANK = auto()
    SELECTING_TANK = auto()
    SELECT_COLOR = auto()
    SELECTING_COLOR = auto()
    START = auto()


class MenuScene(Scene):
    class FlowStep():
        def __init__(self, act, left:State, right:State, b:State=None, a:State=None):
            self.act = act
            self.left = left
            self.right = right
            self.a = a
            self.b = b

    class Cursor():
        def __init__(self, controller:Controller):
            self.controller = controller
            self.pos = State.ADD_TANK

            self.controller_i = 0
            self.tank_i = 0
            self.color_i = 0
            self.color_t = Controller.Mode.BOTH
       
    def __init__(self, engine, data):
        super().__init__()
        self.engine = engine
        self.controllers = data.controllers
        self.players = data.players
        self.data = data
        self.start_game = False

        self.cursors = []

        self.flow = {
            State.ADD_TANK:
                self.FlowStep(
                    self.add_tank, 
                    None, State.REMOVE_TANK),
            State.REMOVE_TANK:     
                self.FlowStep(
                    self.remove_tank, 
                    State.ADD_TANK, State.SELECT_TANK),
            State.SELECT_TANK:
                self.FlowStep(
                    None,
                    State.REMOVE_TANK, State.SELECT_COLOR,
                    a=State.SELECTING_TANK),
            State.SELECTING_TANK: 
                self.FlowStep(
                    self.select_tank, 
                    None, None,
                    b=State.SELECT_TANK),
            State.SELECT_COLOR:
                self.FlowStep(
                    None,
                    State.SELECT_TANK, State.START,
                    a=State.SELECTING_COLOR),
            State.SELECTING_COLOR: 
                self.FlowStep(
                    self.select_color, 
                    None, None,
                    b=State.SELECT_COLOR),
            State.START:
                self.FlowStep(
                    self.start,
                    State.SELECT_COLOR, None)
        }

    def add_tank(self, cur):
        if cur.controller.btns_d[Controller.Buttons.A]:
            pi = len(self.players)
            if pi >= len(playerColors):
                return
            if pi >= len(self.controllers):
                return
            p = Player(mstps[pi], playerColors[pi])
            self.players.append(p)
            for c in self.controllers:
                if c.player is None:
                    c.setPlayer(p, Controller.Mode.BOTH)
                    break

    def remove_tank(self, cur):
        if cur.controller.btns_d[Controller.Buttons.A]:
            if len(self.players) == 0:
                return
            rmi = len(self.players) - 1
            rmp = self.players[rmi]

            for c in self.controllers:
                if rmp == c.player:
                    c.player = None

            del self.players[rmi]

    def reset_cursor(self, cur):
        cur.controller_i = 0
        cur.tank_i = -1
        if self.controllers[cur.controller_i].player is not None:
            for i in range(len(self.players)):
                if self.players[i] == self.controllers[cur.controller_i].player:
                    cur.tank_i = i
                    break

    def select_tank(self, cur):
        # LR select tank
        if cur.controller.btns_d[Controller.Buttons.LEFT]:
            cur.tank_i = (cur.tank_i - 1) % (len(self.players) + 1)
            if cur.tank_i < 0 or cur.tank_i >= len(self.players) or len(self.players) == 0:
                self.controllers[cur.controller_i].player = None
            else:
                self.controllers[cur.controller_i].player = self.players[cur.tank_i]
                self.controllers[cur.controller_i].mode = Controller.Mode.BOTH
        elif cur.controller.btns_d[Controller.Buttons.RIGHT]:
            cur.tank_i = (cur.tank_i + 1) % (len(self.players) + 1)
            if cur.tank_i < 0 or cur.tank_i >= len(self.players) or len(self.players) == 0:
                self.controllers[cur.controller_i].player = None
            else:
                self.controllers[cur.controller_i].player = self.players[cur.tank_i]
                self.controllers[cur.controller_i].mode = Controller.Mode.BOTH

        # UD select controller
        elif cur.controller.btns_d[Controller.Buttons.UP]:
            cur.controller_i = (cur.controller_i - 1) % len(self.controllers)
            cur.tank_i = -1
            if self.controllers[cur.controller_i].player is not None:
                for i in range(len(self.players)):
                    if self.players[i] == self.controllers[cur.controller_i].player:
                        cur.tank_i = i
                        break

        elif cur.controller.btns_d[Controller.Buttons.DOWN]:
            cur.controller_i = (cur.controller_i + 1) % len(self.controllers)
            cur.tank_i = -1
            if self.controllers[cur.controller_i].player is not None:
                for i in range(len(self.players)):
                    if self.players[i] == self.controllers[cur.controller_i].player:
                        cur.tank_i = i
                        break

        # A change tank mode
        elif cur.controller.btns_d[Controller.Buttons.A]:
            if self.controllers[cur.controller_i].player is not None:
                old_mode = self.controllers[cur.controller_i].mode
                if old_mode == Controller.Mode.BOTH:
                    self.controllers[cur.controller_i].mode = Controller.Mode.TANK
                elif old_mode == Controller.Mode.TANK:
                    self.controllers[cur.controller_i].mode = Controller.Mode.CANON
                else:
                    self.controllers[cur.controller_i].mode = Controller.Mode.BOTH


    def select_color(self, cur):
        # LR select tank - color
        if len(self.players) == 0:
            return
        cur.tank_i %= len(self.players)

        if cur.controller.btns_d[Controller.Buttons.LEFT]:
            cur.color_i -= 1
            if cur.color_i < 0:
                cur.color_i = 2
                cur.tank_i = (cur.tank_i - 1) % len(self.players)
        elif cur.controller.btns_d[Controller.Buttons.RIGHT]:
            cur.color_i += 1
            if cur.color_i > 2:
                cur.color_i = 0
                cur.tank_i = (cur.tank_i + 1) % len(self.players)

        # UD select color
        elif cur.controller.btns_d[Controller.Buttons.UP]:
            if Controller.Mode.TANK in cur.color_t:
                color = list(self.players[cur.tank_i].t.color) 
                if color[cur.color_i] < 0xCC:
                    color[cur.color_i] += 0x11
                else:
                    color[cur.color_i] = 0xCC
                self.players[cur.tank_i].t.color = tuple(color)
            if Controller.Mode.CANON in cur.color_t:
                color = list(self.players[cur.tank_i].t.c.color) 
                if color[cur.color_i] < 0xCC:
                    color[cur.color_i] += 0x11
                else:
                    color[cur.color_i] = 0xCC
                self.players[cur.tank_i].t.c.color = tuple(color)

        elif cur.controller.btns_d[Controller.Buttons.DOWN]:
            if Controller.Mode.TANK in cur.color_t :
                color = list(self.players[cur.tank_i].t.color) 
                if color[cur.color_i] > 0x22:
                    color[cur.color_i] -= 0x11
                else:
                    color[cur.color_i] = 0x22
                self.players[cur.tank_i].t.color = tuple(color)
            if Controller.Mode.CANON in cur.color_t:
                color = list(self.players[cur.tank_i].t.c.color) 
                if color[cur.color_i] > 0x22:
                    color[cur.color_i] -= 0x11
                else:
                    color[cur.color_i] = 0x22
                self.players[cur.tank_i].t.c.color = tuple(color)

        # A change tank / canon
        elif cur.controller.btns_d[Controller.Buttons.A]:
            old_mode = cur.color_t
            if old_mode == Controller.Mode.BOTH:
                cur.color_t = Controller.Mode.TANK
            elif old_mode == Controller.Mode.TANK:
                cur.color_t = Controller.Mode.CANON
            else:
                cur.color_t = Controller.Mode.BOTH

    def start(self, cur):
        if cur.controller.btns_d[Controller.Buttons.A]:
            for p in self.data.players:
                p.reset()

            self.start_game = True

    def draw(self):

        self.engine.screen.fill("black")

        self.engine.text_print.reset()
        
        self.engine.text_print.tprint(self.engine.screen, "Tanks")
        self.engine.text_print.tprint(self.engine.screen, "")

        self.engine.text_print.tprint(self.engine.screen, f"  Controllers {len(self.controllers)}")
        for c in self.controllers:
            self.engine.text_print.tprint(self.engine.screen, f"  Controller {id(c)}: ")
            if c.player is not None:
                self.engine.text_print.tprint(self.engine.screen, f"    Player {id(c.player)} - {c.mode} {c.player.t.color} - {c.player.t.c.color}")
            else:
                self.engine.text_print.tprint(self.engine.screen, f"    Player None")

        self.engine.text_print.tprint(self.engine.screen, "")

        self.engine.text_print.tprint(self.engine.screen, f"  Cursors {len(self.cursors)}")
        i = 1
        for cur in self.cursors:
            self.engine.text_print.tprint(self.engine.screen, f"  Cursor {i}: {id(cur.controller)} - {cur.pos} - {cur.controller_i} - {cur.tank_i} - {cur.color_i}")
            i += 1

        self.engine.text_print.tprint(self.engine.screen, "")

        self.engine.text_print.tprint(self.engine.screen, f"  Players {len(self.players)}")
        for p in self.players:
            self.engine.text_print.tprint(self.engine.screen, f"    Player {id(p)} - {p.t.color} - {p.t.c.color}")

    def run(self):
        # Check nav actions
        i = 0
        while i < len(self.cursors):
            cur = self.cursors[i]
            if self.flow[cur.pos].act is not None:
                # Run current pos if
                self.flow[cur.pos].act(cur)

            if cur.controller.btns_d[Controller.Buttons.LEFT]:
                if self.flow[cur.pos].left is not None:
                    cur.pos = self.flow[cur.pos].left
            elif cur.controller.btns_d[Controller.Buttons.RIGHT]:
                if self.flow[cur.pos].right is not None:
                    cur.pos = self.flow[cur.pos].right
            elif cur.controller.btns_d[Controller.Buttons.A]:
                if self.flow[cur.pos].a is not None:
                    cur.pos = self.flow[cur.pos].a
            elif cur.controller.btns_d[Controller.Buttons.B]:
                if self.flow[cur.pos].b is not None:
                    cur.pos = self.flow[cur.pos].b
                else:
                    del self.cursors[i]
                    i -= 1
            i += 1

        # Check for new controllers
        for c in self.controllers:
            if c.btns_d[Controller.Buttons.A]:
                if len([cur for cur in self.cursors if c == cur.controller]) == 0:
                    self.cursors.append(self.Cursor(c))

        self.draw()

        if self.start_game:
            return self.data.State.GAME
        return self.data.State.MENU
