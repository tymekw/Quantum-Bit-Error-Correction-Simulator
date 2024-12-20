from fastapi import APIRouter, BackgroundTasks, HTTPException
from starlette.responses import FileResponse

from backend.api.core.task_manager import (
    run_simulation_in_background,
    get_task_status,
    force_stop_process,
    semaphore,
    running_tasks,
    task_id_generator,
    get_download_file, tasks,
)
from backend.simulator.common import SimulatorParameters
from backend.api.model import ForcedStopStatus, TaskStatus, Status

router = APIRouter()


@router.post("/simulator/start-simulation")
def start_simulation(
    parameters: SimulatorParameters, background_tasks: BackgroundTasks
) -> TaskStatus:
    task_id = next(task_id_generator)
    if not semaphore.acquire(block=False):
        return TaskStatus(
            task_id=task_id, status=Status.COULD_NOT_START, parameters=parameters
        )

    background_tasks.add_task(run_simulation_in_background, task_id, parameters)
    print(task_id)
    return TaskStatus(task_id=task_id, status=Status.STARTED, parameters=parameters)


@router.get("/simulator/status/{task_id}")
async def get_task_status_data(task_id: int) -> TaskStatus:
    return get_task_status(task_id)


@router.post("/simulator/cancel-simulation/{task_id}")
async def cancel_simulation(task_id: int) -> ForcedStopStatus:
    return force_stop_process(task_id)


@router.get("/simulator/running-simulations")
async def running_simulations() -> dict[str, list[int]]:
    return {"simulations": list(running_tasks.keys())}

@router.get("/simulator/all-simulations")
async def running_simulations() -> dict[str, list[int]]:
    return {"simulations": list(tasks.keys())}


@router.get("/simulator/download/{task_id}")
async def download_file(task_id: int) -> FileResponse:
    try:
        return get_download_file(task_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
