# From FailStop
import numpy as np
from threading import Lock

n = 244
def get_n():
    global n
    return n
def set_n(new_val):
    global n
    n = new_val
# t denotes an upper bound on the number of failures tolerated
t = int(np.floor(n/3))
if n%3 == 0:
    t -= 1

def get_t():
    return t
def set_t():
    global t, n
    t = int(np.floor(n/3))
    if n%3 == 0:
        t -= 1

#MAX_ALIVE_PROCESSES = n-t
        
class Message:
    def __init__(self, process_id, receivers) -> None:
        self.sender = process_id
        self.receivers = receivers

# From QuantumCoinFlip
coin_lock = Lock()
leader_lock = Lock()
