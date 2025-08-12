from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from models.request import QueryParams, TimeSheetParams
from models.response import Respond
from modules.timesheets import fetch_timesheets

timesheet = APIRouter(prefix="/timesheets")

@timesheet.get("")
def get_timesheets(params: TimeSheetParams = Depends()) -> JSONResponse:
    return Respond.success("Datas fetched successfully", fetch_timesheets(params))

@timesheet.get("/test")
def test(params: TimeSheetParams = Depends()) -> JSONResponse:
    return params