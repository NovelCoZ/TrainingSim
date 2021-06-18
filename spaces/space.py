""" base class for space """
from abc import ABCMeta, abstractmethod
import numpy as np


class Space:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def sample(self):
        pass

    @abstractmethod
    def contains(self, x):
        pass


class Discrete(Space):

    n: int

    def __init__(self, n):
        super().__init__()
        self.n = n

    def sample(self):
        return np.random.choice(np.array(0, self.n))

    def contains(self, x):
        return 0 < x < self.n
