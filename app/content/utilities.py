"""
Content utils
"""
import uuid
import aiofiles
from fastapi import HTTPException, UploadFile
from cloudinary.uploader import upload
from app.content.crud import get_event_by_id, create_image
from app.exceptions import USER_FORBIDDEN
from app.settings import DEBUG, CLOUDINARY_OVERRIDE
from app.users.role_mock_middleware import is_at_least_role
from app.users.roles import Roles

IMG_MIMES = ("image/jpeg", "image/png")


def verify_user_permissions_to_update_event(user, event_id, database):
    """
    :param user: User Object, intended as logged in user
    :param event_id: Event Id
    :param database: database session
    """
    is_at_least_role(Roles.MODERATOR, user)
    db_event = get_event_by_id(database, event_id)
    if db_event.user_id != user.id and user.role != Roles.ADMIN:
        raise HTTPException(
            status_code=403,
            detail=USER_FORBIDDEN)

    return db_event


def validate_image(img: UploadFile):
    """
    Check if file is valid image
    """
    if img.content_type not in IMG_MIMES:
        raise HTTPException(
            status_code=422,
            detail="Image should be either JPG/PNG format"
        )
    return True


async def handle_uploaded_image(img: UploadFile, database):
    """
    Store File To Cloud and Db
    """
    if DEBUG and not CLOUDINARY_OVERRIDE:
        host = "http://127.0.0.1:8000"
        base_dir = "app/images"
        new_file_name = str(uuid.uuid4()) + "." + img.filename.split(".")[-1]
        async with aiofiles.open("%s/%s" % (base_dir, new_file_name), 'wb') as out_file:
            while content := await img.read(1024):
                await out_file.write(content)
        url = "%s/images/%s" % (host, new_file_name)
        return create_image(database=database, img_url=url)

    img_bytes = bytearray()
    while content := await img.read(1024):
        img_bytes += content

    upload_res = upload(img_bytes)
    return create_image(database=database, img_url=upload_res["secure_url"])
