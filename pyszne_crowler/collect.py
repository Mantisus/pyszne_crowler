import json
from collections.abc import Generator
from urllib.parse import urlencode

from lxml import html

from .config import API_URL, DOMAIN_URL


def category_parse(html_content: bytes, main_categories: bool = False) -> Generator:
    content = html.fromstring(html_content)
    content.make_links_absolute(DOMAIN_URL)
    categories_urls = content.xpath('//div[@class="delarea"]/a/@href')
    if main_categories:
        main_categories_urls = content.xpath('//a[@class="menucategorytd"]/@href')
        categories_urls.extend(main_categories_urls)
    return (item for item in categories_urls)


def region_parse(html_content: bytes) -> str | None:
    try:
        content = html.fromstring(html_content)
        script_data = content.xpath('//script[@id="__NEXT_DATA__"]/text()')[0]
        script_data = json.loads(script_data)
        location_data = script_data["props"]["appProps"]["preloadedState"]["discovery"][
            "location"
        ]["validation"]["result"]
    except Exception:
        return None
    payload_data = {
        "deliveryAreaId": location_data["deliveryAreaId"],
        "postalCode": location_data["takeawayPostalCode"],
        "lat": location_data["lat"],
        "lng": location_data["lng"],
        "limit": 0,
        "isAccurate": True,
    }
    return f"{API_URL}restaurants?{urlencode(payload_data)}"


def restorants_parse(json_content: bytes) -> Generator:
    data = json.loads(json_content)["restaurants"]
    for key in data:
        yield f"{API_URL}restaurant?slug={data[key]['primarySlug']}"


def restorant_parse(json_content: bytes) -> dict:
    data = json.loads(json_content)
    return {
        "name": data["brand"]["name"],
        "restaurants_url": data.get("minisiteUrl"),
        "telephone": data.get("restaurantPhoneNumber"),
        "street": data.get("location", {}).get("streetName"),
        "street_number": data.get("location", {}).get("streetNumber"),
        "city": data.get("location", {}).get("city"),
        "postal_code": data.get("location", {}).get("postalCode"),
        "rating": data.get("rating", {}).get("score"),
        "number_ratings": data.get("rating", {}).get("votes"),
    }
