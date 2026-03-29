from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class SensorData(BaseModel):
    device_id: UUID
    temperature: float
    humidity: float
    timestamp: datetime


class userResponse(BaseModel):
    device_id: UUID
    temperature: float
    humidity: float
    device_name: str
