from sympy.codegen.cnodes import sizeof
from source.Workspace.BroadCastQueue import BroadCastQueue


class BroadCastQueueImpl(BroadCastQueue):
    def __init__(self):
        super().__init__()
        self.DEFAULT_QUEUE_CAPACITY = 20
        self.broadcastQueueCapacity  = self.DEFAULT_QUEUE_CAPACITY
        self.broadcast_queue = []

    def receive_broadcast(self, coalition):
        pass

    def add_buffer_content(self, workspace_content):
        self.broadcast_queue.insert(0, workspace_content)

        while sizeof(self.broadcast_queue) > self.broadcastQueueCapacity:
            self.broadcast_queue.pop(self.broadcastQueueCapacity - 1)

    def get_position_content(self, index):
        if -1 < index < sizeof(self.broadcast_queue):
            if sizeof(self.broadcast_queue) > 0:
                return self.broadcast_queue[index]
        return None

    def get_buffer_content(self, params):
        if params is not None:
            index = params.get("position")
            if isinstance(index, int):
                return self.get_position_content(index)
        return None

    def getModuleContent(self, params):
        pass

    def decayModule(self, time):
        pass
