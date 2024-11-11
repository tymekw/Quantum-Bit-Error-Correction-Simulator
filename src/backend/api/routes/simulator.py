from fastapi import APIRouter, BackgroundTasks

from backend.core.task_manager import (
    run_simulation_in_background,
    get_task_status,
    force_stop_process,
    semaphore,
    running_tasks,
    task_id_generator,
)
from simulator.common import SimulatorParameters
from backend.model import ForcedStopStatus, TaskStatus

router = APIRouter()


@router.post("/simulator/start-simulation")
def start_simulation(
    parameters: SimulatorParameters, background_tasks: BackgroundTasks
) -> int | None:
    task_id = next(task_id_generator)
    if not semaphore.acquire(block=False):
        return None

    background_tasks.add_task(run_simulation_in_background, task_id, parameters)

    return task_id


@router.get("/simulator/status/{task_id}")
async def get_task_status_data(task_id: int) -> TaskStatus:
    return get_task_status(task_id)


@router.post("/simulator/cancel-simulation/{task_id}")
async def cancel_simulation(task_id: int) -> ForcedStopStatus:
    return force_stop_process(task_id)


@router.get("/simulator/running-simulations")
async def running_simulations() -> dict[str, list[int]]:
    return {'running simulations': list(running_tasks.keys())}
