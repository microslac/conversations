from typing import Optional
from faststream import Path
from faststream.rabbit import RabbitMessage


class QueueContext:
    def __init__(self, msg: RabbitMessage, event: Optional[str] = Path()):
        self.msg = msg
        self.event = event
