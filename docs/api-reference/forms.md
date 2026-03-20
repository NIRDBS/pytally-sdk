# Forms

The Forms resource covers listing, fetching, creating, updating, and deleting forms, plus question and submission access.

## Initialization

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")
```

## List Forms

### Method

```python
client.forms.all(
    page: int = 1,
    limit: int = 50,
    workspace_ids: list[str] | None = None,
) -> PaginatedForms
```

### Example

```python
forms = client.forms.all(page=1, limit=10)

print(forms.page, forms.total, forms.has_more)
for form in forms.items:
    print(form.id, form.name, form.status.value)
```

### Notes

- `workspace_ids` accepts a list of workspace IDs
- The returned collection is `items`, not `data`
- `PaginatedForms` exposes `page`, `limit`, `total`, and `has_more`

### Official Reference

[List Forms](https://developers.tally.so/api-reference/endpoint/forms/list)

---

## Get Form

### Method

```python
client.forms.get(form_id: str) -> FormDetails
```

### Example

```python
form = client.forms.get("wXYz123")

print(form.name)
print(form.number_of_submissions)
print(form.settings.has_progress_bar)
print(len(form.blocks))
```

### Official Reference

[Get Form](https://developers.tally.so/api-reference/endpoint/forms/get)

---

## Create Form

### Method

```python
client.forms.create(
    status: FormStatus | str,
    blocks: list[FormBlock] | list[dict],
    workspace_id: str | None = None,
    template_id: str | None = None,
    settings: FormSettings | dict | None = None,
) -> FormCreated
```

### Example

```python
from tally.models import BlockType, FormBlock, FormSettings, FormStatus

form = client.forms.create(
    status=FormStatus.DRAFT,
    workspace_id="ws_123",
    blocks=[
        FormBlock(
            uuid="block-1",
            type=BlockType.FORM_TITLE,
            group_uuid="block-1",
            group_type=BlockType.FORM_TITLE,
            payload={"html": "<h1>Customer Feedback</h1>"},
        )
    ],
    settings=FormSettings(
        has_progress_bar=True,
        save_for_later=True,
    ),
)
```

### Official Reference

[Create Form](https://developers.tally.so/api-reference/endpoint/forms/post)

---

## Update Form

### Method

```python
client.forms.update(
    form_id: str,
    name: str | None = None,
    status: FormStatus | str | None = None,
    blocks: list[FormBlock] | list[dict] | None = None,
    settings: FormSettings | dict | None = None,
) -> Form
```

### Example

```python
form = client.forms.update(
    "wXYz123",
    name="Customer Feedback 2026",
    status="PUBLISHED",
    settings={"hasProgressBar": True},
)

print(form.id, form.status.value)
```

### Official Reference

[Update Form](https://developers.tally.so/api-reference/endpoint/forms/patch)

---

## Delete Form

### Method

```python
client.forms.delete(form_id: str) -> None
```

### Official Reference

[Delete Form](https://developers.tally.so/api-reference/endpoint/forms/delete)

---

## List Questions

### Method

```python
client.forms.list_questions(form_id: str) -> QuestionsList
```

### Example

```python
result = client.forms.list_questions("wXYz123")

print(result.has_responses)
for question in result.questions:
    print(question.id, question.title, question.type)
    for field in question.fields:
        print(field.uuid, field.title, field.type)
```

### Notes

- `QuestionsList` exposes `questions` and `has_responses`
- `QuestionField` exposes `uuid`, `type`, `question_type`, `block_group_uuid`, and `title`

### Official Reference

[List Questions](https://developers.tally.so/api-reference/endpoint/forms/questions/list)

---

## List Submissions

### Method

```python
client.forms.list_submissions(
    form_id: str,
    page: int = 1,
    filter: SubmissionFilter | str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    after_id: str | None = None,
) -> PaginatedSubmissions
```

### Example

```python
from tally.models import SubmissionFilter

result = client.forms.list_submissions(
    "wXYz123",
    page=1,
    filter=SubmissionFilter.ALL,
)

print(result.total_number_of_submissions_per_filter.all)
for submission in result.submissions:
    print(submission.id, submission.submitted_at, submission.is_completed)
```

### Notes

- Date filters use `start_date` and `end_date`
- Cursor-style pagination can use `after_id`
- The returned collections are `questions` and `submissions`

### Official Reference

[List Submissions](https://developers.tally.so/api-reference/endpoint/forms/submissions/list)

---

## Get Submission

### Method

```python
client.forms.get_submission(
    form_id: str,
    submission_id: str,
) -> SubmissionWithQuestions
```

### Example

```python
result = client.forms.get_submission("wXYz123", "sub_abc456")

print(result.submission.id)
for response in result.submission.responses:
    print(response.question_id, response.value)
```

### Official Reference

[Get Submission](https://developers.tally.so/api-reference/endpoint/forms/submissions/get)

---

## Delete Submission

### Method

```python
client.forms.delete_submission(
    form_id: str,
    submission_id: str,
) -> None
```

### Official Reference

[Delete Submission](https://developers.tally.so/api-reference/endpoint/forms/submissions/delete)

---

## Models

### Form

::: tally.models.form.Form
    options:
      show_source: false
      heading_level: 4
      members: []

### FormCreated

::: tally.models.form.FormCreated
    options:
      show_source: false
      heading_level: 4
      members: []

### FormDetails

::: tally.models.form.FormDetails
    options:
      show_source: false
      heading_level: 4
      members: []

### PaginatedForms

::: tally.models.form.PaginatedForms
    options:
      show_source: false
      heading_level: 4
      members: []

### Question

::: tally.models.form.Question
    options:
      show_source: false
      heading_level: 4
      members: []

### QuestionsList

::: tally.models.form.QuestionsList
    options:
      show_source: false
      heading_level: 4
      members: []

### Submission

::: tally.models.form.Submission
    options:
      show_source: false
      heading_level: 4
      members: []

### SubmissionWithQuestions

::: tally.models.form.SubmissionWithQuestions
    options:
      show_source: false
      heading_level: 4
      members: []

### PaginatedSubmissions

::: tally.models.form.PaginatedSubmissions
    options:
      show_source: false
      heading_level: 4
      members: []
