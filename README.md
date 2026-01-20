# drizzle-llm

## init

```shell
npm i
```

## db

```shell
docker-compose up -d
# generate migrate file
npm run drizzle:generate
# migrate
npm run drizzle:migrate
```

### php my admin

`http://localhost:8080`

## fixture

```shell
npx ts-node ./src/load-fixture.ts
```

## docker

```shell
docker-compose down
docker-compose down -v
docker images -qa | xargs docker rmi
```
