import os

from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles


from simulator.common import SimulatorParameters
from simulator.simulation_runner import run_simulation





app = FastAPI()
is_done = False
app.mount("/static", StaticFiles(directory="src/server/static", html=True), name="static")


def run_simulation_task(parameters):
    global is_done
    is_done = run_simulation(parameters)
    print("Simulation completed")


@app.post("/send_params")
async def receive_params(params: SimulatorParameters, background_task: BackgroundTasks):
    print(params)
    background_task.add_task(run_simulation_task, params)
    print("Redirecting to /thanks")
    return RedirectResponse(url="/thanks", status_code=303)

@app.get('/current_simulation')
def get_current_simulation():
    return {"is_done": is_done}


@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(index_path, "r") as file:
        return file.read()



@app.get("/thanks", response_class=HTMLResponse)
async def thank_you():
    return """
    <html>
        <head>
            <title>Thank You</title>
        </head>
        <body>
            <h1>Thank you for your submission!</h1>
        </body>
    </html>
    """