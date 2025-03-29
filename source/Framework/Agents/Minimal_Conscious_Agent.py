import importlib
import Configs
from importlib import util
from threading import Thread
from yaml import YAMLError, safe_load
from source.ActionSelection.ActionSelectionImpl import ActionSelectionImpl
from source.AttentionCodelets.AttentionCodeletImpl import AttentionCodeletImpl
from source.Environment.Environment import Environment
from source.Environment.FrozenLakeEnvironment import FrozenLake
from source.Framework.Agents.Agent import Agent
from source.Framework.Shared.NodeStructure import NodeStructure
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl
from source.Workspace.CurrentSituationModel.CurrentSituationModelImpl import \
    CurrentSituationalModelImpl
from source.Workspace.WorkspaceImpl import WorkspaceImpl


class MinimalConsciousAgent(Agent):
    def __init__(self):
        super().__init__()
        self.sensor_module = self.load_sensors_from_file("Sensors")
        self.sensors = self.get_agent_sensors()
        self.processor_dict = self.get_agent_processors()

        self.global_workspace = GlobalWorkSpaceImpl()
        self.csm = CurrentSituationalModelImpl()
        self.attention_codelets = AttentionCodeletImpl(self.csm,
                                                       self.global_workspace)
        self.environment = FrozenLake(self, self.attention_codelets)
        self.sensory_motor_mem = SensoryMotorMemoryImpl(self.environment)
        self.action_selection = ActionSelectionImpl(self.sensory_motor_mem)
        self.procedural_memory = ProceduralMemoryImpl(self.action_selection,
                                                      self.environment)
        self.pam = PAMImpl(self.procedural_memory)
        self.workspace = WorkspaceImpl(self.csm, self.pam)
        self.sensory_memory = SensoryMemoryImpl(None,self.pam,
                                                None,
                                                self.workspace,
                                                self.processor_dict,
                                                self.sensors,
                                                self.sensor_module)

        #Add observers
        self.add_observer(self.sensory_memory)

        #Agent thread
        self.agent_thread = Thread(target=self.environment.reset)

        #Attention Codelets thread
        self.attention_codelets_thread = (
                            Thread(target=self.attention_codelets.run_task))

        self.action_value = {
            "3": "up",
            "2": "right",
            "1": "down",
            "0": "left",
        }

    def run(self):
        self.agent_thread.start()
        sought_content = NodeStructure()
        sought_content.addNode("safe", 1.0, 0.0)
        sought_content.addNode("start", 1.0, 0.0)
        sought_content.addNode("goal", 2.0, -1.0)
        sought_content.addNode("danger", -1.0, 0.5)
        self.attention_codelets.setSoughtContent(NodeStructure())
        self.attention_codelets_thread.start()

    def notify(self, module):
        if isinstance(module, Environment):
            self.notify_observers()

    def load_sensors_from_file(self, type):
        with open(
                r'C:\Users\brian\Documents\Fall 2024\SWENG 480\lidapy'
                r'\Configs\module_locations.yaml', 'r') as yaml_file:
            try:
                loaded_module_locations = safe_load(yaml_file)
            except YAMLError as exc:
                print(exc)

        #Specify the module file path
        try:
            module_path = loaded_module_locations[type]
        except:
            raise KeyError(f"Invalid key \"{type}\"")
        #Name the module
        module_name = type

        #Load the module dynamically
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def get_agent_sensors(self):
        with open(r'C:\Users\brian\Documents\Fall 2024\SWENG 480\lidapy'
                r'\Configs\DEFAULT_PROCESSORS.yaml', 'r') as yaml_file:
            try:
                DEFAULT_SENSORS = safe_load(yaml_file)
            except YAMLError as exc:
                print(exc)
        return DEFAULT_SENSORS

    def get_agent_processors(self):
        with open(r'C:\Users\brian\Documents\Fall 2024\SWENG 480\lidapy'
                r'\Configs\DEFAULT_PROCESSORS.yaml', 'r') as yaml_file:
            try:
                DEFAULT_PROCESSORS = safe_load(yaml_file)
            except YAMLError as exc:
                print(exc)
        return DEFAULT_PROCESSORS

    def get_state(self):
        return self.environment.get_stimuli()