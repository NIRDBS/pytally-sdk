# PyTally SDK

> Unofficial Python SDK for the [Tally.so](https://tally.so) API.

[![PyPI version](https://badge.fury.io/py/pytally-sdk.svg)](https://badge.fury.io/py/pytally-sdk)
[![Python Versions](https://img.shields.io/pypi/pyversions/pytally-sdk.svg)](https://pypi.org/project/pytally-sdk/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Docs](https://img.shields.io/badge/docs-online-brightgreen)](https://nirdbs.github.io/pytally-sdk/)

---

## Overview

**PyTally SDK** is a lightweight, fully typed Python client for the [Tally.so API](https://tally.so).
It provides a clean, Pythonic interface for authenticating, querying, and managing Tally resources -- without worrying about HTTP requests or pagination.

### Implemented Resources

- [x] Users
- [x] Organizations
- [x] Forms
- [x] Workspaces
- [x] Webhooks
- [ ] MCP

---

## Installation

### pip

```bash
pip install pytally-sdk
```

### uv (recommended)

```bash
uv add pytally-sdk
```

**Requirements:**
Python ≥ 3.11
`httpx` (auto-installed)

Validated against Tally API version `2025-05-30`.

---

## Quick Start

```python
from tally import SUPPORTED_TALLY_API_VERSION, Tally

client = Tally(
    api_key="tly_your_api_key_here",
    api_version=SUPPORTED_TALLY_API_VERSION,
)

user = client.users.me()
print(f"Hello, {user.full_name} ({user.email})")
```

### With Context Manager

```python
from tally import SUPPORTED_TALLY_API_VERSION, Tally

with Tally(
    api_key="tly_your_api_key_here",
    api_version=SUPPORTED_TALLY_API_VERSION,
) as client:
    for form in client.forms:
        print(f"{form.name} ({form.id})")
```

---

## Forms — Example Usage

### List Forms

```python
from tally import SUPPORTED_TALLY_API_VERSION, Tally

client = Tally(
    api_key="tly_your_api_key_here",
    api_version=SUPPORTED_TALLY_API_VERSION,
)

# Get first page of forms
forms = client.forms.all(page=1, limit=10)
print(f"Page {forms.page}, total={forms.total}")

for form in forms.items:
    print(f"{form.name} ({form.id}) → {form.status.value}")
```

### List Form Submissions

```python
from tally import SUPPORTED_TALLY_API_VERSION, Tally
from tally.models import SubmissionFilter

client = Tally(
    api_key="tly_your_api_key_here",
    api_version=SUPPORTED_TALLY_API_VERSION,
)

result = client.forms.list_submissions(
    "your_form_id",
    page=1,
    filter=SubmissionFilter.ALL,
)

print(result.total_number_of_submissions_per_filter.all)
for submission in result.submissions:
    print(submission.id, submission.submitted_at)
```

For complete API usage, visit the [📘 Forms Reference](https://nirdbs.github.io/pytally-sdk/api-reference/forms/).

---

## Error Handling

```python
from tally import Tally, UnauthorizedError, NotFoundError

client = Tally(api_key="tly_invalid")

try:
    client.users.me()
except UnauthorizedError:
    print("Invalid API key.")
except NotFoundError:
    print("Resource not found.")
```

See [Error Handling → docs](https://nirdbs.github.io/pytally-sdk/error-handling/).

---

## Documentation

👉 Full documentation and API reference available at:
**[https://nirdbs.github.io/pytally-sdk/](https://nirdbs.github.io/pytally-sdk/)**

---

## Development

Wanna help improve the SDK?

```bash
git clone https://github.com/felipeadeildo/pytally-sdk.git
cd pytally-sdk
uv sync --dev
uv run mkdocs serve  # preview docs locally
pre-commit install   # install pre-commit hooks
```

### Tests

Unit tests:

```bash
PYTHONPATH=src python -m pytest tests/test_client.py tests/resources/test_forms.py
```

Live read-only tests:

```bash
export TALLY_API_KEY="tly_your_api_key_here"
export TALLY_FORM_ID="your_form_id"
export TALLY_API_VERSION="2025-05-30"
PYTHONPATH=src python -m pytest -m live_api tests/integration/test_forms_live.py
```

---

## 🔗 Links

* 📦 [PyPI Package](https://pypi.org/project/pytally-sdk/)
* 💻 [GitHub Repository](https://github.com/NIRDBS/pytally-sdk)
* 🧾 [Tally API Reference](https://developers.tally.so/api-reference/introduction)
* 🪲 [Issue Tracker](https://github.com/NIRDBS/pytally-sdk/issues)
* 📘 [Documentation](https://nirdbs.github.io/pytally-sdk/)

---

## ⚖️ License

Licensed under the [Apache License 2.0](https://github.com/felipeadeildo/pytally-sdk/blob/main/LICENSE).

> **Disclaimer**
> This is an unofficial SDK and is not affiliated with or endorsed by Tally.
> “Tally” and the Tally logo are trademarks of Tally B.V.
