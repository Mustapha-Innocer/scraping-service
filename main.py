import asyncio

from lib.sources.ScrapingSources.CityNews.CityNews import CityNews


async def main():
    cn = CityNews()
    news_sources = [
        cn,
    ]
    await asyncio.gather(*[source.push_data() for source in news_sources])


if __name__ == "__main__":
    cn = CityNews()
    news_sources = [
        cn,
    ]
    asyncio.run(main())
