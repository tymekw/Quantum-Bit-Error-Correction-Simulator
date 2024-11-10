import multiprocessing
import itertools

from backend.core.config import MAX_CONCURRENT_PROCESSES
from backend.model import TaskStatus, Status
from simulator.simulation_runner import run_simulation
from simulator.common import SimulatorParameters

# Semaphore for limiting concurrent processes
semaphore = multiprocessing.Semaphore(MAX_CONCURRENT_PROCESSES)

# In-memory task storage
task_id_generator = itertools.count()
running_tasks: dict[int, multiprocessing.Process] = {}
tasks: dict[int, TaskStatus] = {}


def update_task_status(task_id: int, status: Status):
    """Update the status of the task."""
    if status == Status.FINISHED:
        print("somehow finished.")
        if task_id in running_tasks and tasks[task_id].status not in {
            Status.STOPPING,
            Status.CANCELED,
        }:
            tasks[task_id].status = status
            del running_tasks[task_id]
    elif status == Status.CANCELED:
        tasks[task_id].status = status
        del running_tasks[task_id]
    elif status == Status.STOPPING:
        tasks[task_id].status = status
    elif status == Status.RUNNING:
        tasks[task_id].status = status


def start_task(
    task_id: int, parameters: SimulatorParameters, process: multiprocessing.Process
):
    """Start a task, store its process and status."""
    tasks[task_id] = TaskStatus(Status.RUNNING, parameters)
    running_tasks[task_id] = process


def run_simulation_with_status(parameters: SimulatorParameters):
    """Run simulation and handle errors."""
    try:
        run_simulation(parameters)
    except Exception as e:
        print(f"Simulation failed: {e}")


def run_simulation_in_background(task_id: int, parameters: SimulatorParameters):
    """Handle background simulation and status updates."""
    process = multiprocessing.Process(
        target=run_simulation_with_status, args=(parameters,)
    )
    start_task(task_id, parameters, process)

    process.start()

    try:
        process.join()
        update_task_status(task_id, Status.FINISHED)
    finally:
        semaphore.release()


def force_stop_process(task_id: int):
    """Force stop a running simulation."""
    process = running_tasks.get(task_id)
    if not process:
        return {"process is not running."}

    update_task_status(task_id, Status.STOPPING)

    if process.is_alive():
        process.terminate()
        process.join(timeout=2)

        if process.is_alive():
            process.kill()

        if not process.is_alive():
            update_task_status(task_id, Status.CANCELED)
            return {"task cancelled": task_id}
        else:
            update_task_status(task_id, Status.RUNNING)
            return {"something went wrong while stopping the task. Try again."}
    else:
        return {"process was already terminated."}


def get_task_status(task_id: int):
    """Return task status from memory."""
    return tasks.get(task_id, {"status": "unknown", "parameters": {}})
