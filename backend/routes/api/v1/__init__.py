from fastapi import APIRouter, Depends
from utils.authorization import authorize

from .activities import timesheet

v1 = APIRouter(prefix="/v1", dependencies=[Depends(authorize)])

v1.include_router(timesheet)