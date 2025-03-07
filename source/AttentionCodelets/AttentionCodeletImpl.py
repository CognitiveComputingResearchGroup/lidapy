from source.AttentionCodelets.AttentionCodelet import AttentionCodelet
from source.GlobalWorkspace.Coalition import Coalition
from source.GlobalWorkspace.CoalitionImpl import CoalitionImpl


class AttentionCodeletImpl(AttentionCodelet):
    def __init__(self, current_situational_model, global_workspace):
        super().__init__(current_situational_model, global_workspace)

        self.currentSituationalModel = current_situational_model
        self.global_workspace = global_workspace
        self.DEFAULT_CODELET_REFRACTORY_PERIOD = 50
        self.codeletRefractoryPeriod = None

    def run_task(self):
        if self.bufferContainsSoughtContent(self.currentSituationalModel):
            csm_content = self.retrieveWorkspaceContent(
                                    self.currentSituationalModel)
            if csm_content is None:
                self.logger.warning("Null WorkspaceContent returned."
                                          "Coalition cannot be formed.")
            elif csm_content.getLinkableCount() > 0:
                coalition = CoalitionImpl(csm_content, self)
                self.global_workspace.add_coalition(coalition)
                self.logger.info("Coalition successfully formed.")

    def set_refactory_period(self, ticks):
        if ticks > 0:
            self.codeletRefractoryPeriod = ticks
        else:
            self.codeletRefractoryPeriod =  (
                self.DEFAULT_CODELET_REFRACTORY_PERIOD)

    def get_refactory_period(self):
        return self.codeletRefractoryPeriod

