from trainingsim.agent import Actuator
from builtin.entity2d import Entity2d
from typing import List


class MotionActuator(Actuator, Entity2d):

    def __init__(self, input_connections: List, output_connections: List, x, y, orientation):
        Actuator.__init__(self, input_connections, output_connections)
        Entity2d.__init__(self, x, y, orientation)
        self.speed = 0

    def add_input(self, connect):
        self.input_connections.append(connect)

    def add_output(self, connect):
        self.output_connections.append(connect)

    def program(self):
        pass

    def act(self, signal):
        self.speed = signal
