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

router = APIRouter()


@router.post("/simulator/start-simulation")
def start_simulation(
    parameters: SimulatorParameters, background_tasks: BackgroundTasks
):
    task_id = next(task_id_generator)

    # Check if the maximum number of concurrent simulations has been reached
    if not semaphore.acquire(block=False):
        return {
            "maximum_number_of_running_simulations_reached": list(running_tasks.keys())
        }

    background_tasks.add_task(run_simulation_in_background, task_id, parameters)

    return {"simulation_id": task_id}


@router.get("/simulator/status/{task_id}")
async def get_task_status_data(task_id: int):
    return get_task_status(task_id)


@router.post("/simulator/cancel-simulation/{task_id}")
async def cancel_simulation(task_id: int):
    return force_stop_process(task_id)


@router.get("/simulator/running-simulations")
async def running_simulations():
    return {"running_simulations": list(running_tasks.keys())}
