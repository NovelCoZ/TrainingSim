from renderers.renderer import Renderable, BaseRenderer
from builtin.entity2d import CircleEntity
import pygame


class Renderer(BaseRenderer):

    def __init__(self, width, height, screen=None):
        super().__init__()
        pygame.init()
        self.width = int(round(width))
        self.height = int(round(height))
        if screen is None:
            self.screen = pygame.display.set_mode((self.width, self.height))
        else:
            self.screen = screen

    def render(self, env):
        events = pygame.event.get()
        self.screen.fill((255, 255, 255))
        for entity in env.entities:
            if isinstance(entity, Renderable):
                entity.render()

        pygame.display.update()

    def get_display(self):
        return self.screen


class CircleRenderer(BaseRenderer):

    def __init__(self, width, height, color, screen):
        super().__init__()
        self.width = int(round(width))
        self.height = int(round(height))
        self.color = color
        self.screen = screen

    def render(self, entity):
        if isinstance(entity, CircleEntity):
            pygame.draw.circle(self.screen, self.color, entity.position, entity.r)


class PredatorRenderer(CircleRenderer):

    def __init__(self, width, height, screen):
        super().__init__(width, height, (255, 0, 0), screen)


class PreyRenderer(CircleRenderer):

    def __init__(self, width, height, screen):
        super().__init__(width, height, (0, 0, 255), screen)


# GridWorld renderers
class GridCircleRenderer(BaseRenderer):

    def __init__(self, width: int, height: int, sz: int, color, screen):
        super().__init__()
        self.width = width
        self.height = height
        self.sz = sz
        self.color = color
        self.screen = screen

    def render(self, entity):
        x, y = entity.position
        x = self.sz * x + self.sz // 2
        y = self.sz * y + self.sz // 2
        pygame.draw.circle(self.screen, self.color, (x, y), self.sz // 2 - 1)


class DirtRenderer(GridCircleRenderer):

    def __init__(self, width: int, height: int, sz: int, screen):
        super().__init__(width, height, sz, (110, 72, 15), screen)


class CleanerRenderer(GridCircleRenderer):

    def __init__(self, width: int, height: int, sz: int, screen):
        super().__init__(width, height, sz, (37, 134, 156), screen)


class WallRenderer(BaseRenderer):

    def __init__(self, width: int, height: int, sz: int, screen):
        super().__init__()
        self.width = width
        self.height = height
        self.sz = sz
        self.color = (171, 161, 145)
        self.screen = screen

    def render(self, entity):
        x, y = entity.position
        x = self.sz * x
        y = self.sz * y
        pygame.draw.rect(self.screen, self.color, pygame.Rect(x, y, self.sz, self.sz), width=0)


class GridRenderer(BaseRenderer):

    def __init__(self, width: int, height: int, sz: int, screen=None):
        super().__init__()
        pygame.init()
        self.width = width
        self.height = height
        self.sz = sz
        if screen is None:
            self.screen = pygame.display.set_mode((self.width * sz, self.height * sz))
        else:
            self.screen = screen

    def render(self, env):
        events = pygame.event.get()
        self.screen.fill((47, 27, 66, 25))

        for entity in env.entities:
            if isinstance(entity, Renderable):
                entity.render()
        for agent in env.agents:
            if isinstance(agent, Renderable):
                agent.render()

        for i in range(self.width + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (i * self.sz, 0), (i * self.sz, self.height * self.sz), 1)
        for i in range(self.height + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (0, i * self.sz), (self.width * self.sz, i * self.sz), 1)

        pygame.display.update()

    def get_display(self):
        return self.screen
