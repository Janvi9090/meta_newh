from pydantic import BaseModel

class Observation(BaseModel):
    concentration: float

class Action(BaseModel):
    dose: float