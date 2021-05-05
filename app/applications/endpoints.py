"""
Application Endpoints
"""
# pylint: disable=inconsistent-return-statements
import datetime
from typing import List
from dateutil import tz
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.applications.schemas import ApplicationRead, ApplicationBase, ApplicationUpdate
from app.dependancies import get_db, get_current_user
from app.users.roles import Roles
from app.users.role_mock_middleware import is_at_least_role
from app.users.schemas import UserInDB
from . import crud
from .application_states import ApplicationStates
from .utils import create_user_from_application, send_fail_mail
from ..settings import TZ

router = APIRouter(
    prefix="/application",
    tags=["Application"],
)

min_view_role = Roles.MODERATOR
min_update_role = Roles.ADMIN


@router.get("/", response_model=List[ApplicationRead])
def view_all_pending_applications(database: Session = Depends(get_db),
                                  current_user: UserInDB = Depends(get_current_user)):
    """View all pending applications"""
    if is_at_least_role(current_user=current_user, role=min_view_role):
        return crud.get_pending_applications(database)


@router.get("/{application_id}", response_model=ApplicationRead)
def view_application(application_id: int, database: Session = Depends(get_db),
                     current_user: UserInDB = Depends(get_current_user)):
    """View an application"""
    if is_at_least_role(current_user=current_user, role=min_view_role):
        return crud.get_application(database=database, application_id=application_id)


@router.post("/", response_model=ApplicationRead, status_code=201)
def create_application(application: ApplicationBase, database: Session = Depends(get_db)):
    """Create an application"""
    min_application_difference = 7 * 24 * 60 * 60  # 1 week
    last_application = crud.get_latest_application_by_email(
        database=database,
        email=application.email
    )
    if last_application:
        diff = (datetime.datetime.now(tz=tz.gettz(TZ)) - last_application.created_date).total_seconds()

        if last_application.status == ApplicationStates.APPROVED:
            raise HTTPException(
                status_code=400,
                detail="Your last application has been approved, please check your mail"
            )
        if last_application.status == ApplicationStates.PENDING:
            raise HTTPException(
                status_code=400,
                detail="Your last application is not yet reviewed, please wait until we review it"
            )
        if diff < min_application_difference:
            raise HTTPException(
                status_code=400,
                detail="Please wait at least a week before submitting a new application"
            )

    return crud.create_application(database=database, application=application)


@router.patch("/{application_id}")
async def update_application(
        application_id: int,
        data: ApplicationUpdate,
        database: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    """Approve/Reject Application"""
    approved_state_map = {True: ApplicationStates.APPROVED, False: ApplicationStates.REJECTED}
    if is_at_least_role(current_user=current_user, role=min_update_role):
        application_from_db = crud.get_application(database, application_id)
        if not application_from_db.status == ApplicationStates.PENDING:
            raise HTTPException(status_code=400, detail="The application must be pending")

        updated_application = crud.change_state_of_application(
            database=database,
            application_id=application_id,
            new_state=approved_state_map[data.approved]
        )
        if updated_application:
            if data.approved:
                await create_user_from_application(
                    database=database,
                    application=updated_application
                )
            else:
                await send_fail_mail(updated_application)
            return updated_application
        raise HTTPException(status_code=404, detail="Application not found")
