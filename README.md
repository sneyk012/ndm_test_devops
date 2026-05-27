# Тестовый стенд: цепочка nginx и X-Forwarded-For

Решение тестового задания: несколько nginx в режиме reverse proxy передают в backend корректную цепочку `X-Forwarded-For` (IP клиента + IP каждого nginx на пути), при этом поддельный заголовок от клиента отбрасывается.
На тестовое задание ушло порядка 20 минут и несколько запросов в ИИ. 

## Ключевая логика (nginx)

Файл [`nginx/common/xff.conf`](nginx/common/xff.conf):

- Запросы с **edge-сети** (хост, `client`) — недоверенные: в upstream уходит `$remote_addr` + `$server_addr`, клиентский `X-Forwarded-For` **игнорируется**.
- Запросы из **internal-сети** (`10.10.10.0/24`, только nginx↔nginx↔app) — доверенные: к цепочке из заголовка добавляется `$server_addr` текущего hop'а.

Две сети в `docker-compose.yml` нужны, чтобы IP шлюза Docker (`172.x`) не попадал в список «доверенных прокси» — иначе подделка `X-Forwarded-For` с хоста проходила бы в backend.

Между nginx используются **фиксированные internal IP** в `upstream`, чтобы не уехать на edge-адрес из DNS Docker.
