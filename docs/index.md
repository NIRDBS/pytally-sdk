# PyTally SDK

Unofficial Python SDK for the [Tally.so](https://tally.so) API.

[![PyPI version](https://badge.fury.io/py/pytally-sdk.svg)](https://badge.fury.io/py/pytally-sdk)
[![Python Versions](https://img.shields.io/pypi/pyversions/pytally-sdk.svg)](https://pypi.org/project/pytally-sdk/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Introduction

PyTally SDK is a Python library that provides a simple and intuitive interface to interact with the Tally.so API. It handles authentication, request/response processing, pagination, and error handling, allowing you to focus on building your application.

### What's Implemented

Currently, the SDK covers the following Tally API resources:

- ✅ **Users** - Get current user information
- ✅ **Organizations** - Manage users and invites
- ✅ **Forms** - Create, update, and manage forms and submissions
- ✅ **Workspaces** - List and manage workspaces
- ✅ **Webhooks** - Configure and monitor webhook integrations
- 🚧 **MCP** - Not implemented yet

!!! info "Official API Documentation"
    For complete API details and specifications, refer to the [Official Tally API Documentation](https://developers.tally.so/api-reference/introduction).

## Installation

### Using pip

```bash
pip install pytally-sdk
```

### Using uv

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver:

```bash
uv add pytally-sdk
```

### Requirements

- Python 3.11 or higher
- `httpx` library (automatically installed)

## Quickstart

Get started with PyTally SDK in just a few lines of code:

### Basic Usage

```python
from tally import Tally

# Initialize the client with your API key
client = Tally(api_key="tly_your_api_key_here")

# Get current user information
user = client.users.me()
print(f"Hello, {user.full_name}!")
print(f"Email: {user.email}")
if user.subscription_plan:
    print(f"Plan: {user.subscription_plan.value}")
```

### Using Context Manager

The recommended approach for automatic resource cleanup:

```python
from tally import Tally

with Tally(api_key="tly_your_api_key_here") as client:
    # Get current user
    user = client.users.me()
    print(f"Organization ID: {user.organization_id}")

    # List all forms
    for form in client.forms:
        print(f"Form: {form.name} (ID: {form.id})")
```

### Working with Forms

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# List forms with pagination
forms = client.forms.all(page=1, limit=10)
print(f"Found {len(forms.items)} forms")

# Get a specific form
form = client.forms.get(form_id="wXYz123")
print(f"Form: {form.name}")
print(f"Status: {form.status.value}")
print(f"Submissions: {form.number_of_submissions}")

# List form submissions
submissions = client.forms.list_submissions(
    form_id="wXYz123",
    filter="all",
    page=1,
)

for submission in submissions.submissions:
    print(f"Submission ID: {submission.id}")
    print(f"Submitted: {submission.submitted_at}")
```

### Setting up Webhooks

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Create a webhook
webhook = client.webhooks.create(
    form_id="wXYz123",
    url="https://your-app.com/webhooks/tally",
    event_types=["FORM_RESPONSE"],
)

print(f"Webhook created: {webhook.id}")

# List webhook events
events = client.webhooks.get_events(webhook_id=webhook.id)
for event in events.events:
    print(f"Event: {event.event_type.value} - {event.delivery_status.value}")
```

## API Versioning

The Tally API uses date-based versioning. You can specify a specific API version when initializing the client:

```python
from tally import Tally

client = Tally(
    api_key="tly_your_api_key_here",
    api_version="2026-02-05"  # Optional: specify API version
)
```

If not specified, the client will use the version tied to your API key.

## Error Handling

The SDK provides specific exceptions for different error scenarios:

```python
from tally import Tally, UnauthorizedError, RateLimitError, NotFoundError

client = Tally(api_key="tly_your_api_key_here")

try:
    form = client.forms.get(form_id="invalid_id")
except UnauthorizedError:
    print("Invalid API key!")
except NotFoundError:
    print("Form not found!")
except RateLimitError as e:
    print(f"Rate limit exceeded. Try again later.")
    print(f"Status code: {e.status_code}")
```

For more details, see the [Error Handling](error-handling.md) guide.

## Configuration Options

The [`TallyClient`](api-reference/users.md#initialization) accepts the following configuration options:

```python
from tally import Tally

client = Tally(
    api_key="tly_your_api_key_here",       # Required: Your Tally API key
    api_version="2026-02-05",              # Optional: API version (default: key version)
    timeout=30.0,                          # Optional: Request timeout in seconds (default: 30.0)
    base_url="https://api.tally.so",       # Optional: Custom base URL (default: https://api.tally.so)
)
```

## Testing

The project includes two test layers:

- Unit tests for `TallyClient` and forms serialization/parsing
- Live read-only API tests for listing forms and form submissions

```bash
PYTHONPATH=src python -m pytest tests/test_client.py tests/resources/test_forms.py
```

```bash
export TALLY_API_KEY="tly_your_api_key_here"
export TALLY_FORM_ID="your_form_id"
PYTHONPATH=src python -m pytest -m live_api tests/integration/test_forms_live.py
```

## Next Steps

- 🔑 [Get your API Key](api-keys.md) - Learn how to obtain API keys from Tally
- 📖 [API Reference](api-reference/users.md) - Explore all available methods
- ⚠️ [Error Handling](error-handling.md) - Learn about exception handling

## Links

- [PyPI Package](https://pypi.org/project/pytally-sdk/)
- [GitHub Repository](https://github.com/felipeadeildo/pytally-sdk)
- [Official Tally API Documentation](https://developers.tally.so/api-reference/introduction)
- [Issue Tracker](https://github.com/felipeadeildo/pytally-sdk/issues)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/felipeadeildo/pytally-sdk/blob/main/LICENSE) file for details.

!!! warning "Disclaimer"
    This is an unofficial SDK and is not affiliated with or endorsed by Tally. Tally and the Tally logo are trademarks of Tally B.V.
