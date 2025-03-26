import time

from source.ActionSelection.ActionSelection import ActionSelection
from source.AttentionCodelets.AttentionCodelet import AttentionCodelet
from source.Framework.Strategies.DecayStrategy import DecayStrategy
from source.GlobalWorkspace.Coalition import Coalition
from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.ModuleInitialization.DefaultLogger import getLogger
from source.PAM.PAM import PerceptualAssociativeMemory
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory
from source.SensoryMotorMemory.SensoryMotorMemory import SensoryMotorMemory
from source.Workspace.CurrentSituationModel.CurrentSituationModelImpl import \
    CurrentSituationalModelImpl

DEFAULT_REFRACTORY_PERIOD = 40
DEFAULT_COALITION_REMOVAL_THRESHOLD = 0.0
DEFAULT_THRESHOLD = 0.0

class GlobalWorkSpaceImpl(GlobalWorkspace):
    def __init__(self):
        super().__init__()
        self.coalitions = []
        self.broadcast_triggers = []
        self.add_observer(PerceptualAssociativeMemory)
        self.add_observer(AttentionCodelet)
        self.add_observer(ProceduralMemory)
        self.add_observer(ActionSelection)
        self.add_observer(SensoryMotorMemory)
        self.coalition_decay_strategy = DecayStrategy()
        self.broadcast_sent_count = 0
        self.broadcast_started = False
        self.broadcast_was_sent = False
        self.tick_at_last_broadcast = None
        self.last_broadcast_trigger = None
        self.aggregate_trigger_threshold = DEFAULT_THRESHOLD
        self.coalition_removal_threshold = DEFAULT_COALITION_REMOVAL_THRESHOLD
        self.broadcast_refractory_period = DEFAULT_REFRACTORY_PERIOD
        self.logger = getLogger(self.__class__.__name__).logger

    def addCoalition(self, coalition):
        coalition.setDecayStrategy(self.coalition_decay_strategy)
        coalition.setActivatibleRemovalThreshold(
            self.coalition_removal_threshold)
        self.coalitions.append(coalition)
        self.logger.debug(f"New coalition added with activation {
                coalition.getActivatibleRemovalThreshold()}")

    def addBroadcastTrigger(self, trigger):
        self.broadcast_triggers.append(trigger)

    def getBroadcastSentCount(self):
        return self.broadcast_sent_count

    def newCoalitionEvent(self):
        aggregateActivation = 0.0
        for trigger in self.broadcast_triggers:
            for coalition in self.coalitions:
                aggregateActivation += coalition.getActivation()
                if aggregateActivation > self.aggregate_trigger_threshold:
                    self.logger.debug("Aggregate activation trigger fired")
                    self.triggerBroadcast(trigger)

    def getTickAtLastBroadcast(self):
        return self.tick_at_last_broadcast

    def triggerBroadcast(self, trigger):
        if self.broadcast_started:
            self.broadcast_started = False
            if (time.time() - self.tick_at_last_broadcast <
                self.broadcast_refractory_period):
                self.broadcast_started = False
            else:
                self.broadcast_was_sent = True
                if self.broadcast_was_sent:
                    self.last_broadcast_trigger = trigger


    def sendBroadCast(self):
        self.logger.debug("Triggering broadcast")
        winningCoaliton = self.chooseCoalition()
        if winningCoaliton is not None:
            self.coalitions.remove(winningCoaliton)
            self.notify_observers()
            self.broadcast_sent_count += 1
            self.tick_at_last_broadcast = time.time()
        else:
            self.logger.debug("Broadcast was triggerd but there are no "
                              "coalitions")
        self.broadcast_started = False

    def chooseCoalition(self):
        chosenCoalition = None
        for coalition in self.coalitions:
            if (chosenCoalition is None or
                coalition.getActivation() > chosenCoalition.getActication()):
                chosenCoalition = coalition
        return chosenCoalition

    def setCoalitionDecayStrategy(self, decay_strategy):
        self.coalition_decay_strategy = decay_strategy

    def getCoalitionDecayStrategy(self):
        return self.coalition_decay_strategy

    def decayModule(self, ticks):
        self.decay(ticks)
        self.logger.debug("Coalitions decayedS")

    def decay(self, ticks):
        for coalition in self.coalitions:
            coalition.decay(ticks)
            if isinstance(coalition, Coalition):
                if coalition.isRemovable():
                    self.coalitions.remove(coalition)
                    self.logger.debug("Coalition removed")

    def notify(self, module):
        if isinstance(module, CurrentSituationalModelImpl):
            self.addCoalition(module.getCoalition())