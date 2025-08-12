from typing import List, Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, Query as SQLQuery

from Exceptions import InternalServerError
from database import with_db_session
from database.tables import TimesheetTable, UserTable
from models.models import TimeSheet
from models.request import TimeSheetParams, TimesheetPayload


@with_db_session
def fetch_timesheets(params: TimeSheetParams, *, db: Session) -> List[TimeSheet]:
    base_query = db.query(
        TimesheetTable.id,
        UserTable.username.label("person"),
        TimesheetTable.machine_name.label("machine"),
        TimesheetTable.description,
        TimesheetTable.start_time,
        TimesheetTable.end_time
    ).join(UserTable, UserTable.id == TimesheetTable.user_id)

    query: SQLQuery = params.build(base_query)

    return [TimeSheet.model_validate(timesheet) for timesheet in query.all()]

@with_db_session
def create_timesheet(activity: Union[TimesheetPayload, TimesheetTable], *, db: Session) -> int:
    if isinstance(activity, TimesheetPayload):
        activity = TimesheetTable(
            user_id=activity.user_id,
            machine_name=activity.machine,
            description=activity.description,
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