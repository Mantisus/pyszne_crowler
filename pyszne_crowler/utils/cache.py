from collections.abc import Callable
from functools import wraps
from hashlib import sha256
from pathlib import Path

CACHE_FOLDER = Path(Path(__file__).parents[1], "cache")

if not CACHE_FOLDER.exists():
    CACHE_FOLDER.mkdir()


def get_cache_path(*args):
    file_string = "".join(args)
    cache_path = Path(CACHE_FOLDER, sha256(file_string.encode("UTF-8")).hexdigest())
    return cache_path.with_suffix(".cache")


def get_cache_data(cache_path: Path) -> bytes:
    with open(cache_path, "rb") as cache_file:
        return cache_file.read()


def save_cache_data(cache_path: Path, data: bytes) -> None:
    with open(cache_path, "wb") as cache_file:
        cache_file.write(data)


def clear_cache() -> None:
    for file in CACHE_FOLDER.glob("*.cache"):
        file.unlink()


def url_cache(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        cache_path = get_cache_path(*args)
        if cache_path.exists():
            return get_cache_data(cache_path)
        data = await func(*args, **kwargs)
        if data:
            save_cache_data(cache_path, data)
        return data

    return wrapper
