from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import httpx

from ..tree_parity_machine.weights_converter import BinaryProcessor

app = FastAPI()

# Store registered users
users = []



hidden_layer_bits = None

class User(BaseModel):
    ip: str
    port: int

class WeightsRange(BaseModel):
    range: int

class SendWeightsRangeRequest(BaseModel):
    receiver_ip: str
    receiver_port: int
    params: WeightsRange

class TPMWeights(BaseModel):
    weights: str


@app.post("/register/")
async def register_user(user: User):
    # Check if user is already registered
    for existing_user in users:
        if existing_user.ip == user.ip and existing_user.port == user.port:
            raise HTTPException(status_code=400, detail="User already registered")
    
    users.append(user)
    return {"message": "User registered successfully"}

@app.post('/set-input-weights')
async def set_input_weights(tmp_weights: TPMWeights):
    global hidden_layer_bits
    hidden_layer_bits = tmp_weights.weights
    return {"hidden layer weights set!"}

@app.post('/send-weights-range')
async def send_weights_range(request: SendWeightsRangeRequest):
    # Check if the receiver is registered
    if not any(user for user in users if user.ip == request.receiver_ip and user.port == request.receiver_port):
        raise HTTPException(status_code=400, detail="Receiver not registered")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{request.receiver_ip}:{request.receiver_port}/receive-weights-range/",
            json=request.params.model_dump()  # Send the params as JSON
        )
    
    return {"message": "Parameters sent successfully", "response": response.json(), "req:": request.params.model_dump()}

@app.post("/receive-weights-range/")
async def receive_result(params: WeightsRange):
    # Handle the received parameters
    hidden_layer_weights_range = params.range
    hidden_layer_weights = prepare_hidden_layer_weights(hidden_layer_weights_range, hidden_layer_bits)
    return {"message": f"Parameters received: {params}", "arr": hidden_layer_weights}


def prepare_hidden_layer_weights(range: int, weights: str):
    return BinaryProcessor(weights, range).bits_to_weights()


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
