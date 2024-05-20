# From FailStop
import numpy as np

n = 4
t = 0
first_to_decide = None

MAX_ALIVE_PROCESSES = n-t
        
class Message:
    def __init__(self, process_id, receivers) -> None:
        self.sender = process_id
        self.receivers = receivers