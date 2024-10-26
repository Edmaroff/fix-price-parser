import os
import re
import time
from typing import Dict, Optional, Union

import scrapy
from dotenv import load_dotenv
from scrapy.http import HtmlResponse, TextResponse

from app.items import ProductItem
from app.settings import ALLOWED_DOMAINS, COOKIES, START_URLS

load_dotenv()


class FixPriceSpider(scrapy.Spider):
    name = "fix_price"

    allowed_domains = ALLOWED_DOMAINS
    start_urls = START_URLS

    def start_requests(self):
        """
        Генерация начальных запросов с опциональной настройкой прокси
        Если переменные окружения для прокси заданы, запросы будут идти через прокси
        """
        # Проверка на наличие переменных окружения для прокси
        proxy_user = os.getenv("PROXY_LOGIN")
        proxy_pass = os.getenv("PROXY_PASSWORD")
        proxy_host = os.getenv("PROXY_IP")
        proxy_port = os.getenv("PROXY_PORT")

        # Настройка прокси-адреса, если все переменные окружения заданы
        proxy_address = (
            f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
            if all([proxy_user, proxy_pass, proxy_host, proxy_port])
            else None
        )

        cookies = COOKIES  # Задаем куки для Екатеринбурга

        # Генерация запросов на каждую начальную страницу
        for url in self.start_urls:
            request = scrapy.Request(
                url=url,
                callback=self.parse_main_page,
                cookies=cookies,
            )

            # Устанавливаем прокси, если он задан
            if proxy_address:
                request.meta["proxy"] = proxy_address

            yield request

    def parse_main_page(self, response: Union[HtmlResponse, TextResponse]):
        """
        Парсинг главной страницы для сбора ссылок на товары и пагинации
        """
        self.logger.info("Парсинг главной страницы: %s", response.url)

        # Извлечение ссылок на товары
        product_links = response.css("a.title::attr(href)").extract()
        for link in product_links:
            full_url = response.urljoin(link)
            yield scrapy.Request(url=full_url, callback=self.parse_product_page)

        # Обработка пагинации
        next_page_links = response.css(
            ".pagination.pagination a.number::attr(href)"
        ).extract()
        if next_page_links:
            for next_link in next_page_links[1:]:
                yield response.follow(next_link, callback=self.parse_main_page)

    def parse_product_page(self, response: Union[HtmlResponse, TextResponse]):
        """
        Извлечение данных о продукте, таких как цена, название, скидка и метаданные
        """
        self.logger.info("Парсинг страницы товара: %s", response.url)

        try:
            special_price_json = response.xpath(
                "//script[contains(text(), 'specialPrice')]/text()"
            ).get()
            special_price = self.extract_price(special_price_json)
            original_price = self.extract_original_price(response)
            sale_info = self.calculate_discount(original_price, special_price)
        except Exception as e:
            self.logger.error("Ошибка при извлечении цен для %s: %s", response.url, e)
            special_price, original_price, sale_info = None, None, None

        # Извлечение других данных о товаре
        item_data = {
            "timestamp": int(time.time()),
            "RPC": response.css("span.value::text").get(default="").strip(),
            "url": response.url,
            "title": response.css("h1.title::text").get(default="").strip(),
            "brand": response.css(".properties p:nth-child(1) .value a::text")
            .get(default="")
            .strip(),
            "marketing_tags": response.css("p.special-auth::text").get() or "Нет меток",
            "section": [
                section.strip()
                for section in response.css("div.breadcrumbs span::text").extract()
                if section.strip()
            ],
            "price_data": {
                "current": special_price or original_price,
                "original": original_price,
                "sale_tag": sale_info,
            },
            "assets": {
                "main_image": response.css(
                    "div.product-images img.normal::attr(src)"
                ).get()
                or "Нет изображения",
                "set_images": response.css(
                    "div.product-images link[itemprop='contentUrl']::attr(href)"
                ).extract(),
                "view_zoom": response.css(
                    "div.product-images img.zoom::attr(src)"
                ).extract(),
            },
            "metadata": self.extract_metadata(response),
        }
        yield ProductItem(item_data)

    def extract_price(self, special_price_json: Optional[str]) -> Optional[float]:
        """
        Извлекает цену со скидкой из JSON в тексте страницы
        """
        if special_price_json:
            match = re.search(r'price:"([^"]+)"', special_price_json)
            if match:
                return float(match.group(1))
        return None

    def extract_original_price(
        self, response: Union[HtmlResponse, TextResponse]
    ) -> Optional[float]:
        """
        Извлекает исходную цену товара из метатегов
        """
        price_meta = response.css(
            "div.price-quantity-block > div > meta[itemprop='price']"
        )
        if price_meta:
            return float(price_meta.attrib.get("content", "0"))
        return None

    def calculate_discount(
        self, original_price: Optional[float], special_price: Optional[float]
    ) -> Optional[str]:
        """
        Рассчитывает процент скидки, если специальная цена меньше оригинальной
        """
        if original_price and special_price and original_price > special_price:
            discount = ((original_price - special_price) / original_price) * 100
            return f"Скидка {discount:.2f}%"
        return None

    def extract_metadata(
        self, response: Union[HtmlResponse, TextResponse]
    ) -> Dict[str, Optional[str]]:
        """
        Извлекает метаданные о товаре, включая описание и дополнительные свойства
        """
        metadata = {
            "__description": response.css(".product-details .description::text")
            .get(default="")
            .strip()
        }
        for prop in response.css("div.properties p.property"):
            key = prop.css("span.title::text").get()
            value = prop.css("span.value::text").get()
            if key and value:
                metadata[key.strip()] = value.strip()
        return metadata
