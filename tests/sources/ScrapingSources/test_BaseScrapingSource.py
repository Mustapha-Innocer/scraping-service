from unittest.mock import MagicMock

import pytest
from aioresponses import aioresponses

from lib.sources.ScrapingSources.BaseScrapingSource import BaseScrapingSource


@pytest.mark.asyncio
async def test_process(mocker, tag):
    url = "https://example.com"
    data = ""

    c = MagicMock(spec=BaseScrapingSource)

    c._get_title.return_value = "title"
    c._get_timestamp.return_value = 1
    c._get_image_url.return_value = "http://image.com"
    c._get_text.return_value = "text body"
    c._get_author.return_value = "author"
    c.name = "name"

    kafka_producer = mocker.patch(
        "lib.sources.ScrapingSources.BaseScrapingSource.kafka_producer"
    )

    with aioresponses() as mock_session:
        mock_session.get(url, payload=data)
        await BaseScrapingSource._process(c, tag)
        kafka_producer.assert_called
