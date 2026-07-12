from pathlib import Path

import pytest


@pytest.fixture
def test_base_url() -> str:
    return "https://oldschool.runescape.wiki"


@pytest.fixture
def test_category_page() -> str:
    category_page_path = (
        Path(__file__).parent / "fixtures" / "category_page_example.html"
    )

    with open(category_page_path, "r", encoding="utf-8") as f:
        return f.read()
