<img src="https://img.shields.io/badge/python-3.12-blue" alt="Python version"/> <img src="https://img.shields.io/badge/Scrapy-2.11.2-blue" alt="Scrapy Version"/>
<h1>Fix Price Parser</h1>
<p>Парсер для интернет-магазина <a href="https://fix-price.com" target="_blank">Fix Price</a>, написанный с использованием Scrapy. Собирает данные о товарах из заданных категорий и сохраняет результаты в формате JSON.</p>

<details>
  <summary style="font-size: 1.3em;"><b>Структура данных товара</b></summary>
  <pre>
{
    "timestamp": int,               # Дата и время сбора товара в формате timestamp.
    "RPC": "str",                   # Уникальный код товара.
    "url": "str",                   # Ссылка на страницу товара.
    "title": "str",                 # Заголовок/название товара.
    "marketing_tags": ["str"],      # Список маркетинговых тэгов, например ['Популярный', 'Акция'].
    "brand": "str",                 # Бренд товара.
    "section": ["str"],             # Иерархия разделов, например ['Игрушки', 'Интерактивные игрушки'].
    "price_data": {
        "current": float,           # Цена со скидкой, если скидки нет то = original.
        "original": float,          # Оригинальная цена.
        "sale_tag": "str"           # Например: "Скидка 20%".
    },
    "stock": {
        "in_stock": bool,           # Наличие товара в магазине.
        "count": int                # Количество в наличии, если доступно, иначе 0.
    },
    "assets": {
        "main_image": "str",        # Ссылка на основное изображение товара.
        "set_images": ["str"],      # Ссылки на все изображения товара.
        "view360": ["str"],         # Ссылки на изображения в формате 360.
        "video": ["str"]            # Ссылки на видео.
    },
    "metadata": {
        "__description": "str",     # Описание товара.
        "KEY": "str",               # Дополнительные характеристики, например "Цвет", "Объем".
        "KEY": "str"
    },
    "variants": int                 # Количество вариантов товара (например, разные цвета).
}
  </pre>
</details>

<p><strong>Пример результата парсинга</strong> можно найти в <code>output/output_example.json</code></p>

<hr>

<h2>Запуск локально</h2>
<ol>
  <li>Клонируйте репозиторий:
    <pre><code>git clone https://github.com/Edmaroff/fix-price-parser</code></pre>
  </li>
  <li>Перейдите в директорию проекта:
    <pre><code>cd fix-price-parser</code></pre>
  </li>
  <li>Установите и активируйте виртуальное окружение для проекта <code>venv</code>:
    <pre><code>python -m venv venv
venv\Scripts\activate</code></pre>
  </li>
  <li>Установите зависимости из <code>requirements.txt</code>:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>Настройка Proxy <em>(опционально)</em>:
    <p>Если требуется использовать proxy, добавьте файл <code>.env</code> и заполните его, используя <code>.env_example</code> как шаблон.</p>
  </li>
  <li>Запустите парсер:
    <pre><code>scrapy crawl fix_price</code></pre>
    <p>Результаты сохраняются в папке <code>output</code> с автоматически сгенерированным именем файла (<code>fix_price_&lt;date&gt;.json</code>).</p>
  </li>
</ol>

<h2>Запуск с Docker</h2>
<ol>
  <li>Клонируйте репозиторий:
    <pre><code>git clone https://github.com/Edmaroff/fix-price-parser</code></pre>
  </li>
  <li>Перейдите в директорию проекта:
    <pre><code>cd fix-price-parser</code></pre>
  </li>
  <li>Настройка Proxy <em>(опционально)</em>:
    <p>Если требуется использовать proxy, добавьте файл <code>.env</code> и заполните его, используя <code>.env_example</code> как шаблон.</p>
  </li>
  <li>Соберите Docker-образ:
    <pre><code>docker-compose build</code></pre>
  </li>
  <li>Запустите контейнеры:
    <pre><code>docker-compose up</code></pre>
  </li>
</ol>
---