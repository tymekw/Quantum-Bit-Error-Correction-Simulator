from dataclasses import dataclass
from enum import Enum

from simulator.common import SimulatorParameters


class Status(Enum):
    RUNNING = "running"
    FINISHED = "finished"
    CANCELED = "cancelled"
    STOPPING = "stopping"


@dataclass
class TaskStatus:
    status: Status
    parameters: SimulatorParameters
