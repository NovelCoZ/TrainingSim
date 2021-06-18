""" base class for renderer """
from abc import ABCMeta, abstractmethod


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
