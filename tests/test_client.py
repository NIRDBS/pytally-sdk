from unittest.mock import MagicMock

import httpx
import pytest

from tally import (
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TallyClient,
    TallyConnectionError,
    TallyTimeoutError,
    UnauthorizedError,
)


def make_response(
    status_code: int,
    *,
    json_data: object | None = None,
    text: str = "",
) -> MagicMock:
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.text = text
    if isinstance(json_data, Exception):
        response.json.side_effect = json_data
    else:
        response.json.return_value = json_data
    return response


def test_client_sets_default_headers() -> None:
    client = TallyClient(api_key="tly_test_key")

    assert client._get_headers() == {
        "Authorization": "Bearer tly_test_key",
        "Content-Type": "application/json",
    }

    client.close()


def test_client_includes_api_version_header() -> None:
    client = TallyClient(api_key="tly_test_key", api_version="2026-02-05")

    assert client._get_headers()["tally-version"] == "2026-02-05"

    client.close()


def test_request_returns_json_payload(client: TallyClient) -> None:
    response = make_response(200, json_data={"ok": True})
    client._client.request = MagicMock(return_value=response)

    data = client.request("GET", "/users/me", params={"include": "profile"})

    assert data == {"ok": True}
    client._client.request.assert_called_once_with(
        method="GET",
        url="/users/me",
        params={"include": "profile"},
        json=None,
    )


def test_request_returns_none_for_no_content(client: TallyClient) -> None:
    response = make_response(204, json_data=None)
    client._client.request = MagicMock(return_value=response)

    data = client.request("DELETE", "/forms/form_123")

    assert data is None


@pytest.mark.parametrize(
    ("status_code", "error_class"),
    [
        (400, BadRequestError),
        (401, UnauthorizedError),
        (403, ForbiddenError),
        (404, NotFoundError),
        (429, RateLimitError),
        (500, ServerError),
        (502, ServerError),
    ],
)
def test_request_maps_api_errors(
    client: TallyClient,
    status_code: int,
    error_class: type[Exception],
) -> None:
    response = make_response(
        status_code,
        json_data={
            "message": "Request failed",
            "errorType": "VALIDATION_ERROR",
            "errors": [{"errorType": "FIELD", "msg": "Bad field"}],
        },
    )
    client._client.request = MagicMock(return_value=response)

    with pytest.raises(error_class) as exc_info:
        client.request("GET", "/forms")

    assert exc_info.value.message == "Request failed"
    assert exc_info.value.status_code == status_code


def test_request_uses_plain_text_when_error_json_is_invalid(client: TallyClient) -> None:
    response = make_response(
        400,
        json_data=ValueError("not json"),
        text="plain-text error",
    )
    client._client.request = MagicMock(return_value=response)

    with pytest.raises(BadRequestError) as exc_info:
        client.request("GET", "/forms")

    assert exc_info.value.message == "plain-text error"
    assert exc_info.value.response is None


def test_request_wraps_timeout_errors(client: TallyClient) -> None:
    client._client.request = MagicMock(side_effect=httpx.TimeoutException("slow request"))

    with pytest.raises(TallyTimeoutError, match="Request timed out"):
        client.request("GET", "/forms")


def test_request_wraps_connection_errors(client: TallyClient) -> None:
    client._client.request = MagicMock(side_effect=httpx.ConnectError("dns failed"))

    with pytest.raises(TallyConnectionError, match="Connection error"):
        client.request("GET", "/forms")


def test_request_wraps_unexpected_errors(client: TallyClient) -> None:
    client._client.request = MagicMock(side_effect=RuntimeError("boom"))

    with pytest.raises(TallyConnectionError, match="Unexpected error: boom"):
        client.request("GET", "/forms")


def test_context_manager_closes_underlying_http_client() -> None:
    client = TallyClient(api_key="tly_test_key")
    client._client.close = MagicMock()

    with client as managed_client:
        assert managed_client is client

    client._client.close.assert_called_once_with()
