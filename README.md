# Herzendo

## Instalación

1. Copia tu archivo `.env` y luego añadele de nuevo a tus necesidades de acuerdo a tus necesidades

    ```bash
    cp .env.example .env
    ```

2. Genera una clave fuerte para la aplicación con la siguiente información

    ```bash
    CLAVE_SEGURA=$(openssl rand -base64 64 | tr -dc 'a-zA-Z0-9!@#$%^&*(-_=+)' | head -c 50) && \
        sed -i "s|DJANGO_SECRET_KEY=<CLAVE_SEGURA>|DJANGO_SECRET_KEY=$CLAVE_SEGURA|" .env
    ```

3. Por favor genera tus crendenciales seguras para la base de datos, como por ejemplo con el siguiente comando

    ```bash
    mkdir -p credenciales/database
    openssl rand -base64 32 > credenciales/database/root_password.txt
    openssl rand -base64 32 > credenciales/database/user_password.txt
    openssl rand -base64 32 > credenciales/database/admin_password.txt
    mkdir -p credenciales/superuser
    openssl rand -base64 32 > credenciales/superuser/password.txt
    ```

4. Crea tus contenedores con el comando

    ```bash
    docker compose build
    ```

## Uso

1. _(Sólo por primera vez o cambios en la base de datos)_ Por favor, genera una migración y crea un superusuario con el siguiente comando

    ```bash
    docker compose up db -d && sleep 30 &&
    docker compose -f docker-compose.yml -f docker-compose.migrate.yml up herzendo &&
    docker compose -f docker-compose.yml -f docker-compose.superuser.yml up herzendo
    ```

2. Inicia los contedores con

    ```bash
    docker compose -f docker-compose.yml up -d
    ```

## Desarrollo

### Configuración

Sincroniza tus cambios locales con los del contenedor al usar el comando

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up herzendo --build
```

### Panel de Administración

La aplicación tiene un panel de administración integrado que puedes acceder a través de [http://<APP_URL>:<HERZENDO_PUERTO>/admin/](http://<APP_URL>:<HERZENDO_PUERTO>/admin/])
