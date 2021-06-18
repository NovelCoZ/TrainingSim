from trainingsim.agent import Sensor
from builtin.entity2d import Entity2d


class DistanceSensor2d(Sensor, Entity2d):

    observation: float

    def __init__(self, input_connections=None, output_connections=None, x=0.0, y=0.0, orientation=0.0):
        Sensor.__init__(self, input_connections, output_connections)
        Entity2d.__init__(self, x, y, orientation)

    def observe(self, response):
        ret = 0
        for entity in response:
            ret = ((self.position[0] - entity.position[0]) ** 2 + (self.position[1] - entity.position[1]) ** 2) ** 0.5

        return ret

    def program(self):
        pass

    def add_input(self, connect):
        self.input_connections.append(connect)

    def add_output(self, connect):
        self.output_connections.append(connect)
