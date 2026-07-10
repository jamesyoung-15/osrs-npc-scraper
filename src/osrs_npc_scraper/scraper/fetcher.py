from http import HTTPStatus

import httpx

from osrs_npc_scraper.exceptions import FetchError, FetchFailureReason


async def fetch_page(
    client: httpx.AsyncClient, url: str, timeout: int = 10
) -> httpx.Response:
    """Sends a GET request with HTTPX to a URL."""

    try:
        response = await client.get(url=url, timeout=timeout)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == HTTPStatus.BAD_REQUEST:
            raise FetchError(
                url=url, reason=FetchFailureReason.BAD_REQUEST, original_exception=e
            )
        elif e.response.status_code == HTTPStatus.FORBIDDEN:
            raise FetchError(
                url=url, reason=FetchFailureReason.FORBIDDEN, original_exception=e
            )
        elif e.response.status_code == HTTPStatus.NOT_FOUND:
            raise FetchError(
                url=url, reason=FetchFailureReason.NOT_FOUND, original_exception=e
            )
        elif e.response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            raise FetchError(
                url=url, reason=FetchFailureReason.RATE_LIMITED, original_exception=e
            )
        elif e.response.status_code == HTTPStatus.REQUEST_TIMEOUT:
            raise FetchError(
                url=url, reason=FetchFailureReason.REQUEST_TIMEOUT, original_exception=e
            )
        else:
            raise FetchError(
                url=url, reason=FetchFailureReason.UNKNOWN, original_exception=e
            )
    except httpx.TimeoutException as e:
        raise FetchError(
            url=url, reason=FetchFailureReason.HTTPX_TIMEOUT, original_exception=e
        )
    except Exception as e:
        raise FetchError(
            url=url, reason=FetchFailureReason.UNKNOWN, original_exception=e
        )

    return response
