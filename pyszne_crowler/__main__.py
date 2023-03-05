import asyncio

import click
from crowler import start_crowler

from .utils.cache import clear_cache as cache_cleaner


@click.command()
@click.option("--clear_cache", default=False, is_flag=True, help="Clear saved cache files")
def main(clear_cache: bool):
    if clear_cache:
        cache_cleaner()
    asyncio.run(start_crowler())


if __name__ == "__main__":
    main()
