# HackClub Website Backend

### Table of Contents
- [Requirements](#requirements)
- [Running the app](#running-the-app)
- [Running scripts inside container](#running-scripts)
    - [Running Migrations](#running-migrations)
    - [Running pylint](#run-pylint)
    - [Running tests](#run-tests)
- [Environment Variables](#environment-variables)  
- [Json Schemas](#json-schemas)
    - [User Receive](#user-receive)
    - [User Create](#user-create)
    - [User Update](#user-update)
    - [ApplicationView](#applicationview)
    - [ApplicationCreate](#applicationcreate)
- [Endpoints](#endpoints)
- [PyCharm Docker Setup](#setting-up-docker-remote-interpreter-for-PyCharm-IDE)

### Requirements
- Docker(With compose): Container tool

Verify by
```
docker -v
docker-compose -v
```  

### Running the app
`$ docker-compose up`
- Add `--build` to rebuild the image if needed.
- Add `-d` to run in detached mode(No Output from uvicorn process)
- `./app` & `./alembic` are mounted as volumes to refresh changes without rebuilding the image


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
| ALLOWED_ORIGINS | List of allowed origins in production | List as Json String | - | NO |
| SECRET_KEY | 64 digit hexadecimal string used for encryption | String | - | YES |
| DEBUG | Is Debug Mode | Boolean as String | true | NO |
| ALLOW_RELOAD | Pass --reload param to uvicorn run server cmd | Boolean as String | false | NO |
| TEST_DB | Test Database URL | Url String | - | NO |

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


### Endpoints
| URL | DESCRIPTION |METHOD | PARAMS | AUTHENTICATED | RESPONSE |
| --- | --- | --- | --- | --- | --- |
| `/auth/user/{user_id}` | Get User By ID | GET | - | No | [User](#user-receive) |
| `/auth/user` | Create new User(DEBUG ONLY) | POST | [UserCreate](#user-create) | No | [User](#user-receive) |
| `/auth/user/{user_id}` | Update Existing User | PATCH | [UserUpdate](#user-update) | Yes |  [User](#user-receive) |
| `/auth/user/{user_id}` | Soft Delete User By ID | DELETE | - | Yes |  - |
| `/auth/token` | Return token by submitting credentials | POST | `{"email": STRING, "password": STRING}` | No | `{"access_token": "string", "token_type": "string"}` |
| `/application` | View all pending applications | GET | - | Yes | [List(ApplicationView)](#applicationview) |
| `/application/{application_id}` | View application by ID | GET | - | No | [ApplicationView](#applicationview) |
| `/application/{application_id}` | Approve/Reject Application | PATCH | `{"approved": BOOLEAN}` | Yes | - |  


### Setting up docker remote interpreter for IDEs
VS Code, PyCharm - [Blog](https://dev.to/alvarocavalcanti/setting-up-a-python-remote-interpreter-using-docker-1i24)
