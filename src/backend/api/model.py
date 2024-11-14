from enum import Enum

from pydantic import BaseModel

from backend.simulator.common import SimulatorParameters


class Status(Enum):
    STARTED = "started"
    RUNNING = "running"
    FINISHED = "finished"
    CANCELED = "cancelled"
    STOPPING = "stopping"
    COULD_NOT_START = "not_started"


class TaskStatus(BaseModel):
    task_id: int | None
    status: Status | None
    parameters: SimulatorParameters | None


class ForcedStopResult(Enum):
    SUCCESS = "success"
    ALREADY_NOT_RUNNING = "process already not running"
    ERROR = "error"


class ForcedStopStatus(BaseModel):
    task_id: int
    forced_stop_result: ForcedStopResult
