from builtin.environment2d import Environment2d
from builtin.entity2d import CircleEntity
from builtin.sensor2d import DistanceSensor2d
from builtin.actuator2d import MotionActuator
from renderers.pygame_renderer import PredatorRenderer, PreyRenderer

env = Environment2d(700, 500)

env.reset()

done = False


def make_sample_agent():
    predator = PreyRenderer(env.width, env.height, env.renderer.get_display())
    entity = CircleEntity(10, 10, 50, renderer=predator)
    return entity


env.register_entity(make_sample_agent())

while not done:
    # observations = env.get_observations()
    # env.set_actions(observations)

    env.render()
    done = env.step()
