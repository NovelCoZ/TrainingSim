import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, models, optimizers, losses
from builtin.entity2d import *
from trainingsim.environment import *
from trainingsim.agent import *
from renderers.pygame_renderer import *


class SimpleSensor(Sensor):

    def __init__(self, input_connections: List, output_connections: List):
        super().__init__(input_connections, output_connections)
        self.observation = []

    def program(self):
        pass

    def observe(self, response):
        pass

    def add_input(self, connect):
        self.input_connections.append(connect)

    def add_output(self, connect):
        self.output_connections.append(connect)


class WorldSensor(SimpleSensor):

    def __init__(self, input_connections: List, output_connections: List):
        super().__init__(input_connections, output_connections)
        self.observation = []

    def program(self):
        return self.observation

    def observe(self, response):
        ret = np.zeros((10, 10), dtype='int')
        for observation in response:
            ind = 1  # observation[0] == dirt
            if observation[0] == 'wall':
                ind = 2
            if observation[0] == 'cleaner':
                ind = 3
            ret[observation[1]][observation[2]] = ind
        self.observation = ret


class MotionActuator(Actuator):

    def __init__(self, input_connections: List, output_connections: List, env):
        super().__init__(input_connections, output_connections)
        self.action = None
        self.env = env

    def act(self, signal):
        actions = ['up', 'down', 'left', 'right']
        self.action = actions[signal]
        return self.action

    def program(self):
        self.env.set_action(self.action)


class VacuumCleanerBehavior(Behavior):

    def __init__(self, input_connections: List, output_connections: List):
        super().__init__(input_connections, output_connections)

        inputs = layers.Input(shape=(10, 10, 1,))
        common = layers.Conv2D(10, (3, 3), activation='relu')(inputs)
        common = layers.MaxPooling2D((2, 2))(common)
        common = layers.Conv2D(20, (3, 3), activation='relu')(common)
        common = layers.MaxPooling2D((2, 2))(common)
        common = layers.Flatten()(common)
        common = layers.Dense(16, activation='relu')(common)
        action = layers.Dense(4, activation='softmax')(common)
        critic = layers.Dense(1)(common)
        model = models.Model(inputs=inputs, outputs=[action, critic])

        self.optimizer = optimizers.Adam(learning_rate=0.01)
        self.huber_loss = losses.Huber()
        self.action_probs_history = []
        self.critic_value_history = []
        self.rewards_history = []
        self.running_reward = 0
        self.episode_count = 0
        self.episode_reward = 0

        self.tape = tf.GradientTape()

        self.model = model

    def save_model(self, filename):
        self.model.save(filename)

    def load_model(self, filename):
        self.model = models.load_model(filename)

    def train(self, batch):
        with self.tape as tape:
            gamma = 0.99
            eps = np.finfo(np.float32).eps.item()

            # Calculate expected value from rewards
            # - At each timestep what was the total reward received after that timestep
            # - Rewards in the past are discounted by multiplying them with gamma
            # - These are the labels for our critic
            returns = []
            discounted_sum = 0
            for r in self.rewards_history[::-1]:
                discounted_sum = r + gamma * discounted_sum
                returns.insert(0, discounted_sum)

            # Normalize
            returns = np.array(returns)
            returns = (returns - np.mean(returns)) / (np.std(returns) + eps)
            returns = returns.tolist()


            # Calculating loss values to update our network
            history = zip(self.action_probs_history, self.critic_value_history, returns)
            actor_losses = []
            critic_losses = []

            for log_prob, value, ret in history:
                # At this point in history, the critic estimated that we would get a
                # total reward = `value` in the future. We took an action with log probability
                # of `log_prob` and ended up recieving a total reward = `ret`.
                # The actor must be updated so that it predicts an action that leads to
                # high rewards (compared to critic's estimate) with high probability.
                diff = ret - value
                actor_losses.append(-log_prob * diff)  # actor loss

                # The critic must be updated so that it predicts a better estimate of
                # the future rewards.
                critic_losses.append(
                    self.huber_loss(tf.expand_dims(value, 0), tf.expand_dims(ret, 0))
                )

            # Backpropagation
            loss_value = sum(actor_losses) + sum(critic_losses)

            grads = tape.gradient(loss_value, self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

            # Clear the loss and reward history
            self.action_probs_history.clear()
            self.critic_value_history.clear()
            self.rewards_history.clear()
            self.episode_reward = 0

    def program(self):
        with self.tape as tape:
            state = []
            for inp in self.input_connections:
                state = inp.program()

            # Predict action probabilities and estimated future rewards
            # from environment state
            state = tf.convert_to_tensor(state)
            state = tf.expand_dims(state, 0)

            action_probs, critic_value = self.model(state)
            self.critic_value_history.append(critic_value[0, 0])

            # Sample action from action probability distribution
            action = np.random.choice(4, p=np.squeeze(action_probs))
            self.action_probs_history.append(tf.math.log(action_probs[0, action]))

            for actuator in self.output_connections:
                actuator.act(action)

    def add_reward(self, reward):
        self.rewards_history.append(reward)
        self.episode_reward += reward

    def add_input(self, connect):
        self.input_connections.append(connect)

    def add_output(self, connect):
        self.output_connections.append(connect)


class VacuumCleaner(GridEntity2d, Agent, Renderable):

    def __init__(self, sensor: Sensor, behavior: Behavior, actuator: Actuator, renderer, x: int, y: int):
        GridEntity2d.__init__(self, x, y)
        Renderable.__init__(self, renderer)
        Agent.__init__(self, [sensor], [actuator])
        self.sensor = sensor
        self.behavior = behavior
        self.actuator = actuator

    def program(self):
        self.behavior.program()
        return self.actuator.action

    def get_reward(self, reward):
        self.behavior.add_reward(reward)

    def add_input(self, connect):
        pass

    def add_output(self, connect):
        pass

    def render(self):
        self.renderer.render(self)

