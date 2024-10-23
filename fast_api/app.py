from functools import wraps
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import httpx

from tree_parity_machine.weights_converter import bits_to_arr, bits_to_weights, get_possible_hidden_layer_size
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# Store registered users
server_user = None
client_user = None


hidden_layer_bits = None
weights_range = None


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

# Custom decorator to check if client_user is set
def server_only(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global client_user
        if client_user is None:
            raise HTTPException(status_code=400, detail="This function is awailable only for server user.")
        return await func(*args, **kwargs)
    return wrapper

def client_only(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global server_user
        if server_user is None:
            raise HTTPException(status_code=400, detail="This function is awailable only for client user.")
        return await func(*args, **kwargs)
    return wrapper


@app.post("/register-server/")
async def register_server(user: User):
    global server_user
    server_user = user
    return {"message": "User registered successfully"}

@app.post("/register-client/")
async def register_client(user: User):
    global client_user
    client_user = user
    return {"message": "User registered successfully"}

@app.post('/set-input-weights')
async def set_input_weights(tmp_weights: TPMWeights):
    global hidden_layer_bits
    hidden_layer_bits = tmp_weights.weights
    return {"hidden layer weights set!"}


# @app.post('/set-weights-range')

@app.post('/set-weights-range')
@server_only
async def send_weights_range(request: SendWeightsRangeRequest):
    global client_user
    if not client_user.ip == request.receiver_ip and client_user.port == request.receiver_port:
        raise HTTPException(status_code=400, detail="Receiver not registered")
    global weights_range
    weights_range = request.params.range

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{request.receiver_ip}:{request.receiver_port}/receive-weights-range/",
            json=request.params.model_dump()  # Send the params as JSON
        )
    
    return {"message": "Parameters sent successfully", "response": response.json(), "req:": request.params.model_dump()}

@app.post("/receive-weights-range/")
@client_only
async def receive_result(params: WeightsRange):
    global weights_range
    weights_range = params.range
    return {"message": f"Parameters received: {params}", "weights_range":  weights_range}


def prepare_hidden_layer_weights(range: int, weights: str, K, N):
    return bits_to_arr(bits=weights, L=range, K=K, N=N)










# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
