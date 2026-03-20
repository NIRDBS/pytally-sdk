from collections.abc import Callable

import pytest

from tally import TallyClient


@pytest.fixture
def client() -> TallyClient:
    sdk_client = TallyClient(api_key="tly_test_key", api_version="2026-02-05")
    yield sdk_client
    sdk_client.close()


@pytest.fixture
def form_payload_factory() -> Callable[..., dict]:
    def _build(**overrides: object) -> dict:
        payload = {
            "id": "form_123",
            "name": "Customer Feedback",
            "workspaceId": "ws_123",
            "status": "PUBLISHED",
            "numberOfSubmissions": 2,
            "isClosed": False,
            "createdAt": "2026-03-01T10:00:00Z",
            "updatedAt": "2026-03-02T11:00:00Z",
        }
        payload.update(overrides)
        return payload

    return _build


@pytest.fixture
def form_details_payload(form_payload_factory: Callable[..., dict]) -> dict:
    return form_payload_factory(
        settings={
            "language": "en",
            "isClosed": False,
            "hasProgressBar": True,
            "saveForLater": True,
        },
        blocks=[
            {
                "uuid": "block-1",
                "type": "FORM_TITLE",
                "groupUuid": "group-1",
                "groupType": "FORM_TITLE",
                "payload": {"html": "<h1>Customer Feedback</h1>"},
            }
        ],
        payments=[
            {
                "amount": 25,
                "currency": "USD",
            }
        ],
    )


@pytest.fixture
def paginated_forms_payload(form_payload_factory: Callable[..., dict]) -> dict:
    return {
        "items": [
            form_payload_factory(id="form_123", name="Customer Feedback"),
            form_payload_factory(id="form_456", name="Product Survey", status="DRAFT"),
        ],
        "page": 2,
        "limit": 10,
        "total": 25,
        "hasMore": True,
    }


@pytest.fixture
def submissions_payload() -> dict:
    return {
        "page": 1,
        "limit": 50,
        "hasMore": False,
        "totalNumberOfSubmissionsPerFilter": {
            "all": 2,
            "completed": 1,
            "partial": 1,
        },
        "questions": [
            {
                "id": "question_1",
                "type": "INPUT_TEXT",
                "title": "First name",
                "isTitleModifiedByUser": True,
                "formId": "form_123",
                "isDeleted": False,
                "numberOfResponses": 2,
                "createdAt": "2026-03-01T10:00:00Z",
                "updatedAt": "2026-03-02T10:00:00Z",
                "fields": [
                    {
                        "uuid": "field-1",
                        "type": "INPUT_TEXT",
                        "blockGroupUuid": "group-1",
                        "title": "First name",
                    }
                ],
            }
        ],
        "submissions": [
            {
                "id": "submission_1",
                "formId": "form_123",
                "isCompleted": True,
                "submittedAt": "2026-03-03T10:00:00Z",
                "responses": [
                    {
                        "questionId": "question_1",
                        "value": "Ada",
                    }
                ],
            }
        ],
    }


@pytest.fixture
def submission_with_questions_payload(submissions_payload: dict) -> dict:
    return {
        "questions": submissions_payload["questions"],
        "submission": {
            "id": "submission_1",
            "formId": "form_123",
            "isCompleted": True,
            "submittedAt": "2026-03-03T10:00:00Z",
            "createdAt": "2026-03-03T09:59:00Z",
            "updatedAt": "2026-03-03T10:01:00Z",
            "responses": submissions_payload["submissions"][0]["responses"],
        },
    }
