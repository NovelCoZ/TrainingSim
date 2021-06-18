"""base classes for environment"""
from abc import ABCMeta, abstractmethod
from typing import List

from trainingsim.agent import Agent


class Environment:
    __metaclass__ = ABCMeta

    agents: List[Agent]
    entities: List

    def __init__(self):
        self.agents = []
        self.entities = []
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def register_agent(self, agent: Agent):
        pass

    @abstractmethod
    def register_entity(self, entity):
        pass

    @abstractmethod
    def remove_agent(self, agent: Agent):
        pass

    @abstractmethod
    def remove_entity(self, entity):
        pass


class FullyObservable:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def state(self):
        pass


class PartiallyObservable:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def send_observations(self):
        pass


class Static:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_actions(self):
        pass


class Dynamic:
    __metaclass__ = ABCMeta

    actions: List
    dt: float
    current_time: float

    def __init__(self, dt):
        self.actions = []
        self.dt = dt
        self.current_time = 0.0
        pass


class Renderable:
    __metaclass__ = ABCMeta

    def __init__(self, renderer):
        self.renderer = renderer
        pass

    @abstractmethod
    def render(self):
        pass


class Reinforcing:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def send_reward(self, reward, agent):
        pass
