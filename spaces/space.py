""" base class for space """
from trainingsim.spaces import Space
import numpy as np


class Discrete(Space):

    n: int

    def __init__(self, n):
        super().__init__()
        self.n = n

    def sample(self):
        return np.random.choice(np.array(0, self.n))

    def contains(self, x):
        return 0 < x < self.n
