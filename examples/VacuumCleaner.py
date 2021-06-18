import time

import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, models, optimizers, losses
from builtin.environment2d import *
from builtin.entity2d import *
from trainingsim.environment import *
from trainingsim.agent import *
from renderers.pygame_renderer import *
from examples.agents import *


class SensorHandle:

    def __init__(self, sensors: [Sensor], env: Environment):
        self.sensors = sensors
        self.env = env

    def handle(self):
        for sensor in self.sensors:
            sensor.observe(self.env.state())

    def add_sensor(self, sensor):
        self.sensors.append(sensor)


class VacuumCleanerEnv(Environment2d, FullyObservable, Static, Reinforcing):

    class Dirt(GridEntity2d, Renderable):

        def __init__(self, x, y, renderer):
            GridEntity2d.__init__(self, x, y)
            Renderable.__init__(self, renderer)

        def render(self):
            self.renderer.render(self)

    class Wall(GridEntity2d, Renderable):
        def __init__(self, x, y, renderer):
            GridEntity2d.__init__(self, x, y)
            Renderable.__init__(self, renderer)

        def render(self):
            self.renderer.render(self)

    def __init__(self, width, height, sz):
        Environment2d.__init__(self, width, height, renderer=GridRenderer(width, height, sz))
        FullyObservable.__init__(self)
        Static.__init__(self)
        Reinforcing.__init__(self)
        self.sensory_handler = SensorHandle([], self)

    def add_walls(self, num):
        wall_renderer = WallRenderer(self.width, self.height, self.renderer.sz, self.renderer.get_display())
        for i in range(self.width - 1):
            wall = self.Wall(i, 0, wall_renderer)
            self.register_entity(wall)
            wall = self.Wall(i, self.height - 1, wall_renderer)
            self.register_entity(wall)
        for i in range(self.height):
            wall = self.Wall(0, i, wall_renderer)
            self.register_entity(wall)
            wall = self.Wall(self.width - 1, i, wall_renderer)
            self.register_entity(wall)
        for _ in range(num):
            x, y = np.random.randint(0, self.width), np.random.randint(0, self.height)
            while self.entity_at(x, y) is not None:
                x, y = np.random.randint(0, self.width), np.random.randint(0, self.height)
            wall = self.Wall(x, y, wall_renderer)
            self.register_entity(wall)

    def add_dirt(self, num):
        dirt_renderer = DirtRenderer(self.width, self.height, self.renderer.sz, self.renderer.get_display())
        for _ in range(num):
            x, y = np.random.randint(0, self.width), np.random.randint(0, self.height)
            while self.entity_at(x, y) is not None:
                x, y = np.random.randint(0, self.width), np.random.randint(0, self.height)
            dirt = self.Dirt(x, y, dirt_renderer)
            self.register_entity(dirt)

    def add_cleaner(self, cleaner):
        self.register_agent(cleaner)

    def wall_at(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        ent = self.entity_at(x, y)
        if ent is not None and isinstance(ent, self.Wall):
            return True
        return False

    def entity_at(self, x, y):
        for entity in self.entities:
            if entity.position[0] == x and entity.position[1] == y:
                return entity
        for agent in self.agents:
            if agent.position[0] == x and agent.position[1] == y:
                return agent
        return None

    def clean(self):
        for entity in self.entities:
            if isinstance(entity, self.Dirt):
                return False
        return True

    def step(self):
        agent, action = self.get_actions()
        b = True
        if action == 'up':
            if not self.wall_at(agent.position[0], agent.position[1] - 1):
                agent.move(0, -1)
                b = False
        if action == 'down':
            if not self.wall_at(agent.position[0], agent.position[1] + 1):
                agent.move(0, 1)
                b = False
        if action == 'left':
            if not self.wall_at(agent.position[0] - 1, agent.position[1]):
                agent.move(-1, 0)
                b = False
        if action == 'right':
            if not self.wall_at(agent.position[0] + 1, agent.position[1]):
                agent.move(1, 0)
                b = False
        ent = self.entity_at(agent.position[0], agent.position[1])
        if ent is not None and isinstance(ent, self.Dirt):
            self.remove_entity(ent)
            self.send_reward(0.9, self.agents[0])
        else:
            self.send_reward(-0.1 if b is False else -0.2, self.agents[0])

        return self.clean()

    def reset(self):
        self.entities.clear()
        self.agents[0].position = (1, 1)
        self.add_walls(np.random.randint(5, 10))
        self.add_dirt(np.random.randint(10, 30))

    def state(self):
        state = []
        for entity in self.entities:
            entity_type = ''
            if isinstance(entity, self.Dirt):
                entity_type = 'dirt'
            if isinstance(entity, self.Wall):
                entity_type = 'wall'
            state.append((entity_type, entity.position[0], entity.position[1]))
        state.append(('cleaner', self.agents[0].position[0], self.agents[0].position[1]))
        return state

    def get_actions(self):
        agent = []
        for cleaner in self.agents:
            agent = cleaner
        actions = ['up', 'down', 'left', 'right']
        action = agent.program()
        return agent, action

    def send_reward(self, reward, agent):
        agent.behavior.add_reward(reward)


env = VacuumCleanerEnv(10, 10, 40)

sensor_handle = SensorHandle([], env)

cleaner_renderer = CleanerRenderer(env.width, env.height, env.renderer.sz, env.renderer.get_display())
cleaner = VacuumCleaner(WorldSensor([], []),
                        VacuumCleanerBehavior([], []),
                        MotionActuator([], [], env),
                        cleaner_renderer, 0, 0)

cleaner.sensor.add_output(cleaner.behavior)
cleaner.behavior.add_input(cleaner.sensor)
cleaner.actuator.add_input(cleaner.behavior)
cleaner.behavior.add_output(cleaner.actuator)

sensor_handle.add_sensor(cleaner.sensor)

env.add_cleaner(cleaner)

epochs = 1000
max_episodes = 100

for epoch in range(epochs):
    env.reset()
    done = False
    episodes = 0

    while not done and episodes < max_episodes:
        sensor_handle.handle()
        done = env.step()
        if epoch % 2 == 0:
            env.render()
            time.sleep(0.1)
        episodes += 1

    cleaner.behavior.train([])
    if epoch % 10 == 0:
        cleaner.behavior.save_model("trained_model_ep" + epoch.__str__() + ".h5")






