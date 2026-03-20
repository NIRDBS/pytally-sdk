# Workspaces

The Workspaces resource covers listing, iterating, creating, fetching, updating, and deleting workspaces.

## Initialization

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")
```

## List Workspaces

### Method

```python
client.workspaces.all(page: int = 1) -> PaginatedWorkspaces
```

### Example

```python
result = client.workspaces.all(page=1)

print(result.page, result.total, result.has_more)
for workspace in result.items:
    print(workspace.id, workspace.name)
```

### Notes

- The returned collection is `items`, not `data`
- `PaginatedWorkspaces` exposes `page`, `limit`, `total`, and `has_more`

### Official Reference

[List Workspaces](https://developers.tally.so/api-reference/endpoint/workspaces/list)

---

## Iterate Workspaces

```python
for workspace in client.workspaces:
    print(workspace.name, len(workspace.members))
```

---

## Create Workspace

### Method

```python
client.workspaces.create(name: str) -> Workspace
```

### Example

```python
workspace = client.workspaces.create(name="Marketing Team")
print(workspace.id, workspace.name)
```

### Official Reference

[Create Workspace](https://developers.tally.so/api-reference/endpoint/workspaces/post)

---

## Get Workspace

### Method

```python
client.workspaces.get(workspace_id: str) -> Workspace
```

### Example

```python
workspace = client.workspaces.get("ws_123")
print(workspace.name)
print(len(workspace.members), len(workspace.invites))
```

### Official Reference

[Get Workspace](https://developers.tally.so/api-reference/endpoint/workspaces/get)

---

## Update Workspace

### Method

```python
client.workspaces.update(
    workspace_id: str,
    name: str,
) -> None
```

### Example

```python
client.workspaces.update("ws_123", name="Marketing and Sales")
```

### Notes

- The SDK currently treats this endpoint as returning no value

### Official Reference

[Update Workspace](https://developers.tally.so/api-reference/endpoint/workspaces/patch)

---

## Delete Workspace

### Method

```python
client.workspaces.delete(workspace_id: str) -> None
```

### Official Reference

[Delete Workspace](https://developers.tally.so/api-reference/endpoint/workspaces/delete)

---

## Models

### Workspace

::: tally.models.workspace.Workspace
    options:
      show_source: false
      heading_level: 4
      members: []

### PaginatedWorkspaces

::: tally.models.workspace.PaginatedWorkspaces
    options:
      show_source: false
      heading_level: 4
      members: []
