from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse

from models.request import TimeSheetParams, TimesheetPayload
from models.response import Respond
from modules.timesheets import fetch_timesheets, create_timesheet
from utils.session import get_session_user_id

timesheet = APIRouter(prefix="/timesheets")

@timesheet.get("")
def get_timesheets(params: TimeSheetParams = Depends()) -> JSONResponse:
    return Respond.success("Datas fetched successfully", fetch_timesheets(params), params.pagination)

@timesheet.post("")
def post_timesheets(payload: TimesheetPayload, request: Request) -> JSONResponse:
    if payload.user_id is None:
        payload.user_id = get_session_user_id(request)
    return Respond.created("Activity created successfully", create_timesheet(payload))