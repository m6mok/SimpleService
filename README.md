# Проект SimpleService

## Описание

Production-ready минимальный шаблон сервиса на `Flask`, который будет включать в себя:

1. Логирование (`stdout`, `filestream`, `TelegramAPI`, `ClickHouse`)

2. Мониторинг ресурсов (`Prometeus`)

3. Систему тестирования (`pytest`)

4. Систему стилистического анализатора (`black`, `flake8`, `ruff`)

5. Систему статического анализатора (`mypy`)

6. Систему умной бесшовной канареечной выкатки

7. Менеджер пакетов (`astral-sh/uv`)

## Разработка

1. Запустите `devcontainer`

2. Запустите команду

    ```sh
    uv run src/simpleservice/main.py --env DEV --port 3000
    ```

## Локальный запуск

1. Соберите контейнер

    ```sh
    docker build -t simpleservice:prod .
    ```

2. Запустите контейнер

    ```sh
    docker run -d -p 8080:8080 --name my-prod-service simpleservice:prod \
        uv run src/simpleservice/main.py --env PROD --port 8080 --workers 4 --timeout 300
    ```
