""" base classes for agent"""
from typing import List
from abc import ABCMeta, abstractmethod


class Agent:
    __metaclass__ = ABCMeta

    input_connections: List
    output_connections: List

    def __init__(self, input_connections: List, output_connections: List):
        self.input_connections = input_connections
        self.output_connections = output_connections

    @abstractmethod
    def program(self):
        pass

    @abstractmethod
    def add_input(self, connect):
        pass

    @abstractmethod
    def add_output(self, connect):
        pass


class Actuator(Agent):
    __metaclass__ = ABCMeta

    def __init__(self, input_connections: List, output_connections: List):
        super().__init__(input_connections, output_connections)

    @abstractmethod
    def act(self, signal):
        pass

    def add_input(self, connect):
        self.input_connections.append(connect)

    def add_output(self, connect):
        self.output_connections.append(connect)


class Sensor(Agent):
    __metaclass__ = ABCMeta

    def __init__(self, input_connections: List, output_connections: List):
        super().__init__(input_connections, output_connections)

    @abstractmethod
    def observe(self, response):
        pass

    def add_input(self, connect):
        self.input_connections.append(connect)

    def add_output(self, connect):
        self.output_connections.append(connect)


class Behavior(Agent):
    __metaclass__ = ABCMeta

    def __init__(self, input_connections: List, output_connections: List):
        super().__init__(input_connections, output_connections)
        self.inner_parameters = []

    @abstractmethod
    def train(self, batch):
        pass

    def add_input(self, connect):
        self.input_connections.append(connect)

    def add_output(self, connect):
        self.output_connections.append(connect)

