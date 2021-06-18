from builtin.environment2d import Environment2d
from builtin.entity2d import GridEntity2d
from trainingsim.environment import *
from trainingsim.agent import *
from trainingsim.spaces import Space


class PredatorActionSpace(Space):

    def sample(self):
        pass

    def contains(self, x):
        pass


class PredatorAndPreyEnv(Environment2d, PartiallyObservable, Dynamic, Reinforcing):

    def __init__(self, width, height, dt):
        Environment2d.__init__(self, width, height)
        PartiallyObservable.__init__(self)
        Dynamic.__init__(self, dt)
        Reinforcing.__init__(self)

    def step(self):
        self.send_observations()
        for action in self.actions:
            pass
        pass

    def send_observations(self):
        pass

    def send_reward(self, reward, agent):
        pass
