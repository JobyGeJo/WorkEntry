from typing import List

from sqlalchemy.orm import Session

from database import with_db_session
from database.tables import TimesheetTable, UserTable
from models.models import TimeSheet
from models.request import QueryParams, TimeSheetParams


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

    query = params.execute(base_query)

    return [TimeSheet.model_validate(timesheet) for timesheet in query]

if __name__ == "__main__":
    print(fetch_timesheets())