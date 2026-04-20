from datetime import datetime
from uuid import UUID
from sqlmodel import Field, SQLModel


class Telemetry(SQLModel, table=True):
    id: int = Field(primary_key=True)
    device_id: UUID = Field(foreign_key="devices.device_id")
    name: str | None
    temperature: float | None = Field(default=None)
    humidity: float | None = Field(default=None)
    timestamp: datetime = Field(default=datetime.now())


class Devices(SQLModel, table=True):
    device_id: UUID = Field(primary_key=True)
