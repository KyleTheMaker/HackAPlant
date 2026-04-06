from uuid import UUID
from fastapi import APIRouter, status
from .schemas.SensorSchema import SensorData, userResponse

router = APIRouter()


@router.post("/device/register")
def registerDevice(device_id: UUID, status_code=status.HTTP_201_CREATED):
    print("Value from client", device_id)
    return {"message": "device registered"}


@router.post("/device/{device_id}/entry", status_code=status.HTTP_201_CREATED)
def registerData(data: SensorData):
    # Save it
    pass


@router.get("/user/{device_id}", response_model=userResponse)
def sendData(device_id: UUID):
    # send data
    return {
        "device_id": device_id,
        "temperature": 38.0,
        "humidity": 33.4,
        "device_name": "test",
    }
