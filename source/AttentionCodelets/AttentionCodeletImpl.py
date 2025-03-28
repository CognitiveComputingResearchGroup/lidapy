from source.AttentionCodelets.AttentionCodelet import AttentionCodelet
from source.Framework.Shared.NodeStructure import NodeStructure
from source.GlobalWorkspace.CoalitionImpl import CoalitionImpl
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.ModuleInitialization.DefaultLogger import getLogger
from source.Workspace.CurrentSituationModel.CurrentSituationModelImpl import \
    CurrentSituationalModelImpl
from source.Workspace.CurrentSituationModel.CurrentSituationalModel import \
    CurrentSituationalModel

DEFAULT_CODELET_REFRACTORY_PERIOD = 50
DEFAULT_CODELET_REINFORCEMENT = 0.5
DEFAULT_CODELET_REMOVAL_THRESHOLD = -1.0
DEFAULT_CODELET_ACTIVATION = 1.0

class AttentionCodeletImpl(AttentionCodelet):
    def __init__(self, current_situational_model, global_workspace):
        super().__init__(current_situational_model, global_workspace)
        self.buffer = current_situational_model
        self.global_workspace = global_workspace
        self.add_observer(current_situational_model)
        self.codeletRefractoryPeriod = DEFAULT_CODELET_REFRACTORY_PERIOD
        self.formed_coalition = None
        self.codelet_reinforcement = DEFAULT_CODELET_REINFORCEMENT
        self.logger = getLogger(self.__class__.__name__).logger

    def run_task(self):
        if self.bufferContainsSoughtContent(self.buffer):
            csm_content = self.retrieveWorkspaceContent(
                                    self.buffer)
            if csm_content is None:
                self.logger.warning("Null WorkspaceContent returned."
                                          "Coalition cannot be formed.")
            elif csm_content.getLinkableCount() > 0:
                formed_coalition = CoalitionImpl(csm_content, self)
                formed_coalition.setCreatingAttentionCodelet(self)
                self.notify_observers()
                self.logger.info("Coalition successfully formed.")

    def set_refactory_period(self, ticks):
        if ticks > 0:
            self.codeletRefractoryPeriod = ticks
        else:
            self.codeletRefractoryPeriod =  (
                DEFAULT_CODELET_REFRACTORY_PERIOD)

    def get_refactory_period(self):
        return self.codeletRefractoryPeriod

    def notify(self, module):
        if isinstance(module, GlobalWorkSpaceImpl):
            broadcast = module.getWinningCoalition()
            self.learn(broadcast)

    def learn(self, coalition):
        global coalition_codelet
        if isinstance(coalition, CoalitionImpl):
            coalition_codelet = coalition.getCreatingAttentionCodelet()
        if isinstance (coalition_codelet, AttentionCodelet):
            newCodelet = AttentionCodeletImpl(self.current_situational_model,
                                              self.global_workspace)
            content = coalition.getContent()
            newCodelet.setSoughtContent(content.copy())
            newCodelet.run_task()
            self.logger.debug(f"Created new codelet: {newCodelet}")
        elif coalition_codelet is not None:
    # TODO Reinforcement amount might be a function of the broadcast's
    # activation
            coalition_codelet.reinforceBaseLevelActivation(
                self.codelet_reinforcement)
            self.logger.debug(f"Reinforcing codelet: {coalition_codelet}")

    def FormCoalition(self):
        return self.formed_coalition

    def bufferContainsSoughtContent(self, buffer):
        if isinstance(buffer, CurrentSituationalModelImpl):
            for node in buffer.getBufferContent().getNodes():
                for sought_node in self.getSoughtContent().getNodes():
                    if node.getLabel() == sought_node.getLabel():
                        return True
        return False

    """
        Returns sought content and related content from specified
        WorkspaceBuffer
        """
    def retrieveWorkspaceContent(self, buffer):
        if isinstance(buffer, CurrentSituationalModel):
            return buffer.getBufferContent()

