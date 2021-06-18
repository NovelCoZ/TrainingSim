""" base class for renderer """
from abc import ABCMeta, abstractmethod


class BaseRenderer:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def render(self, env):
        pass


class Renderable:
    __metaclass__ = ABCMeta

    renderer: BaseRenderer

    def __init__(self, renderer):
        self.renderer = renderer
        pass

    @abstractmethod
    def render(self):
        pass

