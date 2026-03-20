import os

import pytest

from tally import TallyClient


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        pytest.skip(f"{name} is required for live API tests")
    return value


@pytest.fixture
def live_client() -> TallyClient:
    api_key = _require_env("TALLY_API_KEY")
    api_version = os.getenv("TALLY_API_VERSION")
    client = TallyClient(api_key=api_key, api_version=api_version)
    yield client
    client.close()


@pytest.fixture
def live_form_id() -> str:
    return _require_env("TALLY_FORM_ID")
