import asyncio
from datetime import datetime

from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from lib.logging.logger import LOGGER
from lib.sources.ScrapingSources.BaseScrapingSource import BaseScrapingSource


class Yahoo(BaseScrapingSource):
    def __init__(self, wait_time: int | None = None):
        self.__name = "yahoo"
        self.__url = "https://www.yahoo.com/news/"
        super().__init__(wait_time)

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    async def _get_html(self, url):
        try:
            options = Options()
            options.add_argument("--headless")  # Run without opening a browser
            options.add_argument(
                "--disable-blink-features=AutomationControlled"
            )
            options.add_argument("start-maximized")
            options.add_argument("user-agent=Mozilla/5.0 ...")

            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options,
            )

            await asyncio.to_thread(driver.get, url)

            scroll_pause_time = 2
            num_scrolls = 10
            for _ in range(num_scrolls):
                LOGGER.info(f"Scrolling down ... - {url}")
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                await asyncio.sleep(scroll_pause_time)
            return BeautifulSoup(driver.page_source, "html.parser")
        except Exception as e:
            LOGGER.error(str(e))

    # @check_cache
    def _get_news_tags(self, source_html: BeautifulSoup) -> set[Tag]:
        LOGGER.debug("Extracting news tags")
        news_tags: list[Tag] = source_html.find_all(
            "div", class_="D(f) Fld(c) Fxg(1) Miw(0)"
        )
        # TODO: handle empty news_tags
        return set(news_tags[:10])

    def _get_title(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story title")
        title: str = story_html.find("h1", class_="jeg_post_title").text
        return title

    def _get_timestamp(self, story_html: BeautifulSoup) -> int:
        LOGGER.info("Extracting story timestamp")
        date_str: str = (
            story_html.find("div", class_="meta_left")
            .find("div", class_="jeg_meta_date")
            .find("a")
            .text
        )
        date = datetime.strptime(date_str, "%B %d, %Y")
        return int(date.timestamp())

    def _get_image_url(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story image url")
        img_url: str = story_html.find(
            "div", class_="jeg_featured featured_image"
        ).find("img")["src"]
        return img_url

    def _get_text(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story body")
        text: str = story_html.find("div", class_="content-inner").text
        return text

    def _get_author(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story author")
        tag: Tag = story_html.select_one(
            "div.meta_left > div.jeg_meta_author.coauthor"
        )
        if tag and tag.find("a"):
            return tag.find("a").text
        LOGGER.info("Author name not found")
        return "unknown"

    def _process(self, tag):
        url = tag.a["href"]
        url = "https://www.yahoo.com" + url
        tag.a["href"] = url
        return super()._process(tag)
