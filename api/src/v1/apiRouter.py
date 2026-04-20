from uuid import UUID
from fastapi import APIRouter, status, HTTPException
from .schemas.SensorSchema import SensorData, userResponse
from .schemas.model import Telemetry, Devices
from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session, select


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


router = APIRouter()


@router.post("/device/register", status_code=status.HTTP_201_CREATED)
def registerDevice(device_id: UUID, session: SessionDep):
    device = session.get(Devices, device_id)
    if device:
        raise HTTPException(status_code=409, detail="device already exists")
    db_device = Devices(device_id=device_id)
    session.add(db_device)
    session.commit()
    return {"message": "device registered"}


@router.delete("/device/unregister/{device_id}", status_code=status.HTTP_200_OK)
def unregisterDevice(device_id: UUID, session: SessionDep):
    device = session.exec(select(Devices).where(Devices.device_id == device_id)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    session.delete(device)
    session.commit()
    return {"message": "device unregistered"}


@router.post("/device/{device_id}/entry", status_code=status.HTTP_201_CREATED)
def registerData(device_id: UUID, data: SensorData, session: SessionDep):
    telemetry = Telemetry(
        device_id=device_id,
        temperature=data.temperature,
        humidity=data.humidity,
        timestamp=data.timestamp,
        name="device_" + str(device_id)[:4],
    )
    session.add(telemetry)
    session.commit()
    return {"message": "data registered"}


@router.get("/user/{device_id}", response_model=userResponse)
def sendData(device_id: UUID, session: SessionDep):
    statement = (
        select(Telemetry)
        .where(Telemetry.device_id == device_id)
        .order_by(Telemetry.timestamp.desc())
    )
    latest_telemetry = session.exec(statement).first()

    if not latest_telemetry:
        raise HTTPException(status_code=404, detail="No data found for this device")

    return {
        "device_id": device_id,
        "temperature": latest_telemetry.temperature or 0.0,
        "humidity": latest_telemetry.humidity or 0.0,
        "device_name": latest_telemetry.name or "Unknown",
    }
