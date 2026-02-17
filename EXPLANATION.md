# Bug Fix Explanation

## What was the bug?

The `Client.request()` method had a logic error when checking token expiration for API requests. When `oauth2_token` was a dict (instead of an `OAuth2Token` instance), the code skipped the expiration check and refresh logic, directly using the stale token.

The problematic code was:
```python
if not self.oauth2_token or (
    isinstance(self.oauth2_token, OAuth2Token) and self.oauth2_token.expired
):
    self.refresh_oauth2()
```

This only refreshed tokens if they were missing OR if they were an `OAuth2Token` instance AND expired. Dict tokens were never checked.

## Why did it happen?

The developer assumed `oauth2_token` would only be in two states: `None` or a valid `OAuth2Token` instance. However, the code's type annotation (`Union[OAuth2Token, Dict[str, Any], None]`) explicitly allows dicts, and `test_api_request_refreshes_when_token_is_dict` already tested this case. The refresh logic didn't account for dict tokens being stale, creating an edge case where expired dict tokens would be silently used.

## Why does your fix solve it?

The fix explicitly checks dict tokens for expiration before deciding to refresh:
```python
should_refresh = (
    not self.oauth2_token
    or (isinstance(self.oauth2_token, OAuth2Token) and self.oauth2_token.expired)
    or (isinstance(self.oauth2_token, dict) and self.oauth2_token.get("expires_at", 0) <= 0)
)
if should_refresh:
    self.refresh_oauth2()
```

Now both token types are checked before use, ensuring stale tokens (whether `OAuth2Token` or dict) always trigger a refresh.

## Edge case not covered

The tests assume `expires_at` in dict tokens is always an integer. If `expires_at` is a string or missing entirely, the comparison might not work as intended. A production fix should include explicit type validation or conversion of dict token timestamps.
