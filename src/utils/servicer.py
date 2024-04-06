from src.utils.AIOgRPCServer import Context
from src.utils.ref import Ref


class AIOgRPCServicer:
    def __init__(self, server_context_ref: Ref[Context] = Ref()):
        self.server_context_ref = server_context_ref

    @property
    def server_context(self) -> Context:
        return self.server_context_ref.current
