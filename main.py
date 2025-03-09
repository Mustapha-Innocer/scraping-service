import asyncio

from lib.logging.logger import LOGGER
from lib.sources.ScrapingSources.CityNews.CityNews import CityNews


async def main():
    cn = CityNews()
    news_sources = [
        cn,
    ]
    await asyncio.gather(*[source.push_data() for source in news_sources])


if __name__ == "__main__":
    LOGGER.info(f"{'*' * 10} Starting Scraping Service {'*' * 10}")
    asyncio.run(main())
