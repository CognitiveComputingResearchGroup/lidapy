from time import sleep

from source.Framework.Strategies.LinearDecayStrategy import LinearDecayStrategy
from source.GlobalWorkspace.Coalition import Coalition
from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.Workspace.CurrentSituationalModel.CurrentSituationalModelImpl import \
    CurrentSituationalModelImpl

DEFAULT_REFRACTORY_PERIOD = 40
DEFAULT_COALITION_REMOVAL_THRESHOLD = 0.0
DEFAULT_THRESHOLD = 0.0
DEFAULT_DECAY_STRATEGY = LinearDecayStrategy()

class GlobalWorkSpaceImpl(GlobalWorkspace):
    def __init__(self):
        super().__init__()
        self.coalitions = []
        self.broadcast_triggers = []
        self.coalition_decay_strategy = None
        self.broadcast_sent_count = 0
        self.broadcast_started = False
        self.broadcast_was_sent = False
        self.last_broadcast_trigger = None
        self.aggregate_trigger_threshold = None
        self.coalition_removal_threshold = None
        self.broadcast_refractory_period = None
        self.winningCoalition = None
        self.state = None
        self.tick = 0
        self.shutdown = False
        self.tick_at_last_broadcast = 0
        self.trigger1 = "no_winning_coalition_trigger"
        self.trigger2 = "winning_coalition_trigger"
        self.trigger3 = "no_broadcast_for_extended_period"
        self.logger.debug("Initialized GlobalWorkspaceImpl")

    def run_task(self):
        self.coalition_decay_strategy = DEFAULT_DECAY_STRATEGY
        self.aggregate_trigger_threshold = DEFAULT_THRESHOLD
        self.coalition_removal_threshold = DEFAULT_COALITION_REMOVAL_THRESHOLD
        self.broadcast_refractory_period = DEFAULT_REFRACTORY_PERIOD
        self.broadcast_triggers.append(self.trigger1)
        self.run()

    def addCoalition(self, coalition):
        coalition.setDecayStrategy(self.coalition_decay_strategy)
        coalition.setActivatibleRemovalThreshold(
            self.coalition_removal_threshold)
        self.coalitions.append(coalition)
        self.logger.debug("New coalition added with activation "
                f"{coalition.getActivation()}")
        self.newCoalitionEvent()

    def addBroadcastTrigger(self, trigger):
        self.broadcast_triggers.append(trigger)

    def getBroadcastSentCount(self):
        return self.broadcast_sent_count

    def newCoalitionEvent(self):
        aggregateActivation = 0.0
        if len(self.broadcast_triggers) > 0:
            for trigger in self.broadcast_triggers:
                for coalition in self.coalitions:
                    aggregateActivation += coalition.getActivation()
                    if aggregateActivation > self.aggregate_trigger_threshold:
                        self.logger.debug("Aggregate activation trigger fired"
                                          f" at tick: {self.tick}")
                        self.broadcast_started = True
                        self.triggerBroadcast(trigger)
                        sleep(3)
        else:
            for coalition in self.coalitions:
                aggregateActivation += coalition.getActivation()
                if aggregateActivation > self.aggregate_trigger_threshold:
                    self.logger.debug("Aggregate activation trigger fired"
                                      f" at tick: {self.tick}")
                    self.triggerBroadcast(None)

    def getTickAtLastBroadcast(self):
        return self.tick_at_last_broadcast

    def triggerBroadcast(self, trigger):
        if self.broadcast_started:
            self.broadcast_started = False
            if (self.tick - self.tick_at_last_broadcast <
                self.broadcast_refractory_period):
                self.broadcast_started = False
                sleep(25)
                """No winning coalition for some time, add trigger"""
                if self.trigger3 not in self.broadcast_triggers:
                    self.broadcast_triggers.append(self.trigger3)
                """No winning coalition, remove trigger"""
                if self.trigger2 in self.broadcast_triggers:
                    self.broadcast_triggers.remove(self.trigger2)
            else:
                self.broadcast_was_sent = self.sendBroadCast()
                if self.broadcast_was_sent:
                    self.last_broadcast_trigger = trigger
                    self.notify_observers()
                    sleep(25)

    def sendBroadCast(self):
        self.logger.debug("Triggering broadcast")
        self.winningCoalition = self.chooseCoalition()
        self.broadcast_was_sent = False
        if self.winningCoalition is not None:
            self.coalitions.remove(self.winningCoalition)
            """Winning coalition found, remove trigger"""
            if self.trigger1 in self.broadcast_triggers:
                self.broadcast_triggers.remove(self.trigger1)
            """Add winning coalition trigger"""
            if self.trigger2 not in self.broadcast_triggers:
                self.broadcast_triggers.append(self.trigger2)
            self.tick_at_last_broadcast = self.tick
            self.broadcast_sent_count += 1
            self.broadcast_was_sent = True
        else:
            self.logger.debug("Broadcast was triggered but there are no "
                              "coalitions")
            self.broadcast_was_sent = False
        self.broadcast_started = False
        return self.broadcast_was_sent

    def get_state(self):
        return self.state

    def get_broadcast(self):
        return self.winningCoalition

    def chooseCoalition(self):
        chosen_coalition = None
        for coalition in self.coalitions:
            if (chosen_coalition is None or
                coalition.getActivation() > chosen_coalition.getActivation()):
                chosen_coalition = coalition
        self.logger.debug("Winning coalition found")
        return chosen_coalition

    def setCoalitionDecayStrategy(self, decay_strategy):
        self.coalition_decay_strategy = decay_strategy

    def getCoalitionDecayStrategy(self):
        return self.coalition_decay_strategy

    def decayModule(self, tick):
        self.decay(tick)
        self.logger.debug("Coalitions decayed")

    def decay(self, tick):
        for coalition in self.coalitions:
            coalition.decay(tick)
            if isinstance(coalition, Coalition):
                if coalition.isRemovable():
                    self.coalitions.remove(coalition)
                    self.logger.debug("Coalition removed")

    def notify(self, module):
        if isinstance(module, CurrentSituationalModelImpl):
            if module.getModuleContent() is not None:
                self.state = module.get_state()
                coalition = module.getModuleContent()
                attention_codelet = coalition.getCreatingAttentionCodelet()
                if attention_codelet not in self.observers:
                    self.add_observer(attention_codelet)
                self.addCoalition(coalition)
            else:
                if self.coalitions is not None and len(self.coalitions) > 0:
                    self.newCoalitionEvent()