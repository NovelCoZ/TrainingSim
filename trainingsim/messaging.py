from abc import ABCMeta, abstractmethod
from typing import Deque, List


class MessageManagementSystem:
    __metaclass__ = ABCMeta

    messages: Deque
    agents: []

    def __init__(self):
        pass

    @abstractmethod
    def add_message(self, message):
        pass

    @abstractmethod
    def send_all(self):
        pass


class Social:
    __metaclass__ = ABCMeta

    messages: Deque
    messenger: MessageManagementSystem

    def __init__(self):
        pass

    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def send_all(self):
        pass
