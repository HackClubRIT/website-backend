"""
Test Event Application
"""
# pylint: disable=use-a-generator
import datetime
from random import randint
from app.test import FeatureTest
from app.users.roles import Roles
from app.users.crud import create_user, get_user
from app.users.schemas import UserCreate
from .crud import create_event, get_event_by_id, get_all_events, create_image
from .schemas import EventBaseSerializer


class EventTest(FeatureTest):
    """
    Event Test Utils
    """
    def __init__(self, database):
        self.events = []
        super().__init__(database)

    def create_image(self):
        """
        Create an image in DB
        """
        return create_image(database=self.database_conn,
                            img_url="https://%s.com" % self.random_string())

    def create_event_object(self, image_id=None):
        """
        Create event object (Not saved in DB)
        """
        if image_id is None:
            image_id = self.create_image().id
        date = datetime.datetime.now() + datetime.timedelta(days=-1 * randint(0, 2))
        return EventBaseSerializer(
            name=self.random_string(),
            registration_link="https://%s.com" % self.random_string(),
            description=self.random_string(),
            date=date.strftime("%Y-%m-%dT%H:%M:%S"),
            image_id=image_id,
        )

    def additional_setup(self, **kwargs):
        """
        Create Test Events
        """
        image = self.create_image()
        self.events = [
            create_event(self.database_conn, self.create_event_object(image.id),
                         self.users[Roles.ADMIN])
            for _ in range(10)]


def test_event_list(test_event_instance: EventTest):
    """
    TEST GET /content/events/
    """
    response = test_event_instance.client.get("/content/events/")
    assert response.status_code == 200
    event_ids = [i["id"] for i in response.json()]
    assert all([get_event_by_id(test_event_instance.database_conn, i) for i in event_ids])

    response = test_event_instance.client.get("/content/events/?upcoming=true")
    assert response.status_code == 200
    assert all([datetime.datetime.now() < event["date"] for event in response.json()])


def test_event_retrieve(test_event_instance: EventTest):
    """
    TEST GET /content/events/{event_id}/
    """
    for event in test_event_instance.events:
        response = test_event_instance.client.get("/content/events/%d/" % event.id)
        assert response.status_code == 200


def test_event_create(test_event_instance: EventTest):
    """
    TEST POST /content/events/
    """
    event = test_event_instance.create_event_object()
    count_event_before_insert = len(get_all_events(database=test_event_instance.database_conn))
    test_event_instance.assert_user_permissions(
        url="/content/events/",
        method="POST",
        users={
            Roles.ADMIN: 201,
            Roles.MODERATOR: 201,
            Roles.USER: 403
        },
        data=event.json()
    )
    assert len(get_all_events(database=test_event_instance.database_conn)) - 2 \
           == count_event_before_insert


def update_event(test_instance, event, user_id, success):
    """
    Utility fn to update an event
    """
    user = get_user(database=test_instance.database_conn, user_id=user_id)
    new_name = test_instance.random_string()
    response = test_instance.client.patch(
        "/content/events/%d/" % event.id,
        headers=test_instance.set_auth_from_user(user),
        json={"name": new_name}
    )
    if success:
        assert response.status_code == 200
        # modified_event = get_event_by_id(database=test_instance.database_conn, event_id=event.id)
        # assert modified_event.name == new_name
    else:
        assert response.status_code == 403


def test_event_update(test_event_instance: EventTest):
    """
    TEST PATCH /content/events/{event.id}
    """
    mod_event = create_event(database=test_event_instance.database_conn,
                             event=test_event_instance.create_event_object(),
                             current_user=test_event_instance.users[Roles.MODERATOR])

    new_mod_user = create_user(
        database=test_event_instance.database_conn,
        user=UserCreate(role=Roles.MODERATOR,
                        email=test_event_instance.random_email(),
                        name=test_event_instance.random_string(),
                        password=test_event_instance.default_password))

    response_map = {
        new_mod_user.id: False,
        test_event_instance.users[Roles.MODERATOR].id: True,
        test_event_instance.users[Roles.ADMIN].id: True,
        test_event_instance.users[Roles.USER].id: False
    }
    for user, success_state in response_map.items():
        update_event(test_event_instance, mod_event, user, success_state)
