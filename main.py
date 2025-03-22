import asyncio

from lib.logging.logger import LOGGER
from lib.sources.ScrapingSources.CityNews.CityNews import CityNews
from lib.sources.ScrapingSources.TechCrunch.TechCrunch import TechCrunch
# from lib.sources.ScrapingSources.Yahoo.Yahoo import Yahoo


async def main():
    cn = CityNews()
    tc = TechCrunch()
    news_sources = [
        cn,
        tc,
    ]
    await asyncio.gather(*[source.push_data() for source in news_sources])


if __name__ == "__main__":
    LOGGER.info(f"{'*' * 10} Starting Scraping Service {'*' * 10}")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info(
            f"{'*' * 10} Scraping Service closed {'*' * 10}"
        )
