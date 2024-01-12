# API Flask into PostgreSQL

## Setup PostgreSQL DB as in TP1

```sh
docker pull totofunku/sql-cours
```

```sh
docker pull dpage/pgadmin4:latest
```

```sh
docker run --name postgresql -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=adminadmin -p 5432:5432 -v /data:/var/lib/postgresql/data -d totofunku/sql-cours
```

```sh
docker run --name my-pgadmin -p 82:80 -e "PGADMIN_DEFAULT_EMAIL=pgadmin4@pgadmin.org" -e "PGADMIN_DEFAULT_PASSWORD=test1234" -d dpage/pgadmin4
```

Restore the DB in the new server using the `dvdrental-2.tar` file.

## Move to /app

```sh
cd /app
```

## Build the docker image

```sh
docker build -t api-image .
```

## Lauch an instance of this image

```sh
docker run -p 8080:8080 --name api-container api-image
```