# Webhooks

The Webhooks resource covers listing, creating, updating, deleting, inspecting delivery events, and retrying failed events.

## Initialization

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")
```

## List Webhooks

### Method

```python
client.webhooks.all(
    page: int = 1,
    limit: int = 25,
) -> PaginatedWebhooks
```

### Example

```python
result = client.webhooks.all(page=1, limit=10)

print(result.page, result.total_count, result.has_more)
for webhook in result.webhooks:
    print(webhook.id, webhook.url, webhook.is_enabled)
```

### Notes

- The returned collection is `webhooks`, not `data`
- `PaginatedWebhooks` exposes `page`, `limit`, `has_more`, and `total_count`

### Official Reference

[List Webhooks](https://developers.tally.so/api-reference/endpoint/webhooks/get)

---

## Iterate Webhooks

```python
for webhook in client.webhooks:
    print(webhook.url, webhook.is_enabled)
```

---

## Create Webhook

### Method

```python
client.webhooks.create(
    form_id: str,
    url: str,
    event_types: list[WebhookEventType] | list[str] | None = None,
    signing_secret: str | None = None,
    http_headers: list[WebhookHeader] | list[dict[str, str]] | None = None,
    external_subscriber: str | None = None,
) -> WebhookCreated
```

### Example

```python
from tally.models import WebhookEventType

webhook = client.webhooks.create(
    form_id="wXYz123",
    url="https://your-app.com/webhooks/tally",
    event_types=[WebhookEventType.FORM_RESPONSE],
    signing_secret="super-secret",
    http_headers=[{"name": "X-App", "value": "pytally-sdk"}],
)

print(webhook.id, webhook.url, webhook.is_enabled)
```

### Notes

- If `event_types` is omitted, the SDK defaults to `["FORM_RESPONSE"]`
- Header objects use `name` and `value`

### Official Reference

[Create Webhook](https://developers.tally.so/api-reference/endpoint/webhooks/post)

---

## Update Webhook

### Method

```python
client.webhooks.update(
    webhook_id: str,
    form_id: str,
    url: str,
    event_types: list[WebhookEventType] | list[str],
    is_enabled: bool,
    signing_secret: str | None = None,
    http_headers: list[WebhookHeader] | list[dict[str, str]] | None = None,
) -> None
```

### Example

```python
client.webhooks.update(
    webhook_id="wh_123",
    form_id="wXYz123",
    url="https://your-app.com/webhooks/tally",
    event_types=["FORM_RESPONSE"],
    is_enabled=True,
)
```

### Notes

- This method updates the full webhook payload; required fields must be supplied

### Official Reference

[Update Webhook](https://developers.tally.so/api-reference/endpoint/webhooks/patch)

---

## Delete Webhook

### Method

```python
client.webhooks.delete(webhook_id: str) -> None
```

### Official Reference

[Delete Webhook](https://developers.tally.so/api-reference/endpoint/webhooks/delete)

---

## Get Webhook Events

### Method

```python
client.webhooks.get_events(
    webhook_id: str,
    page: int = 1,
) -> PaginatedWebhookEvents
```

### Example

```python
events = client.webhooks.get_events("wh_123", page=1)

print(events.total_number_of_events)
for event in events.events:
    print(event.id, event.event_type.value, event.delivery_status.value)
```

### Notes

- The returned collection is `events`, not `data`
- `PaginatedWebhookEvents` exposes `page`, `limit`, `has_more`, and `total_number_of_events`

### Official Reference

[List Webhook Events](https://developers.tally.so/api-reference/endpoint/webhooks/events/get)

---

## Retry Webhook Event

### Method

```python
client.webhooks.retry_event(
    webhook_id: str,
    event_id: str,
) -> None
```

### Example

```python
client.webhooks.retry_event("wh_123", "evt_456")
```

### Official Reference

[Retry Webhook Event](https://developers.tally.so/api-reference/endpoint/webhooks/events/retry)

---

## Models

### Webhook

::: tally.models.webhook.Webhook
    options:
      show_source: false
      heading_level: 4
      members: []

### WebhookCreated

::: tally.models.webhook.WebhookCreated
    options:
      show_source: false
      heading_level: 4
      members: []

### WebhookEvent

::: tally.models.webhook.WebhookEvent
    options:
      show_source: false
      heading_level: 4
      members: []

### PaginatedWebhooks

::: tally.models.webhook.PaginatedWebhooks
    options:
      show_source: false
      heading_level: 4
      members: []

### PaginatedWebhookEvents

::: tally.models.webhook.PaginatedWebhookEvents
    options:
      show_source: false
      heading_level: 4
      members: []
