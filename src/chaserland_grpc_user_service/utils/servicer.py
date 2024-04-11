from .AIOgRPCServer import Context
from .ref import Ref


class AIOgRPCServicer:
    def __init__(self, server_context_ref: Ref[Context] = Ref()):
        self.server_context_ref = server_context_ref

    @property
    def server_context(self) -> Context:
        if self.server_context_ref.current is None:
            raise AttributeError("Server context is not set")
        return self.server_context_ref.current
