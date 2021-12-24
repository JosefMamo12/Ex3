import math
import os

import pygame

from src.GraphAlgo import GraphAlgo
from src.Gui.Range import Range
from src.Gui.Range2D import Range2D
from src.Gui.Range2Range import Range2Range
from src.NodeData import NodeData


def init(g: GraphAlgo):
    gui = GraphDraw(g)
    gui.run_gui()


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


class GraphDraw:

    def __init__(self, g: GraphAlgo):
        self.g = g
        self.range: Range2Range

    def run_gui(self):
        pygame.init()
        clock = pygame.time.Clock()
        fps = 60
        pygame.display.set_caption('Graph')
        width, height = 1000, 700
        window = pygame.display.set_mode((width, height))
        window.fill((255, 255, 255))
        self.draw_graph(window, width, height)
        run = True
        while run:
            clock.tick(20)
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    run = False
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if CONNECTED.isOver(pos):
                #         print(self.g.connected())


                # CONNECTED.draw(self.WIN)
                pygame.display.flip()
        del window
        pygame.quit()


    def draw_graph(self, window, width, height) -> None:
        self.resize(width, height)
        for node in self.g.get_graph().get_all_v():
            for edge in self.g.get_graph().all_out_edges_of_node(node):
                self.draw_edge(window, self.g.get_graph().get_node(node), self.g.get_graph().get_node(edge))
        for node in self.g.get_graph().get_all_v().values():
            self.draw_node(window, node)

    def resize(self, width, height):
        rx = Range(50, width - 300)
        ry = Range(height - 200, 45)
        frame = Range2D(rx, ry)
        self.range = Range2Range(self.graph_range(), frame)

    def graph_range(self) -> Range2D:
        x0, x1, y0, y1 = 0, 0, 0, 0
        first = True
        for node in self.g.get_graph().get_all_v().values():
            pos = node.get_pos()
            if first:
                x0 = pos[0]
                x1 = x0
                y0 = pos[1]
                y1 = y0
                first = False
            else:
                if pos[0] < x0:
                    x0 = pos[0]
                if pos[0] > x1:
                    x1 = pos[0]
                if pos[1] < y0:
                    y0 = pos[1]
                if pos[1] > y1:
                    y1 = pos[1]

        xr = Range(x0, x1)
        yr = Range(y0, y1)
        return Range2D(xr, yr)

    def draw_edge(self, window, src: NodeData, dest: NodeData):
        src_pos, dest_pos = src.get_pos(), dest.get_pos()
        src_pos_loc, dest_pos_loc = self.range.world2frame(src_pos), self.range.world2frame(dest_pos)

        x1, x2, y1, y2 = int(src_pos_loc[0]), int(dest_pos_loc[0]), int(src_pos_loc[1]), int(dest_pos_loc[1])
        start, end = (x1, y1), (x2, y2)

        pygame.draw.line(window, (155, 0, 155), start, end, 3)
        self.draw_arrow(window, start, end)

    def draw_node(self, window, node: NodeData):
        pos = node.get_pos()
        FONT = pygame.font.SysFont('MV Boli', 30)
        NODE_IMAGE = pygame.image.load(os.path.join('resources/new.png'))
        label = FONT.render(str(node.get_key()), 1, (0, 0, 0))
        frame_pos = self.range.world2frame(pos)
        window.blit(label, (int(frame_pos[0]), int(frame_pos[1]) - 50))
        window.blit(NODE_IMAGE, (int(frame_pos[0] - 10), int(frame_pos[1]) - 15))

    def draw_arrow(self, window, start, end):
        rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
        pygame.draw.polygon(window, (255, 0, 0), (
            (end[0] + 5 * math.sin(math.radians(rotation)), end[1] + 5 * math.cos(math.radians(rotation))),
            (end[0] + 5 * math.sin(math.radians(rotation - 120)),
             end[1] + 5 * math.cos(math.radians(rotation - 120))),
            (end[0] + 5 * math.sin(math.radians(rotation + 120)),
             end[1] + 5 * math.cos(math.radians(rotation + 120)))))
