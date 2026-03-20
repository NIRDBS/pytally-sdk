from unittest.mock import MagicMock

from tally import TallyClient
from tally.models import BlockType, FormBlock, FormSettings, FormStatus, SubmissionFilter, SubmissionResponse


def test_all_builds_params_and_parses_paginated_forms(
    client: TallyClient,
    paginated_forms_payload: dict,
) -> None:
    client.request = MagicMock(return_value=paginated_forms_payload)

    result = client.forms.all(page=2, limit=10, workspace_ids=["ws_123", "ws_456"])

    client.request.assert_called_once_with(
        "GET",
        "/forms",
        params={"page": 2, "limit": 10, "workspaceIds": ["ws_123", "ws_456"]},
    )
    assert result.page == 2
    assert result.has_more is True
    assert [form.id for form in result.items] == ["form_123", "form_456"]
    assert result.items[0].status is FormStatus.PUBLISHED
    assert result.items[0].organization_id == "org_123"


def test_get_returns_form_details(client: TallyClient, form_details_payload: dict) -> None:
    client.request = MagicMock(return_value=form_details_payload)

    result = client.forms.get("form_123")

    client.request.assert_called_once_with("GET", "/forms/form_123")
    assert result.id == "form_123"
    assert result.organization_id == "org_123"
    assert result.is_name_modified_by_user is True
    assert result.has_draft_blocks is False
    assert result.index == 7
    assert result.settings.has_progress_bar is True
    assert result.blocks[0].type is BlockType.FORM_TITLE
    assert result.payments[0].currency == "USD"


def test_create_serializes_blocks_enums_and_settings(
    client: TallyClient,
    form_details_payload: dict,
) -> None:
    client.request = MagicMock(return_value=form_details_payload)
    blocks = [
        FormBlock(
            uuid="block-1",
            type=BlockType.FORM_TITLE,
            group_uuid="group-1",
            group_type=BlockType.FORM_TITLE,
            payload={"html": "<h1>Customer Feedback</h1>"},
        )
    ]
    settings = FormSettings(
        is_closed=False,
        save_for_later=True,
        has_progress_bar=True,
    )

    result = client.forms.create(
        status=FormStatus.PUBLISHED,
        blocks=blocks,
        workspace_id="ws_123",
        template_id="template_123",
        settings=settings,
    )

    client.request.assert_called_once_with(
        "POST",
        "/forms",
        json={
            "status": "PUBLISHED",
            "blocks": [
                {
                    "uuid": "block-1",
                    "type": "FORM_TITLE",
                    "groupUuid": "group-1",
                    "groupType": "FORM_TITLE",
                    "payload": {"html": "<h1>Customer Feedback</h1>"},
                }
            ],
            "workspaceId": "ws_123",
            "templateId": "template_123",
            "settings": {
                "isClosed": False,
                "hasSelfEmailNotifications": False,
                "hasRespondentEmailNotifications": False,
                "hasProgressBar": True,
                "hasPartialSubmissions": False,
                "pageAutoJump": False,
                "saveForLater": True,
            },
        },
    )
    assert result.status is FormStatus.PUBLISHED


def test_update_only_sends_supplied_fields(
    client: TallyClient,
    form_details_payload: dict,
) -> None:
    client.request = MagicMock(return_value=form_details_payload)

    result = client.forms.update(
        "form_123",
        name="Renamed form",
        status="DRAFT",
        settings={"isClosed": True},
    )

    client.request.assert_called_once_with(
        "PATCH",
        "/forms/form_123",
        json={
            "name": "Renamed form",
            "status": "DRAFT",
            "settings": {"isClosed": True},
        },
    )
    assert result.name == "Customer Feedback"


def test_delete_calls_delete_endpoint(client: TallyClient) -> None:
    client.request = MagicMock(return_value=None)

    client.forms.delete("form_123")

    client.request.assert_called_once_with("DELETE", "/forms/form_123")


def test_list_questions_parses_question_models(client: TallyClient, questions_payload: dict) -> None:
    client.request = MagicMock(return_value=questions_payload)

    result = client.forms.list_questions("form_123")

    client.request.assert_called_once_with("GET", "/forms/form_123/questions")
    assert result.has_responses is True
    assert len(result.questions) == 1
    assert result.questions[0].fields[0].type is BlockType.INPUT_FIELD
    assert result.questions[0].fields[0].question_type is BlockType.INPUT_TEXT
    assert result.questions[0].number_of_responses == 2


def test_list_submissions_builds_filters_and_parses_payload(
    client: TallyClient,
    submissions_payload: dict,
) -> None:
    client.request = MagicMock(return_value=submissions_payload)

    result = client.forms.list_submissions(
        "form_123",
        page=3,
        filter=SubmissionFilter.COMPLETED,
        start_date="2026-03-01T00:00:00Z",
        end_date="2026-03-20T23:59:59Z",
        after_id="submission_0",
    )

    client.request.assert_called_once_with(
        "GET",
        "/forms/form_123/submissions",
        params={
            "page": 3,
            "filter": "completed",
            "startDate": "2026-03-01T00:00:00Z",
            "endDate": "2026-03-20T23:59:59Z",
            "afterId": "submission_0",
        },
    )
    assert result.total_number_of_submissions_per_filter.completed == 1
    assert result.submissions[0].respondent_id == "respondent_1"
    assert result.submissions[0].responses[0].form_id == "form_123"
    assert result.submissions[0].responses[0].submission_id == "submission_1"
    assert result.submissions[0].responses[0].formatted_answer == "Ada"
    assert result.submissions[0].responses[0].value == "Ada"


def test_get_submission_parses_submission_with_questions(
    client: TallyClient,
    submission_with_questions_payload: dict,
) -> None:
    client.request = MagicMock(return_value=submission_with_questions_payload)

    result = client.forms.get_submission("form_123", "submission_1")

    client.request.assert_called_once_with(
        "GET",
        "/forms/form_123/submissions/submission_1",
    )
    assert result.submission.id == "submission_1"
    assert result.submission.respondent_id == "respondent_1"
    assert result.submission.responses[0].session_uuid == "session_1"
    assert result.submission.responses[0].formatted_answer == "Ada"
    assert result.questions[0].id == "question_1"


def test_delete_submission_calls_delete_endpoint(client: TallyClient) -> None:
    client.request = MagicMock(return_value=None)

    client.forms.delete_submission("form_123", "submission_1")

    client.request.assert_called_once_with(
        "DELETE",
        "/forms/form_123/submissions/submission_1",
    )


def test_submission_response_from_dict_reads_answer_field() -> None:
    response = SubmissionResponse.from_dict(
        {
            "id": "response_1",
            "formId": "form_123",
            "questionId": "question_1",
            "respondentId": "respondent_1",
            "submissionId": "submission_1",
            "sessionUuid": "session_1",
            "answer": ["Ada"],
            "formattedAnswer": "Ada",
            "createdAt": "2026-03-03T10:00:00Z",
            "updatedAt": "2026-03-03T10:01:00Z",
        }
    )

    assert response.id == "response_1"
    assert response.form_id == "form_123"
    assert response.question_id == "question_1"
    assert response.respondent_id == "respondent_1"
    assert response.submission_id == "submission_1"
    assert response.session_uuid == "session_1"
    assert response.formatted_answer == "Ada"
    assert response.value == ["Ada"]
