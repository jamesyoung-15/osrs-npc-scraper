from http import HTTPStatus
from collections.abc import Callable

import pytest
import httpx

from osrs_npc_scraper.scraper.fetcher import fetch_page
from osrs_npc_scraper.exceptions import FetchError, FetchFailureReason


def mock_response(
    status: HTTPStatus, text: str | None = None
) -> Callable[[httpx.Request], httpx.Response]:
    """HTTPX mock transport that returns passed in status code and optionally text string."""
    if text:
        response = httpx.Response(status, text=text)
    else:
        response = httpx.Response(status)
    return lambda request: response


def timeout_transport(request: httpx.Request):
    """Mock transport that raises HTTPX timeout exception"""
    raise httpx.TimeoutException("timed out", request=request)


@pytest.mark.fetcher
@pytest.mark.asyncio
async def test_fetch_page():
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(mock_response(HTTPStatus.OK, text="html page"))
    ) as client:
        response = await fetch_page(
            client=client,
            url="https://oldschool.runescape.wiki/w/Category:Non-player_characters",
        )
        assert response.status_code == HTTPStatus.OK
        assert response.text == "html page"


@pytest.mark.fetcher
@pytest.mark.asyncio
async def test_fetch_page_not_found():
    with pytest.raises(FetchError) as exc_info:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(mock_response(HTTPStatus.NOT_FOUND))
        ) as client:
            await fetch_page(
                client=client,
                url="https://oldschool.runescape.wiki/w/Category:Non-player_characters",
            )
        assert exc_info.value.reason == FetchFailureReason.NOT_FOUND


@pytest.mark.fetcher
@pytest.mark.asyncio
async def test_fetch_page_rate_limited():
    with pytest.raises(FetchError) as exc_info:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(mock_response(HTTPStatus.TOO_MANY_REQUESTS))
        ) as client:
            await fetch_page(
                client=client,
                url="https://oldschool.runescape.wiki/w/Category:Non-player_characters",
            )
        assert exc_info.value.reason == FetchFailureReason.RATE_LIMITED


@pytest.mark.fetcher
@pytest.mark.asyncio
async def test_fetch_page_forbidden():
    with pytest.raises(FetchError) as exc_info:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(mock_response(HTTPStatus.FORBIDDEN))
        ) as client:
            await fetch_page(
                client=client,
                url="https://oldschool.runescape.wiki/w/Category:Non-player_characters",
            )
        assert exc_info.value.reason == FetchFailureReason.FORBIDDEN


@pytest.mark.fetcher
@pytest.mark.asyncio
async def test_fetch_page_bad_request():
    with pytest.raises(FetchError) as exc_info:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(mock_response(HTTPStatus.BAD_REQUEST))
        ) as client:
            await fetch_page(
                client=client,
                url="https://oldschool.runescape.wiki/w/Category:Non-player_characters",
            )
        assert exc_info.value.reason == FetchFailureReason.BAD_REQUEST


@pytest.mark.fetcher
@pytest.mark.asyncio
async def test_fetch_page_request_timeout():
    with pytest.raises(FetchError) as exc_info:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(mock_response(HTTPStatus.REQUEST_TIMEOUT))
        ) as client:
            await fetch_page(
                client=client,
                url="https://oldschool.runescape.wiki/w/Category:Non-player_characters",
            )
    assert exc_info.value.reason == FetchFailureReason.REQUEST_TIMEOUT


@pytest.mark.fetcher
@pytest.mark.asyncio
async def test_fetch_page_httpx_timeout():
    with pytest.raises(FetchError) as exc_info:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(timeout_transport)
        ) as client:
            await fetch_page(
                client=client,
                url="https://oldschool.runescape.wiki/w/Category:Non-player_characters",
            )
    assert exc_info.value.reason == FetchFailureReason.HTTPX_TIMEOUT


@pytest.mark.fetcher
@pytest.mark.asyncio
async def test_fetch_page_unknown():
    with pytest.raises(FetchError) as exc_info:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(mock_response(HTTPStatus.TOO_EARLY))
        ) as client:
            await fetch_page(
                client=client,
                url="https://oldschool.runescape.wiki/w/Category:Non-player_characters",
            )
        assert exc_info.value.reason == FetchFailureReason.UNKNOWN


@pytest.mark.fetcher
@pytest.mark.asyncio
async def test_fetch_page_wrong_error():
    with pytest.raises(FetchError) as exc_info:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(mock_response(HTTPStatus.FORBIDDEN))
        ) as client:
            await fetch_page(
                client=client,
                url="https://oldschool.runescape.wiki/w/Category:Non-player_characters",
            )
        assert exc_info.value.reason != FetchFailureReason.UNKNOWN
