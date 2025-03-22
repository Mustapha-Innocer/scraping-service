import asyncio

from lib.logging.logger import LOGGER
from lib.sources.ScrapingSources.CityNews.CityNews import CityNews
from lib.sources.ScrapingSources.TechCrunch.TechCrunch import TechCrunch
from lib.sources.ScrapingSources.Yahoo.Yahoo import Yahoo


async def main():
    cn = CityNews()
    yh = Yahoo()
    tc = TechCrunch()
    news_sources = [
        # cn,
        # yh,
        tc,
    ]
    await asyncio.gather(*[source.push_data(60) for source in news_sources])


if __name__ == "__main__":
    LOGGER.info(f"{'*' * 10} Starting Scraping Service {'*' * 10}")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info(
            f"{'*' * 10} Scraping Service closed {'*' * 10}"
        )
