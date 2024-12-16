from src.Framework.Agents.Agent import Agent
from src.Framework.Initialization.AgentFactory import AgentFactory
from src.ActionSelection.ActionSelection import ActionSelection
from src.PAM.PAM import PerceptualAssociativeMemory
from src.SensoryMemory.SensoryMemory import SensoryMemory
from src.Environment.Environment import FrozenLakeEnvironment
from src.ProceduralMemory.ProceduralMemory import ProceduralMemory
from src.SensoryMotorMemory.SensoryMotorMemoryImpl import SensoryMotorMemoryImpl
#from MotorPlanExecution.MotorPlanExecution import MPExecution

class ConcreteAgentFactory(AgentFactory):
# concrete factory for creating and initializing agents

    def get_agent(self, agent_type):
        # create modules:
        env = FrozenLakeEnvironment(render_mode=agent_type.get("render_mode", "human"))
        pam = PerceptualAssociativeMemory()
        sensory_memory = SensoryMemory(env, pam)
        procedural_memory = ProceduralMemory()
        action_selection = ActionSelection(env.action_space, procedural_memory)
        #motor_plan_execution = MPExecution(env)
        sensory_motor_memory = SensoryMotorMemoryImpl(action_selection, env)

        # initialize the agent and add the modules:
        agent = Agent()
        agent.add_module("Environment", env)
        agent.add_module("PAM", pam)
        agent.add_module("SensoryMemory", sensory_memory)
        agent.add_module("ProceduralMemory", procedural_memory)
        agent.add_module("ActionSelection", action_selection)
        agent.add_module("SensoryMotorMemory", sensory_motor_memory)
        #agent.add_module("MotorPlanExecution", motor_plan_execution)

        return agent
