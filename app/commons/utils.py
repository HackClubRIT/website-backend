"""
Common Utils
"""
from fastapi_mail import MessageSchema
from app.settings import fastapi_mail_instance


async def send_email(receivers, subject, body, subtype="html", template=None):
    """Send Mail"""
    message = MessageSchema(
        subject=subject,
        recipients=receivers,
        body=body,
        subtype=subtype
    )
    await fastapi_mail_instance.send_message(message, template)
