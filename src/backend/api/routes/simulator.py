import multiprocessing
import uuid
from fastapi import APIRouter
from simulator.common import SimulatorParameters
from simulator.simulation_runner import run_simulation

router = APIRouter()

# Maximum number of concurrent processes
MAX_CONCURRENT_PROCESSES = 4

# Semaphore to limit concurrent processes
semaphore = multiprocessing.Semaphore(MAX_CONCURRENT_PROCESSES)

# Dictionary to store task status and the corresponding process
task_status = {}
running_tasks = {}


def run_simulation_with_status(task_id: str, parameters: SimulatorParameters):
    try:
        parameters.file_path = 'lets_go.csv'
        run_simulation(parameters)
    except OSError:
        print('OS error')
    except Exception as e:
        print(f"failed: {e}")


@router.post("/simulator/start-simulation")
def start_simulation(parameters: SimulatorParameters):
    task_id = str(uuid.uuid4())

    # Create a multiprocessing Process explicitly
    process = multiprocessing.Process(target=run_simulation_with_status, args=(task_id, parameters))
    task_status[task_id] = {"status": "queued", "parameters": parameters.model_dump()}

    # Acquire the semaphore before starting the process to ensure we don't exceed the limit
    semaphore.acquire()
    process.start()

    # Store the process in running_tasks
    running_tasks[task_id] = process
    task_status[task_id]["status"] = "running"

    return {"simulation_id": task_id}


@router.get("/simulator/status/{task_id}")
async def get_task_status_data(task_id: str):

    return task_status.get(task_id, {"status": "unknown", "parameters": {}})


@router.post("/simulator/cancel-simulation/{task_id}")
async def cancel_simulation(task_id: str):
    process = running_tasks.get(task_id)

    if process and process.is_alive():
        force_stop_process(process, task_id)  # Force stop the process


def force_stop_process(process, task_id):
    try:
        process.terminate()  # Forcefully terminate the process
        process.join(timeout=1)  # Wait for the process to terminate gracefully
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
