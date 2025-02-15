#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from source.Framework.Initialization.ConcreteAgentFactory import \
    ConcreteAgentFactory

class FrozenLakeAgent(ConcreteAgentFactory):
    def __init__(self):
        super().__init__()

    #Update Agent state attributes
    def notify(self, state, reward, done, truncated , info, action,
               surrounding_tiles):
        self.update_attribute("state", state)
        self.update_attribute("reward", reward)
        self.update_attribute("done", done)
        self.update_attribute("truncated", truncated)
        self.update_attribute("info", info)
        self.update_attribute("action", action)
        self.update_attribute("surrounding_tiles", surrounding_tiles)

    #Called when percept is 'danger' and no action taken
    def notify_(self, action):
        self.update_attribute("action", action)

    #Run the agent through the environment
    def run(self):
        env = self.get_module("FrozenLakeEnvironment")
        action_selection = self.get_module("ActionSelection")
        sensory_memory = self.get_module("SensoryMemory")
        procedural_memory = self.get_module("ProceduralMemory")
        sensory_motor_memory = self.get_module("SensoryMotorMemoryImpl")

        # Agents behavior logic
        while not self.get_attribute("done"):
            if self.get_attribute("state") is None:
                sensory_memory.run_sensors(self.get_attribute("state"),
                                           self.get_attribute("col"),
                                           self.get_attribute("row"), self)
                print(
                f"Initial Observation: State: {self.get_attribute("state")}"
                    f", Percept: {self.get_attribute("surrounding_tiles")}")
            else:
                self.update_attribute("col",
                                      env.get_attribute("col"))
                self.update_attribute("row",
                                      env.get_attribute("row"))
                sensory_memory.run_sensors(self.get_attribute("state"),
                                           self.get_attribute("col"),
                                           self.get_attribute("row"), self)

            print(f"Action: {self.get_attribute('action')}\n")
            print(f"State: {self.get_attribute('state')}, "
                  f"Reward: {self.get_attribute('reward')}, "
                  f"Done: {self.get_attribute('done')}, "
                  f"Info: {self.get_attribute('info')}")
            print(f"Surrounding Tiles: "
                  f"{self.get_attribute('surrounding_tiles')}")

        env.close()

