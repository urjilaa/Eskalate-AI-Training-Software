import time

import requests

from app.http_client import Client
from app.tokens import OAuth2Token, token_from_iso


def test_client_uses_requests_session():
    c = Client()
    assert isinstance(c.session, requests.Session)


def test_token_from_iso_uses_dateutil():
    t = token_from_iso("ok", "2099-01-01T00:00:00Z")
    assert isinstance(t, OAuth2Token)
    assert t.access_token == "ok"
    assert not t.expired


def test_api_request_sets_auth_header_when_token_is_valid():
    c = Client()
    c.oauth2_token = OAuth2Token(access_token="ok", expires_at=int(time.time()) + 3600)

    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer ok"


def test_api_request_refreshes_when_token_is_missing():
    c = Client()
    c.oauth2_token = None

    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer fresh-token"


def test_api_request_refreshes_when_token_is_dict():
    c = Client()
    c.oauth2_token = {"access_token": "stale", "expires_at": 0}

    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer fresh-token"


def test_api_request_refreshes_dict_token_with_negative_expiry():
    """Bug regression: dict tokens with negative/zero expiry should trigger refresh."""
    c = Client()
    c.oauth2_token = {"access_token": "stale", "expires_at": -1}

    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer fresh-token"


def test_api_request_uses_valid_dict_token():
    """Valid dict tokens should not trigger refresh, but also aren't used in headers."""
    c = Client()
    future_time = int(time.time()) + 3600
    c.oauth2_token = {"access_token": "valid", "expires_at": future_time}

    resp = c.request("GET", "/me", api=True)

    # When token is dict with valid expiry, no refresh should occur.
    # Dict tokens are never used in headers because the code only sets
    # Authorization header for OAuth2Token instances.
    assert resp["headers"].get("Authorization") is None


def test_non_api_request_ignores_token():
    """Non-API requests should not check or use tokens."""
    c = Client()
    c.oauth2_token = None

    resp = c.request("GET", "/public", api=False)

    assert "Authorization" not in resp["headers"]


def test_api_request_preserves_custom_headers():
    """Custom headers should not be overwritten by Authorization header."""
    c = Client()
    c.oauth2_token = OAuth2Token(access_token="ok", expires_at=int(time.time()) + 3600)

    resp = c.request("GET", "/me", api=True, headers={"X-Custom": "value"})

    assert resp["headers"].get("Authorization") == "Bearer ok"
    assert resp["headers"].get("X-Custom") == "value"
