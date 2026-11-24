from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel 

class Machine(BaseModel):
    id: int
    name: str
    status: str

class Alarm(BaseModel):
    id: int
    machine_id: int
    code: str
    message: str

ALARMS = [
    Alarm(id=101, machine_id=1,code="E01",message="Overheating"),
    Alarm(id=102, machine_id=2,code="E02",message="ow pressure"),
    Alarm(id=103, machine_id=1,code="E03",message="High vibration"),
]

MACHINES = [
    Machine(id=1, name = 'CNC-01', status="running"),
    Machine(id=2, name = 'CNC-02', status="stopped"),
    Machine(id=3, name = 'PRESS-01', status="maintenance"),
]

app = FastAPI(title="Mini MES API")


@app.get("/")
def home():
    return {"message": "Mini MES API is running"}

@app.get("/machines",response_model=list[Machine])
def get_machines():
    return MACHINES

@app.get("/machines/{machine_id}", response_model=Machine)
async def read_machine(machine_id: int):
    for machine in MACHINES:
        if (machine_id == machine.id):
            return machine
    else:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

@app.get("/machines/{machine_id}/alarms",response_model=list[Alarm])
async def read_alarms(machine_id: int):
    alarms=[]
    for machine in MACHINES:
        if (machine_id == machine.id):
            for alarm in ALARMS:
                if (machine_id == alarm.machine_id):
                    alarms.append(alarm)
            return alarms
    else:
        raise HTTPException(status_code=404,detail="Machine not found")

 