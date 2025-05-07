import time
from time import sleep

from source.AttentionCodelets.AttentionCodelet import AttentionCodelet
from source.Framework.Tasks.TaskManager import TaskManager
from source.GlobalWorkspace.CoalitionImpl import CoalitionImpl
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.Workspace.CurrentSituationalModel.CurrentSituationalModelImpl import \
    CurrentSituationalModelImpl

DEFAULT_CODELET_REFRACTORY_PERIOD = 50
DEFAULT_CODELET_REINFORCEMENT = 0.5
DEFAULT_CODELET_REMOVAL_THRESHOLD = -1.0
DEFAULT_CODELET_ACTIVATION = 1.0

class AttentionCodeletImpl(AttentionCodelet):
    def __init__(self):
        super().__init__()
        self.buffer = None
        self.global_workspace = None
        self.codeletRefractoryPeriod = DEFAULT_CODELET_REFRACTORY_PERIOD
        self.formed_coalition = None
        self.codelet_reinforcement = DEFAULT_CODELET_REINFORCEMENT
        self.removal_threshold = DEFAULT_CODELET_REMOVAL_THRESHOLD
        self.activation = DEFAULT_CODELET_ACTIVATION
        self.tick_at_last_coalition = 0.0
        self.task_manager = TaskManager()


    def start(self):
        self.logger.debug("Initialized new attention codelets")
        self.run_task()
        if not self.task_manager.shutdown:
            self.task_manager.run()

    def run_task(self):
        if self.bufferContainsSoughtContent(self.buffer):
            csm_content = self.retrieveWorkspaceContent(
                                    self.buffer)
            if csm_content is None:
                self.logger.warning("Null WorkspaceContent returned."
                                          "Coalition cannot be formed.")
            elif csm_content.getLinkableCount() > 0:
                if not self.task_manager.shutdown:
                    self.formed_coalition = CoalitionImpl()
                    self.formed_coalition.setContent(csm_content)
                    self.formed_coalition.setCreatingAttentionCodelet(self)
                    self.formed_coalition.setActivation(DEFAULT_CODELET_ACTIVATION)
                    self.tick_at_last_coalition = (
                    self.task_manager.getCurrentTick())
                    self.logger.debug("Coalition successfully formed.")
                    self.decay(1.0)
                    self.notify_observers()
                    if not self.isRemovable():
                        if not (self.task_manager.getCurrentTick() -
                            self.tick_at_last_coalition >=
                            self.codelet_reinforcement):
                            sleep(self.codelet_reinforcement)
                            self.run_task()
            else:
                while (csm_content.getLinkableCount() == 0 and not
                self.task_manager.shutdown):
                    time.sleep(10)
                if not self.task_manager.shutdown:
                    self.run_task()

    def set_refactory_period(self, ticks):
        if ticks > 0:
            self.codeletRefractoryPeriod = ticks
        else:
            self.codeletRefractoryPeriod =  (
                DEFAULT_CODELET_REFRACTORY_PERIOD)

    def get_refactory_period(self):
        return self.codeletRefractoryPeriod

    def learn(self, coalition):
        coalition_codelet = None
        if isinstance(coalition, CoalitionImpl):
            coalition_codelet = coalition.getCreatingAttentionCodelet()
        if isinstance (coalition_codelet, AttentionCodelet):
            new_codelet = AttentionCodeletImpl()
            for observer in self.observers:
                new_codelet.add_observer(observer)
            new_codelet.buffer = self.buffer
            content = coalition.getContent()
            new_codelet.setSoughtContent(content)
            self.task_manager.shutdown = True
            self.decay(1.0)
            self.logger.info(f"Created new codelet: {new_codelet}")
            sleep(3)
            new_codelet.start()
        elif coalition_codelet is not None:
    # TODO Reinforcement amount might be a function of the broadcast's
    # activation
            coalition_codelet.reinforceBaseLevelActivation(
                self.codelet_reinforcement)
            self.logger.debug(f"Reinforcing codelet: {coalition_codelet}")

    def getModuleContent(self):
        return self.formed_coalition

    def bufferContainsSoughtContent(self, buffer):
        if isinstance(buffer, CurrentSituationalModelImpl):
            if buffer.getBufferContent() is not None:
                return True
        return False

    """
        Returns sought content and related content from specified
        WorkspaceBuffer
        """
    def retrieveWorkspaceContent(self, buffer):
        if isinstance(buffer, CurrentSituationalModelImpl):
            return buffer.getBufferContent()

    def notify(self, module):
        if isinstance(module, GlobalWorkSpaceImpl):
            if not self.isRemovable() and not self.task_manager.shutdown:
                winning_coalition = module.get_broadcast()
                self.logger.debug(f"Received conscious broadcast: "
                                f"{winning_coalition}")
                self.learn(winning_coalition)
            else:
                module.remove_observer(self)
