import pytest

from tally import TallyClient
from tally.models import SubmissionFilter


@pytest.mark.live_api
def test_live_list_forms_returns_paginated_forms(live_client: TallyClient, live_form_id: str) -> None:
    result = live_client.forms.all(limit=100)

    assert result.page >= 1
    assert result.limit >= 1
    assert result.total >= len(result.items)
    assert any(form.id == live_form_id for form in result.items)


@pytest.mark.live_api
def test_live_list_submissions_returns_submission_page(
    live_client: TallyClient,
    live_form_id: str,
) -> None:
    result = live_client.forms.list_submissions(
        live_form_id,
        page=1,
        filter=SubmissionFilter.ALL,
    )

    assert result.page == 1
    assert result.limit >= 1
    assert isinstance(result.has_more, bool)
    assert result.total_number_of_submissions_per_filter.all >= 0
    assert result.total_number_of_submissions_per_filter.completed >= 0
    assert result.total_number_of_submissions_per_filter.partial >= 0

    for question in result.questions:
        assert question.form_id == live_form_id

    for submission in result.submissions:
        assert submission.form_id == live_form_id
        assert submission.id

    if result.submissions:
        assert any(
            response.value is not None
            for submission in result.submissions
            for response in submission.responses
        )


@pytest.mark.live_api
def test_live_list_questions_returns_questions_payload(
    live_client: TallyClient,
    live_form_id: str,
) -> None:
    result = live_client.forms.list_questions(live_form_id)

    assert isinstance(result.has_responses, bool)
    assert len(result.questions) > 0
    for question in result.questions:
        assert question.form_id == live_form_id
