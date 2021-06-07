# HackClub Website Backend

### Table of Contents
- [Requirements](#requirements)
- [Running the app](#running-the-app)
- [pgAdmin]  
- [Running scripts inside container](#running-scripts)
    - [Running Migrations](#running-migrations)
    - [Running pylint](#run-pylint)
    - [Running tests](#run-tests)
- [Environment Variables](#environment-variables)  
    - [Email Variables](#email-variables)
- [Json Schemas](#json-schemas)
    - [User Receive](#user-receive)
    - [User Create](#user-create)
    - [User Update](#user-update)
    - [ApplicationView](#applicationview)
    - [ApplicationCreate](#applicationcreate)
- [Endpoints](#endpoints)
- [Image Uploads](#image-upload)  
- [PyCharm Docker Setup](#setting-up-docker-remote-interpreter-for-PyCharm-IDE)

### Requirements
- Docker(With compose): Container tool

Verify by
```
docker -v
docker-compose -v
```  

### Running the app
- Create a `email.env` and `cloudinary.env` file to prevent docker errors.
`$ docker-compose up`
- Add `--build` to rebuild the image if needed.
- Add `-d` to run in detached mode(No Output from uvicorn process)
- `./app` & `./alembic` are mounted as volumes to refresh changes without rebuilding the image


### pgAdmin

You can use pgAdmin by visiting [localhost:9000](http://localhost:9000).
- Username: `admin@hackclubrit.com`
- Password: `password`
- Get DB container IP by running `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' hackclub-db`
- Add server by entering
  - Host: IP of docker container
  - Database User: `user`
  - Database Password: `password`
- The name of the database is `hackclubdb`  

### Running Scripts

Various scripts for different purposes has been made in the `./scripts` directory. 
They connect to the remote container from host and run commands inside the container.

Set your docker container name(if you changed it) in `./scripts/set_env.sh`

#### Running Migrations

Make migrations using

```
sh scripts/make_migrations.sh "<NAME>"
```

Migrate the database using

```
sh scripts/migrate.sh
```

#### Run pylint

[Pylint](https://pypi.org/project/pylint/) is a Python static code analysis tool which looks for programming errors, helps enforcing a coding standard, sniffs for code smells and offers simple refactoring suggestions.

```
sh scripts/lint.sh
```

#### Run tests

Run tests using pytest

```
sh scripts/test.sh
```

### Environment Variables

| NAME | DESC | TYPE | DEFAULT | REQUIRED |
| --- | --- | --- | --- | --- |
| DATABASE_URL | The database url | Url String | - | YES |
| ALLOWED_ORIGINS | List of allowed origins in production | List as Json String | \[*\] | NO |
| SECRET_KEY | 64 digit hexadecimal string used for encryption | String | Random Key | NO |
| DEBUG | Is Debug Mode | Boolean as String | true | NO |
| ALLOW_RELOAD | Pass --reload param to uvicorn run server cmd | Boolean as String | false | NO |
| TEST_DB | Test Database URL | Url String | - | NO |

#### Email Variables

These environment variables are stored in a separate `email.env` file(Ignored by git)

| NAME | DESC | TYPE | DEFAULT | REQUIRED |
| --- | --- | --- | --- | --- |
| EMAIL_USERNAME | Username(Generally same as FROM mail) | String | - | NO |
| EMAIL_PASSWORD | Password | String | - | NO |
| EMAIL_FROM | Email from which the mail is sent | Email | test@test.com | NO |
| EMAIL_PORT | The email port | Integer | - | NO |
| EMAIL_SERVER | The email server url | Url | - | NO |
| EMAIL_TLS | Use TLS | Boolean as String | false | NO |
| EMAIL_SSL | Use SSL | Boolean as String | false | NO |

#### Cloudinary Variables
| NAME | DESC | TYPE | DEFAULT | REQUIRED |
| --- | --- | --- | --- | --- |
| CLOUDINARY_URL | The url containing all cloudinary info | Url | - | NO |
| CLOUDINARY_OVERRIDE | Override default and use cloudinary for uploads | Boolean as String | false | NO |

### Json Schemas 

#### User Receive
```
{
    "email": STRING, 
    "role": ENUM(ADMIN, MODERATOR, USER), 
    "name": STRING, 
    "id": INTEGER, 
    "is_active": BOOLEAN
}
```

#### User Create
```
{
    "email": STRING, 
    "role": ENUM(ADMIN, MODERATOR, USER), 
    "name": STRING,
    "password": STRING
}
```

#### User Update
```
{
    "email": STRING[Optional],
    "name": STRING[Optional],
    "password": STRING[Optional]
}
```
#### ApplicationView
```
{
    "email": STRING,
    "data": JSON,
    "name": STRING,
    "id": INTEGER,
    "status": ENUM(PENDING, APPROVED, REJECTED),
    "created_date": DATE 
}
```
#### ApplicationCreate
```
{
  "email": STRING,
  "data": JSON,
  "name": STRING
}
```
#### FeedbackView
```
{
  "id": INTEGER,
  "content": STRING,
  "created_time": DATETIME
}
```

#### EventView
```
{
  "user": {
    "name": STRING,
    "id": INTEGER
  },
  "image": URL,
  "name": STRING,
  "registration_link": URL,
  "description": STRING,
  "date": ISODateTime,
  "image_id": INTEGER,
  "id": INTEGER
}
```

#### EventCreate
```
{
  "name": STRING,
  "registration_link": URL,
  "description": STRING,
  "date": ISODateTime,
  "image_id": INTEGER,
}
```


### Endpoints

**NOTE: All urls contain trailing /**

| URL | DESCRIPTION | METHOD | PARAMS | AUTHENTICATED | RESPONSE |
| --- | --- | --- | --- | --- | --- |
| `/auth/user/{user_id}/` | Get User By ID | GET | - | No | [User](#user-receive) |
| `/auth/user/` | Create new User(DEBUG ONLY) | POST | [UserCreate](#user-create) | No | [User](#user-receive) |
| `/auth/user/{user_id}/` | Update Existing User | PATCH | [UserUpdate](#user-update) | Yes |  [User](#user-receive) |
| `/auth/user/{user_id}/` | Soft Delete User By ID | DELETE | - | Yes |  - |
| `/auth/token/` | Return token by submitting credentials | POST as `formdata/x-www-form-urlencoded` | `{"email": STRING, "password": STRING}` | No | `{"access_token": "string", "token_type": "string"}` |
| `/application/` | View all pending applications | GET | - | Yes | [List(ApplicationView)](#applicationview) |
| `/application/{application_id}/` | View application by ID | GET | - | No | [ApplicationView](#applicationview) |
| `/application/{application_id}/` | Approve/Reject Application | PATCH | `{"approved": BOOLEAN}` | Yes | - |  
| `/content/feedback/` | Get all feedbacks | GET | - | No | [List(FeedbackView)](#feedbackview) |  
| `/content/feedback/{feedback_id}/` | View feedback by ID | GET | - | No | [FeedbackView](#feedbackview) |  
| `/content/feedback/` | Create a feedback | POST | `{"content": STRING}` | No | [FeedbackView](#feedbackview) |  
| `/content/events/` | List all events | GET | `{"upcoming": BOOL as STRING}` | No | [List(EventView)](#eventcreate) |
| `/content/events/{event_id}/` | Get event by ID | GET | - | No | [EventView](#eventcreate) | 
| `/content/events/` | Create Event | POST | [EventCreate](#eventcreate) | Yes | [EventView](#eventcreate) |
| `/content/events/{event_id}/` | Edit Event | PATCH | [EventView](#eventview)(all optional) | Yes | [EventView](#eventcreate) |
| `/content/events/{event_id}/` | Delete Event | DELETE | - | Yes | - |
| `/content/image/` | Upload Image | POST as  `multipart/formdata` | `{"img": File}` | Yes | `{"id":INT, "url": URL}` |   

### Image Upload

Create an `images` folder in `./app` for local development

Refer [flowchart](https://app.diagrams.net/#G1tj6X8M1Rj5z3mKeoaEpFfRRapOKb8Frn) for process flow.

### Setting up docker remote interpreter for IDEs
VS Code, PyCharm - [Blog](https://dev.to/alvarocavalcanti/setting-up-a-python-remote-interpreter-using-docker-1i24)
