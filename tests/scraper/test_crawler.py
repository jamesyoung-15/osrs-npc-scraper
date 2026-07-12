import pytest

from bs4 import BeautifulSoup

from osrs_npc_scraper.scraper.crawler import extract_next_page, extract_npc_list

@pytest.mark.crawler
def test_extract_next_page(test_category_page, test_base_url):
    soup = BeautifulSoup(test_category_page, features="html.parser")
    url = extract_next_page(soup, test_base_url)
    assert (
        url
        == test_base_url
        + "/w/Category:Non-player_characters?pagefrom=Beigarth#mw-pages"
    )

@pytest.mark.crawler
def test_extract_npc_list(test_category_page, test_base_url):
    soup = BeautifulSoup(test_category_page, features="html.parser")
    npc_list = extract_npc_list(soup, test_base_url)
    assert len(npc_list) == 200

    # check first and last
    assert npc_list[0].title == "Aristarchus"
    assert npc_list[0].url == test_base_url + "/w/Aristarchus"
    assert npc_list[-1].title == "Beggar"
    assert npc_list[-1].url == test_base_url + "/w/Beggar"
