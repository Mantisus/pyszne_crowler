import asyncio
from csv import DictWriter
from random import choices

from .async_client import AsyncHTTPClient
from .collect import category_parse, region_parse, restorant_parse, restorants_parse
from .config import API_HEADERS, NAVIGATE_HEADERS, OUTPUT_FILE, START_URL
from .utils.cache import url_cache
from .utils.logger import logger

client = AsyncHTTPClient()
URL_FILTER = set()
RESULTS = []


async def request(url: str, headers: dict) -> bytes | None:
    response = await client.get(url, headers=headers)
    if response.status_code == 429:
        await asyncio.sleep(20)
        raise Exception("Too Many Requests")
    return response.content if response.status_code == 200 else None


async def navigate_request(url: str) -> bytes | None:
    async with client.navigate_lock:
        return await request(url, headers=NAVIGATE_HEADERS)


async def api_request(url: str) -> bytes | None:
    headers = API_HEADERS.copy()
    headers["User-Agent"] = "".join(choices("qazxswedcvfrtgbnhyujmkiolp", k=5))
    async with client.api_lock:
        response = await request(url, headers=headers)
        return response


@url_cache
async def cat_request(url: str) -> bytes | None:
    return await navigate_request(url)


async def task_router(url: str, skip: bool = False) -> None:
    if not skip:
        if url in URL_FILTER:
            return
        URL_FILTER.add(url)
    try:
        if url == START_URL:
            await category_processing(url, main_categories=True)
        elif "v33/restaurant?" in url:
            await restaurant_processing(url)
        elif "v33/restaurants?" in url:
            await restaurants_processing(url)
        elif "/na-dowoz/" in url:
            await region_processing(url)
        else:
            await category_processing(url)
    except Exception as e:
        logger.info(f"Repeat {url} error {e}")
        asyncio.create_task(task_router(url, True))


async def region_processing(url: str) -> None:
    content = await navigate_request(url)
    if not content:
        logger.warning(f"Warning {url}")
        return
    region_restaurants_url = region_parse(content)
    if region_restaurants_url:
        asyncio.create_task(task_router(region_restaurants_url))


async def restaurants_processing(url: str) -> None:
    content = await api_request(url)
    if not content:
        raise Exception("Don't restaurants data")
    restaurans_urls = restorants_parse(content)
    if restaurans_urls:
        [asyncio.create_task(task_router(url)) for url in restaurans_urls]


async def restaurant_processing(url: str) -> None:
    content = await api_request(url)
    if not content:
        raise Exception("Don't restaurant data")
    data_item = restorant_parse(content)
    RESULTS.append(data_item)


async def category_processing(url: str, main_categories: bool = False) -> None:
    content = await cat_request(url)
    if not content:
        logger.warning(f"Warning {url}")
        return
    categories_urls = category_parse(content, main_categories=main_categories)
    [asyncio.create_task(task_router(url)) for url in categories_urls]


def save_csv(results: list) -> None:
    with open(OUTPUT_FILE, "w") as f:
        dict_writer = DictWriter(f, results[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(results)


async def check_tasks_complete() -> None:
    while len(asyncio.all_tasks()) > 1:
        logger.info(f"Tasks performed in the pool: {len(asyncio.all_tasks())}")
        await asyncio.sleep(5)


async def start_crowler() -> None:
    logger.info(f"Start crowling from url: {START_URL}")
    await task_router(START_URL)
    await check_tasks_complete()
    await client.close()
    logger.info(f"Result for save {len(START_URL)}")
    print(len(RESULTS))
    if RESULTS:
        save_csv(RESULTS)
    logger.info("Saved")
    await logger.complete()
    logger.info("End crowling")
