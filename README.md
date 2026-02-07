# DB LLM

## venv

```sh
make venv
```

### activate

```sh
source .venv/bin/activate
deactivate
```

## Docker

```shell
make up
```

### migrate

```sh
# create migrate file
docker-compose run web python manage.py makemigrations defaultdb
# migrate
docker-compose run web python manage.py migrate
```

### commands

```sh
docker-compose run web python manage.py model_to_document
```

### php my admin

`http://localhost:8080`

### down

```shell
make down
make down_volume
docker images -qa | xargs docker rmi
```
