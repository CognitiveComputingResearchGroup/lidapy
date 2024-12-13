import gymnasium as gym

class CliffWalkingEnv:
    def __init__(self, env_name= 'CliffWalking-v0'):
        self.env_name = env_name
        self.env = gym.make(env_name, render_mode = 'human')
        self.reset_environment()

    def reset_environment(self):
        self.state, _ = self.env.reset()
        return self.state

    def step(self, action):
        next_state,reward,done, _, info = self.env.step(action)
        return next_state, reward, done, info

    def render(self):
        self.env.render()

    def close(self):
        self.env.close()


if __name__ == '__main__':
    cliff_env = CliffWalkingEnv()
    cliff_env.render()

    done = False
    while not done:
        action = cliff_env.env.action_space.sample()

        next_state, reward, done, info = cliff_env.step(action)
        cliff_env.render()

    cliff_env.close()