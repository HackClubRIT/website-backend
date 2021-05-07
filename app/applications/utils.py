"""
Application Utils
"""
from sqlalchemy.orm import Session
from app.users import crud as user_crud
from app.users.roles import Roles
from app.commons.utils import send_email
from app.users.schemas import UserCreate


async def create_user_from_application(database: Session, application):
    """Create user after application has been approved and send email"""
    user = UserCreate(
        role=Roles.USER,
        # Ensure this password is >= 8 characters
        password="password",
        email=application.email,
        name=application.name
    )
    # FUTURE FEATURE
    # user_crud.create_user(database=database, user=user)
    await send_email(
        template="application_success.html",
        body={"user": user},
        receivers=[user.email],
        subject="Your application for HackClubRIT"
    )



async def send_fail_mail(application):
    """Send application rejected mail"""
    await send_email(
        template="application_fail.html",
        body={"name": application.name},
        subject="Your application for HackClubRIT",
        receivers=[application.email]
    )
