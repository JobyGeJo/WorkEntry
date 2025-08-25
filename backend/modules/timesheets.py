from typing import List, Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, Query as SQLQuery

from Exceptions import InternalServerError
from database import with_postgres
from database.postgres.tables import TimesheetTable, UserTable
from models.models import Timesheet, TimesheetWithUser
from models.request import TimeSheetParams, TimesheetPayload


@with_postgres
def fetch_timesheets(params: TimeSheetParams, *, db: Session) -> List[Timesheet]:
    query: SQLQuery = params.build(db.query(
        TimesheetTable
    ))

    return [Timesheet.model_validate(timesheet) for timesheet in query.all()]

@with_postgres
def fetch_timesheet(timesheet_id: int, *, db: Session) -> Union[Timesheet, None]:
    timesheet: TimesheetTable = db.query(TimesheetTable).filter(TimesheetTable.id == timesheet_id).one_or_none()
    if timesheet is None:
        return None
    return TimesheetWithUser.model_validate(timesheet)

@with_postgres
def create_timesheet(activity: TimesheetPayload, *, db: Session) -> int:
    activity = TimesheetTable(
        user_id=activity.user_id,
        machine=activity.machine,
        description=activity.description,
        date=activity.date,
        start_time=activity.start_time,
        end_time=activity.end_time,
    )

    try:
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity.id
    except IntegrityError:
        db.rollback()
        raise InternalServerError("Database error while creating user")


if __name__ == "__main__":
    print(fetch_timesheets())