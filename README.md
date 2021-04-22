# HackClub Website Backend

## Requirements
- Docker(With compose): Container tool
Verify by
```
docker -v
docker-compose -v
```  

## Running the app
`$ docker-compose up`
- Add `--build` to rebuild the image if needed.
- Add `-d` to run in detached mode(No Output from uvicorn process)
- `./app` & `./alembic` are mounted as volumes to refresh changes without rebuilding the image


## Running Migrations
Make migrations using

```
source scripts/make_migrations.sh
```

Migrate the database using

```
source scripts/migrate.sh
```

## Run pylint

```
source scripts/lint.sh
```

### Setting up docker remote interpreter for PyCharm IDE
Checkout this [blog](https://blog.jetbrains.com/pycharm/2015/12/using-docker-in-pycharm/), to allow code inspections by the IDE without installing any packages.