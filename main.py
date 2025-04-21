import asyncio

from lib.logging.logger import LOGGER
from lib.sources.ScrapingSources.CityNews.CityNews import CityNews
from lib.sources.ScrapingSources.TechCrunch.TechCrunch import TechCrunch


async def heart_beat():
    while True:
        await asyncio.sleep(5)
        LOGGER.info("Heartbeat received ...")


async def main():
    cn = CityNews(60)
    tc = TechCrunch(30)
    news_sources = [
        cn,
        tc,
    ]
    await asyncio.gather(
        heart_beat(), *[source.push_data() for source in news_sources]
    )


if __name__ == "__main__":
    LOGGER.info(f"{'*' * 10} Starting Scraping Service {'*' * 10}")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info(f"{'*' * 10} Scraping Service closed {'*' * 10}")
        LOGGER.info(f"{'*' * 10} Scraping Service closed {'*' * 10}")
