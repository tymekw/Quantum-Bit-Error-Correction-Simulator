from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from simulator.common import SimulatorParameters
from pydantic import BaseModel, validator
from typing import List
import asyncio
from jinja2 import Template

from simulator.simulation_runner import run_simulation
from simulator.utils import write_headers

app = FastAPI()

# Simulation status to track when the simulation is complete
simulation_status = {"completed": False}


# Step 1: Define Pydantic Models for Validation
class SimulatorRequest(BaseModel):
    weights_range: List[int]
    number_of_inputs_per_neuron: List[int]
    number_of_neurons_in_hidden_layer: List[int]
    QBER: List[int]
    eve: int = 0
    filepath: str = "tmp_test_result.csv"

    @validator("number_of_inputs_per_neuron", "number_of_neurons_in_hidden_layer", pre=True)
    def check_three_range_elements(cls, v):
        if len(v) != 3:
            raise ValueError("Each range argument must contain exactly three integers separated by space.")
        return v

    def to_simulator_parameters(self):
        return SimulatorParameters(
            weights_range=self.weights_range,
            range_of_inputs_per_neuron=range(*self.number_of_inputs_per_neuron),
            qber_values=self.QBER,
            range_of_neurons_in_hidden_layer=range(*self.number_of_neurons_in_hidden_layer),
            file_path=Path(self.filepath),
            eve=self.eve,
        )


# Step 2: Define HTML GUI with FastAPI
@app.get("/", response_class=HTMLResponse)
async def get_form():
    html_content = """
    <html>
        <body>
            <h1>Simulator Setup</h1>
            <form action="/submit" method="post">
                <label>Weights Range (space-separated integers):</label>
                <input type="text" name="weights_range" required><br>

                <label>Number of Inputs Per Neuron (three integers - start, stop, step):</label>
                <input type="text" name="number_of_inputs_per_neuron" required><br>

                <label>Number of Neurons in Hidden Layer (three integers - start, stop, step):</label>
                <input type="text" name="number_of_neurons_in_hidden_layer" required><br>

                <label>QBER (space-separated integers):</label>
                <input type="text" name="QBER" required><br>

                <label>Eve's Machines:</label>
                <input type="number" name="eve" value="0"><br>

                <label>Filepath:</label>
                <input type="text" name="filepath" value="tmp_test_result.csv"><br>

                <input type="submit" value="Start Simulation">
            </form>
        </body>
    </html>
    """
    return html_content


# Step 3: Handle Form Submission and Start Simulation
@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
        weights_range: str = Form(...),
        number_of_inputs_per_neuron: str = Form(...),
        number_of_neurons_in_hidden_layer: str = Form(...),
        QBER: str = Form(...),
        eve: int = Form(0),
        filepath: str = Form("tmp_test_result.csv"),
):
    try:
        # Parse and validate form input
        request_data = SimulatorRequest(
            weights_range=[int(x) for x in weights_range.split()],
            number_of_inputs_per_neuron=[int(x) for x in number_of_inputs_per_neuron.split()],
            number_of_neurons_in_hidden_layer=[int(x) for x in number_of_neurons_in_hidden_layer.split()],
            QBER=[int(x) for x in QBER.split()],
            eve=eve,
            filepath=filepath,
        )

        # Convert to simulator parameters and start simulation in the background
        simulator_params = request_data.to_simulator_parameters()

        # Reset simulation status
        simulation_status["completed"] = False
        write_headers(simulator_params.file_path, bool(simulator_params.eve))
        # run_simulation(simulator_params)
        # Start background task
        simulation_status["completed"] = await run_simulation(simulator_params)
        # Return a page that will check for completion
        return HTMLResponse(
            """
            <html>
                <body>
                    <h1>Simulation Running...</h1>
                    <p>Your parameters have been accepted. The simulation is running.</p>
                    <script>
                        async function checkStatus() {
                            const response = await fetch('/status');
                            const data = await response.json();
                            if (data.completed) {
                                window.location.href = '/results';
                            } else {
                                setTimeout(checkStatus, 1000);
                            }
                        }
                        checkStatus();
                    </script>
                </body>
            </html>
            """
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Step 4: Define the Status Endpoint
@app.get("/status", response_class=JSONResponse)
async def check_status():
    return {"completed": simulation_status["completed"]}


# Step 5: Define the Simulation Endpoint to Display Results
@app.get("/results", response_class=HTMLResponse)
async def display_results():
    simulated_results = "Simulation complete! Results are ready."

    # Display the final message to the user
    result_template = """
    <html>
        <body>
            <h1>Simulation Completed</h1>
            <p>{{ simulated_results }}</p>
        </body>
    </html>
    """
    template = Template(result_template)
    return HTMLResponse(template.render(simulated_results=simulated_results))

