# Widget recommendation using Multi-armed bandits

## Описание проекта
Выполненная работа по разработке системы рекомндации виджетов для пользователя
основываясь на времени их просмотра.

Проект состоит из 2 программ:

    1. Сервис - иммитирует поведение пользователя (Среда). Генерирует время просмотра каждого виджета из логнормального распределения.

    2. Агент - реализация многоруких бандитов. На выбор есть 2 подхода - эпсилон жадный и Upper Confidence Bound.


Агент посылает набор виджетов, представленных в ввиде конкретного `id` и корректирует свой выбор, основываясь на времени, который пользователь потратил на просмотр всех виджетов. Даже после нахождения оптимальный виджетов, агент продолжает их слать. Сервис принимает на вход список виджетов и отдает время их просмотра. Также логирует информацию о наборе и времени в отдельный файл `timespent.log`.

## Описание программ

Среда и Агент представленны 2 классами - `User` и `BanditAgent`.

```
user = User( preferences ),
где preferences - словарь с {widget_id: {mean: 2, sigma: 2}}, который находится в 
configs/user_service/widget_preferences.yaml и который задает параметры логнормального распределения.

user.watch_widgets( widget_set ),
где watch_widgets - набор widget_id из n элементов (n=3 по заданию).
Возвращает время, которое "пользователь потратил на просмотр виджетов", сэмлируя из numpy.radnom.lognormal.

```

```
bandit = BanditAgent(
    bandit_conf,
    bandit_name,
    host_adresss,
), 

где:
bandit_conf - конфиг с параметрами для стратегий. Берется из config/agent/bandits_config.yaml.
bandit_name - стратегия бандита - epsilon_greedy или ucb.
host_adress - адрес куда Агент посылает виджеты.

```

## Структура проекта

Реализация сервиса и агента представленны в директориях `user_service` и `agents` соответственно.

Сервис (Среда):
```
├── user_service/
│    ├── __init__.py
│    ├── app.py                     <-- entry point для Сервиса
│    ├── blueprints/ 
│    │   ├── __init__.py
│    │   └── user_routes.py         <-- модуль для получения запросов к пользователю
│    ├── containers/
│    │   ├── __init__.py
│    │   └── user_container.py      <-- Контейнер пользователя для dependency injection
│    ├── logger.py                  <-- Логер для Сервиса
│    ├── requirements_service.txt   <-- Необходимые зависимости для сервиса.
│    └── services/
│        ├── __init__.py
│        └── user.py                <-- Модель Пользователя.

```

Бандиты:
```
├── agents/
│   ├── __init__.py
│   ├── app.py                  <-- Entry point для работы Агента. Бесконечно отсылает запросы к Сервису(Среде).
│   ├── requirements_agent.txt  <-- Необходимые модули для Агента
│   └── src/
│       ├── __init__.py
│       ├── agent.py            <-- Реализация модели Агента.
│       ├── bandits.py          <-- Реализация алгоритмов многоруких бандитов.
│       └── base.py             <-- Абстракция для бандитов.

```
Конфиг файлы:
```
├── configs/
│   ├── agent/
│   │   └── bandits_config.yaml         <-- Конфиг с параметрами для разных бандитов
│   └── user_service/
│       ├── app.yaml                    <-- Конфиг с параметрами для запуска Flask приложения
│       └── widget_preferences.yaml     <-- Конфиг с параметрами для логнормального распределения для каждого
                                            виджета
```

`Dockerfile's`:
```
├── docker/
│   ├── user_service/
│   │   ├── Dockerfile              <-- Dockerfile for user_service container
│   │   └── bandits_config.yaml     <-- Generic .dockerignore
│   └── agent/
│       ├── Dockerfile              <-- Dockerfile for agent container
│       └── .dockerignore           <-- Generic .dockerignore
```


## Запуск проекта

По умолчанию запускается бандит со стратегией Upper Confident Bound.

### Локальный 
По умолчанию программы не предназначены, чтобы работать в локальном режиме. Однако это можно сделать при помощи пары простых действий.

Стоить обратить внимание на комментированный код в файлах `user_service/app.py` и `agents/app.py`.
Tак как я хотел сохранить общую структуру проекта,
(чтобы в его корне были конфиги для всего) то надо раскомментировать код под комментариями  `Local runnig`.

После этого файлы могут запускаться локально.

Также надо вручную установить все зависимости. Проект выполнялся на `Python 3.9.13`
```
    [Опционально создаем и активируем виртуальную среду]

    python -m pip install -r agents/requirements_agent.txt
    python -m pip install -r user_service/requirements_service.txt
```

```
    python user_service/app.py &
    python agents/app.py <bandit_name>
```


### Запуск при помощи докера
#### Docker-compose

Для того, чтобы запустить сервис при помощи `docker-compose` необходим выполнить команды:

    docker-compose build --no-cache

    docker-compose up -d

#### Separate docker containers

Если по какой-то причине `docker-compose` откзывается работать, то можно запустить оба контейнера поочереди.

```
# создаем сеть для того, чтобы контейнеры общались
docker network create my_network

# билдим образы
docker build -t user_service -f docker/user_service/Dockerfile .

docker build -t agent -f docker/agent/Dockerfile .

# запускаем оба контейнера по очереди
docker run -d --name user_service --network my_network -p 8000:8000 user_service

docker run -d --name agent --network my_network -p 8001:8001 agent
```

где `user_service` и `agent` - имена для образов и контейров. Также стоит обратить внимание, что контейнеры должны быть на разных портах.

## Проверяем, что все работает

```
Параметры для логнормального распределения у виджетов заданы так, что самым долгопросматриваемым набором виджетов
окажется [5, 2, 8] или [5, 9, 2] (порядок расположения не играет роли).
```

После запуска обеих программ, сервис начнет генеровать логи в `timespent.log` в ввиде:

```
2023-08-03 20:56:08,457 : INFO : USER_TIMESPENT : 9 8 7 61.502573023079094
2023-08-03 20:56:08,970 : INFO : USER_TIMESPENT : 9 8 7 32.10672505717693
2023-08-03 20:56:09,497 : INFO : USER_TIMESPENT : 9 8 7 44.39964366660119
2023-08-03 20:56:10,011 : INFO : USER_TIMESPENT : 9 8 7 49.452892283891
```

Если все запущено в контейрах:

1. Если мы хотим просто посмотреть логи:
    ```
    docker-compose exec user_service bash
    cat timespent.log

    или если запущено в разных контейнерах:

    docker exec -it user_service bash
    cat timespent.log
    ```

2. Если хотим забрать логи:
    ```
    docker-compose cp user_service:/user_service/timespent.log  [dest_path]
    
    или

    docker cp user_service:/user_service/timespent.log  [dest_path]
    ```


