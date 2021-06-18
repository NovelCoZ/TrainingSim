from trainingsim.environment import Environment
from trainingsim.agent import Agent
from renderers.renderer import Renderable
from renderers.pygame_renderer import Renderer
from builtin.entity2d import Entity2d


class Environment2d(Environment, Renderable):

    width: int
    height: int

    def __init__(self, width, height, screen=None, renderer=None):
        Environment.__init__(self)
        if renderer is None:
            self.renderer = Renderer(width, height, screen)
        else:
            Renderable.__init__(self, renderer)
        self.seed = 0
        self.width = width
        self.height = height

    def reset(self):
        self.entities.clear()
        self.agents.clear()

    def step(self):
        pass

    def render(self):
        self.renderer.render(self)

    def register_agent(self, agent: Agent):
        self.agents.append(agent)

    def register_entity(self, entity):
        self.entities.append(entity)

    def remove_agent(self, agent: Agent):
        self.agents.remove(agent)

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def seed(self, seed=None):
        if seed is not None:
            self.seed = seed
        return self.seed

    def close(self):
        pass

