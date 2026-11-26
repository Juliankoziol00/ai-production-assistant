from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel 

class Machine(BaseModel):
    id: int
    name: str
    status: str
    alarm_count: int

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
    Machine(id=1, name = 'CNC-01', status="running", alarm_count=1),
    Machine(id=2, name = 'CNC-02', status="stopped", alarm_count=3),
    Machine(id=3, name = 'PRESS-01', status="maintenance", alarm_count=0),
]

app = FastAPI(title="Mini MES API")


@app.get("/")
def home():
    return {"message": "Mini MES API is running"}

@app.get("/machines",response_model=list[Machine])
def get_machines():
    return MACHINES

@app.get("/machines/stopped",response_model=list[str])
async def get_stopped_machines():
    stopped_machines = []
    for machine in MACHINES:
        if (machine.status == "stopped"):
            stopped_machines.append(machine.name)
    if (stopped_machines != []):
        return stopped_machines

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

@app.get("/machines/{machine_id}/summary",response_model=dict)
async def get_machine_summary(machine_id: int):
    summary = {}
    alarm_count = 0
    for machine in MACHINES:
        if (machine_id == machine.id):
            summary["machine_id"] = machine.id
            summary["name"] = machine.name
            summary["status"] = machine.status
            summary["alarm_count"] = alarm_count
            return summary
    else:
        raise HTTPException(status_code=404, detail="Machine not found")
