import concurrent.futures
from multiprocessing import Process
from threading import Lock, Thread

from source.Framework.Tasks.TaskManager import TaskManager
from source.Framework.Strategies.LinearDecayStrategy import LinearDecayStrategy
from source.GlobalWorkspace.Coalition import Coalition
from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.Module.Initialization.DefaultLogger import getLogger
from source.Workspace.CurrentSituationModel.CurrentSituationalModel import \
    CurrentSituationalModel

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
        self.task_manager = TaskManager()
        self.ticks = None
        self.state = None
        self.tick_at_last_broadcast = 0
        self.logger = getLogger(self.__class__.__name__).logger
        self.logger.debug("Initialized GlobalWorkspaceImpl")

    def run_task(self):
        self.coalition_decay_strategy = DEFAULT_DECAY_STRATEGY
        self.aggregate_trigger_threshold = DEFAULT_THRESHOLD
        self.coalition_removal_threshold = DEFAULT_COALITION_REMOVAL_THRESHOLD
        self.broadcast_refractory_period = DEFAULT_REFRACTORY_PERIOD
        trigger1 = "no_broadcast_for_extended_period"
        trigger2 = "winning_coalition_trigger"
        trigger3 = "no_winning_coalition_trigger"
        self.broadcast_triggers.append(trigger1)
        self.broadcast_triggers.append(trigger2)
        self.broadcast_triggers.append(trigger3)
        self.task_manager.name = "GlobalWorkspace"
        self.task_manager.run()
        self.ticks = self.task_manager.getCurrentTick()

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
        self.ticks = self.task_manager.getCurrentTick()
        if len(self.broadcast_triggers) > 0:
            for trigger in self.broadcast_triggers:
                for coalition in self.coalitions:
                    aggregateActivation += coalition.getActivation()
                    if aggregateActivation > self.aggregate_trigger_threshold:
                        self.logger.debug("Aggregate activation trigger fired"
                                          f" at tick: {self.ticks}")
                        self.broadcast_started = True
                        self.triggerBroadcast(trigger)
        else:
            for coalition in self.coalitions:
                aggregateActivation += coalition.getActivation()
                if aggregateActivation > self.aggregate_trigger_threshold:
                    self.logger.debug("Aggregate activation trigger fired"
                                      f" at tick: {self.ticks}")
                    self.triggerBroadcast(None)

    def getTickAtLastBroadcast(self):
        return self.tick_at_last_broadcast

    def triggerBroadcast(self, trigger):
        if self.broadcast_started:
            self.broadcast_started = False
            self.ticks = self.task_manager.getCurrentTick()
            if (self.ticks - self.tick_at_last_broadcast <
                self.broadcast_refractory_period):
                self.broadcast_started = False
            else:
                self.broadcast_was_sent = self.sendBroadCast()
                if self.broadcast_was_sent:
                    self.last_broadcast_trigger = trigger


    def sendBroadCast(self):
        self.logger.debug("Triggering broadcast")
        self.winningCoalition = self.chooseCoalition()
        self.broadcast_was_sent = False
        if self.winningCoalition is not None:
            self.coalitions.remove(self.winningCoalition)
            if "no_winning_coalition_trigger" in self.broadcast_triggers:
                self.broadcast_triggers.remove("no_winning_coalition_trigger")
            self.tick_at_last_broadcast = self.task_manager.getCurrentTick()
            self.notify_observers()
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

    def decayModule(self, ticks):
        self.decay(ticks)
        self.logger.debug("Coalitions decayed")

    def decay(self, ticks):
        for coalition in self.coalitions:
            coalition.decay(ticks)
            if isinstance(coalition, Coalition):
                if coalition.isRemovable():
                    self.coalitions.remove(coalition)
                    self.logger.debug("Coalition removed")

    def notify(self, module):
        if isinstance(module, CurrentSituationalModel):
            if module.getModuleContent() is not None:
                self.addCoalition(module.getModuleContent())
                self.state = module.get_state()
            else:
                if self.coalitions is not None and len(self.coalitions) > 0:
                    self.newCoalitionEvent()