import pytest
from bs4 import BeautifulSoup


@pytest.fixture(scope="function")
def tag():
    return BeautifulSoup(
        "<a href='https://example.com'>New Title</a>", "html.parser"
    )
