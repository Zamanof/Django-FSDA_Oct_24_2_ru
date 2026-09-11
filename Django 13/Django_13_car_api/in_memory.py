from threading import Lock
from typing import Dict

from models import CarRead

_store: Dict[int, CarRead] = {}
_next_id = 1
_lock: Lock = Lock()