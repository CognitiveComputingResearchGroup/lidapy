#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from source.ActionSelection.ActionSelection import ActionSelection
from source.ActionSelection.Initialization.ConcreteActionSelectionFactory import \
    ConcreteActionSelectionFactory
from source.Environment.CliffWalkingEnvironment import CliffWalkingEnvironment
from source.Environment.Initialization.ConcreteEnvironmentFactory import \
    ConcreteEnvironmentFactory
from source.Framework.Agents.CliffWalkingAgent import CliffWalkingAgent
from source.Framework.Initialization.ConcreteAgentFactory import ConcreteAgentFactory
from source.PAM.CliffWalkingPAM import CliffWalkingPAM
from source.PAM.Initialization.ConcretePAMFactory import PAMConcreteFactory
from source.ProceduralMemory.Initialization.ConcreteProceduralMemoryFactory import \
    ConcreteProceduralMemoryFactory
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory
from source.SensoryMemory.CliffWalkingSensoryMemory import CliffWalkingSensoryMem
from source.SensoryMemory.Initialization.ConcreteSensoryMemoryFactory import \
    ConcreteSensoryMemoryFactory
from source.SensoryMotorMemory.Initialization.ConcreteSensoryMotorMemoryFactory import \
    ConcreteSensoryMotorMemoryFactory
from source.SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl


if __name__ == "__main__":
    # Create agent factory and initialize agent
    agent_factory = ConcreteAgentFactory()
    agent = agent_factory.get_agent(CliffWalkingAgent())

    # Create environment factory
    environment_factory = ConcreteEnvironmentFactory()

    #Initialize FrozenLake environment
    cliff_walking_environment = (environment_factory.
                               create_environment(CliffWalkingEnvironment()))
    # Add the environment module to the agent
    agent.add_module("CliffWalkingEnvironment", cliff_walking_environment)

    # Create Sensory Motor Memory factory
    sensory_memory_factory = ConcreteSensoryMotorMemoryFactory()

    # Instantiate Sensory Motor Memory Module
    sensory_motor_memory = sensory_memory_factory.create_sensory_motor(
        SensoryMotorMemoryImpl(agent.get_module("CliffWalkingEnvironment"),
                               agent))
    # Add Sensory Motor Memory module
    agent.add_module("SensoryMotorMemoryImpl", sensory_motor_memory)

    # Create action selection factory
    action_selection_factory = ConcreteActionSelectionFactory()

    # Instantiate action_selection module
    action_selection = action_selection_factory.create_action_selection(
        ActionSelection(
        agent.get_module("CliffWalkingEnvironment"),
        agent.get_module("SensoryMotorMemoryImpl")))

    # Add the Action Selection Module
    agent.add_module("ActionSelection", action_selection)

    # Create Procedural Memory Factory
    procedural_memory_factory = ConcreteProceduralMemoryFactory()

    #Instantiate Procedural Memory Factory
    procedural_memory = procedural_memory_factory.create_procedural_memory(
        ProceduralMemory(agent.get_module("ActionSelection")))
    # Add Procedural Memory
    agent.add_module("ProceduralMemory", procedural_memory)

    # Create PAM factory
    pam_factory = PAMConcreteFactory()

    # Instantiate PAM module
    PAM = pam_factory.create_pam(CliffWalkingPAM(
                         agent.get_module("ProceduralMemory")))
    # Add PAM Module
    agent.add_module("PerceptualAssociativeMemory", PAM)

    # Create sensory memory factory
    sensory_mem_factory = ConcreteSensoryMemoryFactory()

    # Initialize sensory memory module
    SensoryMemory = sensory_mem_factory.create_sensory_memory(
    CliffWalkingSensoryMem(agent.get_module("CliffWalkingEnvironment"),
                     agent.get_module("PerceptualAssociativeMemory"), agent))

    # Add the Sensory Memory module
    agent.add_module("CliffWalkingSensoryMemory", SensoryMemory)

    #Add attributes relevant to this agent
    agent.add_attribute("state", None)
    agent.add_attribute("action", None)
    agent.add_attribute("reward", None)
    agent.add_attribute("done", False)
    agent.add_attribute("info", None)
    agent.add_attribute("truncated", False)
    agent.add_attribute("surrounding_tiles", None)
    agent.add_attribute("col", None)
    agent.add_attribute("row", None)

    #Start the agent
    agent.run()