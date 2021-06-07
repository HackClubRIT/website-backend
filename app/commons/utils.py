"""
Common Utils
"""
from fastapi_mail import MessageSchema
from app.settings import FASTAPI_MAIL_INSTANCE


async def send_email(receivers, subject, body, subtype="html", template=None):
    """Send Mail"""
    message = MessageSchema(
        subject=subject,
        recipients=receivers,
        body=body,
        subtype=subtype
    )
    await FASTAPI_MAIL_INSTANCE.send_message(message, template)
