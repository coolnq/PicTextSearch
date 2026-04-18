# PicTextSearch

Текстовый поиск изображений через Яндекс (асинхронно и синхронно).

Библиотека предоставляет удобный интерфейс для поиска изображений по текстовому запросу с использованием поисковой системы **Яндекс.Картинки**. Поддерживает как асинхронный, так и синхронный режимы работы, настройку прокси, пользовательских заголовков, cookies и таймаутов.

---

## 📦 Установка

```bash
pip install git+https://github.com/yourname/pictextsearch.git
```

Или добавьте в `pyproject.toml` / `requirements.txt`:

```toml
pictextsearch @ git+https://github.com/yourname/pictextsearch.git
```

### Зависимости

- `httpx` (с поддержкой HTTP/2)
- `lxml`
- `pyquery`

---

## 🚀 Быстрый старт

### Асинхронный пример

```python
import asyncio
from PicTextSearch import Network, Yandex

async def main():
    async with Network() as client:
        yandex = Yandex(client=client)
        response = await yandex.search("кот в сапогах", page=1)

        print(f"URL результатов: {response.url}")
        for item in response.raw:
            print(f"Название: {item.title}")
            print(f"Изображение: {item.url}")
            print(f"Миниатюра: {item.thumbnail}")
            print(f"Размер: {item.size}")
            print(f"Источник: {item.source}")
            print(f"Описание: {item.content}")
            print("-" * 50)

asyncio.run(main())
```

### Синхронный пример

```python
from PicTextSearch.sync import Yandex

yandex = Yandex()
response = yandex.search("кот в сапогах", page=1)

for item in response.raw:
    print(item.title, item.url)
```

> Синхронная обёртка создаётся автоматически с помощью `syncify` (адаптировано из Telethon). Все публичные асинхронные методы заменяются на синхронные.

---

## 🔧 Конфигурация

### Класс `Network`

Управляет HTTP-клиентом. Может использоваться как асинхронный контекстный менеджер.

| Параметр      | Тип               | По умолчанию | Описание                                    |
|---------------|-------------------|--------------|---------------------------------------------|
| `proxies`     | `str \| None`      | `None`       | Прокси (например, `"http://127.0.0.1:1080"`) |
| `headers`     | `dict \| None`     | `None`       | Дополнительные заголовки                    |
| `cookies`     | `str \| None`      | `None`       | Cookies в формате `"key1=value1; key2=value2"` |
| `timeout`     | `float`            | `30`         | Таймаут запроса (секунды)                   |
| `verify_ssl`  | `bool`             | `True`       | Проверять SSL-сертификаты                   |
| `http2`       | `bool`             | `False`      | Использовать HTTP/2                         |

Пример с прокси и cookies:

```python
network = Network(
    proxies="http://127.0.0.1:1080",
    cookies="NID=xxx; another=yyy",
    timeout=60
)
```

### Класс `Yandex`

Основной класс для поиска.

```python
Yandex(
    base_url: str = "https://yandex.com/images/search",
    client: AsyncClient | None = None,
    proxies: str | None = None,
    headers: dict | None = None,
    cookies: str | None = None,
    timeout: float = 30,
    verify_ssl: bool = True,
    http2: bool = False
)
```

**Метод `search`**:

```python
async def search(query: str, page: int = 0, **kwargs) -> YandexResponse
```

- `query` – текст поискового запроса.
- `page` – номер страницы (начиная с 0).
- Возвращает объект `YandexResponse`.

---

## 📄 Структура ответа

### `YandexResponse`

| Атрибут   | Тип                    | Описание                                   |
|-----------|------------------------|--------------------------------------------|
| `url`     | `str`                  | Ссылка на страницу с результатами поиска   |
| `origin`  | `PyQuery`              | Сырой HTML-ответ (обёрнутый в PyQuery)     |
| `raw`     | `list[YandexItem]`     | Список найденных изображений               |

### `YandexItem`

| Атрибут     | Тип     | Описание                          |
|-------------|---------|-----------------------------------|
| `title`     | `str`   | Заголовок изображения             |
| `url`       | `str`   | Прямая ссылка на изображение      |
| `thumbnail` | `str`   | Ссылка на миниатюру               |
| `size`      | `str`   | Размеры (например, `"1920x1080"`) |
| `source`    | `str`   | Домен-источник                    |
| `content`   | `str`   | Описание / контекст               |
| `origin`    | `Any`   | Сырые данные из ответа            |

---

## 🧪 Разработка

### Установка для разработки

```bash
git clone https://github.com/yourname/pictextsearch.git
cd pictextsearch
uv sync --extra dev
pre-commit install
```

### Инструменты

- **Ruff** – линтинг и форматирование (конфигурация в `pyproject.toml`)
- **Mypy** / **Basedpyright** – статическая типизация
- **Pytest** – тесты (лежат в `tests/`)
- **Pre-commit** – хуки для автоматической проверки

### Запуск линтеров

```bash
ruff check .
ruff format --check
mypy PicTextSearch
basedpyright PicTextSearch
```

### Тестирование

```bash
pytest tests/
```

---

## 📜 Лицензия

Проект распространяется под лицензией **MIT**.

---

## 🙏 Благодарности

Основано на наработках проекта [PicImageSearch](https://github.com/kitUIN/PicImageSearch).  
Синхронная обёртка адаптирована из [Telethon](https://github.com/LonamiWebs/Telethon).

---

## ⚠️ Примечание

На данный момент поддерживается только поиск через **Яндекс.Картинки**.  
Поддержка Google, Bing и других движков может быть добавлена в следующих версиях.