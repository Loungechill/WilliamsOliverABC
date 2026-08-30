# Williams Oliver ABC feed

Отдельный производный YML-фид для Яндекс Директа. Действующий репозиторий
`Loungechill/WilliamsOliver` и его фид не изменяются.

## Что делает сборка

1. Загружает исходный клиентский фид Williams Oliver.
2. Исключает offers, чьи `<vendor>` находятся в `blocked_vendors.txt`.
3. Читает опубликованный CSV листа `Williams Oliver` из Google Таблиц.
4. Сопоставляет данные строго по атрибуту `<offer id>` и столбцу `Offer ID`.
5. Добавляет каждому оставшемуся offer один элемент `<custom_label_0>`:
   - `1` — больше двух покупок;
   - `2` — одна или две покупки;
   - `3` — ноль покупок или Offer ID отсутствует в таблице.
6. Сохраняет прежнюю очистку предупреждений Яндекс Директа и проверяет XML.

GitHub Actions запускает сборку каждые четыре часа и публикует проверенный
`feed.xml` как стабильный release asset:

`https://github.com/Loungechill/WilliamsOliverABC/releases/download/feed-latest/feed.xml`

Cloudflare Worker из `worker.js` проксирует этот файл по отдельному адресу.

## Ручной запуск

```bash
python3 filter_feed.py \
  --source "https://williams-oliver.ru/api/feed/diginetica" \
  --stats-source "PUBLIC_GOOGLE_SHEETS_CSV_URL" \
  --blacklist blocked_vendors.txt \
  --output feed.xml
```

