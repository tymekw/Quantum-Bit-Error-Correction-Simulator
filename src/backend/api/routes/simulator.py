import multiprocessing
import os
import uuid
from fastapi import APIRouter, BackgroundTasks
from simulator.common import SimulatorParameters
from simulator.simulation_runner import run_simulation

router = APIRouter()

# Maximum number of concurrent processes
MAX_CONCURRENT_PROCESSES = os.cpu_count() - 1
semaphore = multiprocessing.Semaphore(MAX_CONCURRENT_PROCESSES)

# Dictionary to store task status
task_status = {}
running_tasks = {}


def run_simulation_with_status(parameters: SimulatorParameters):
    try:
        run_simulation(parameters)
    except OSError:
        print('OS error')
    except Exception as e:
        print(f"failed: {e}")


@router.post("/simulator/start-simulation")
def start_simulation(parameters: SimulatorParameters, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())

    # Try to acquire the semaphore non-blocking
    if not semaphore.acquire(block=False):
        return {"maximum_number_of_running_simulations_reached": list(running_tasks.keys())}

    # Start the simulation in the background if the semaphore is acquired
    background_tasks.add_task(run_simulation_in_background, task_id, parameters)

    # Store task status in the dictionary
    task_status[task_id] = {"status": "running", "parameters": parameters.model_dump()}

    return {"simulation_id": task_id, "status": "running"}


@router.get("/simulator/status/{task_id}")
async def get_task_status_data(task_id: str):
    return task_status.get(task_id, {"status": "unknown", "parameters": {}})


@router.post("/simulator/cancel-simulation/{task_id}")
async def cancel_simulation(task_id: str):
    process = running_tasks.get(task_id)

    if process and process.is_alive():
        force_stop_process(process, task_id)  # Force stop the process


def run_simulation_in_background(task_id: str, parameters: SimulatorParameters):
    process = multiprocessing.Process(target=run_simulation_with_status, args=(parameters,))

    # Start the process
    process.start()

    # Store the process in the running_tasks dictionary
    running_tasks[task_id] = process
    task_status[task_id]["status"] = "running"

    # Wait for the process to finish
    process.join()

    # Update status after the process finishes
    task_status[task_id]["status"] = "completed"

    # Release the semaphore once the process is done
    semaphore.release()


def force_stop_process(process, task_id):
    try:
        process.terminate()  # Forcefully terminate the process
        process.join(timeout=2)  # Wait for the process to terminate gracefully
        if process.is_alive():
            print("Process did not terminate in time, forcefully killing it.")
            process.kill()  # If the process doesn't terminate, kill it
        running_tasks.pop(task_id)
        task_status[task_id]["status"] = "terminated"
        # Release the semaphore after process termination
        semaphore.release()
    except Exception as e:
        print(f"Error while terminating process: {e}")
        semaphore.release()  # Release the semaphore in case of error
