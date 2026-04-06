from v1.schemas.SensorSchema import SensorData
from .engine import SessionDep
from .model import Devices


def addNewDevice(device_id: int, session: SessionDep):
    session.add(Devices(device_id))


def addNewEntry(data: SensorData, session: SessionDep):
    session.add(data)


def showAllEntries(session: SessionDep):
    session.list
