"""
Tests for security module - verifies imports work when module is loaded directly
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-ci")

import hashlib
import hmac

import pytest
from app.core.security import (
    verify_api_key,
    hash_sensitive_data,
    verify_webhook_signature,
    setup_security,
    ContentSafetyMiddleware,
    DataProtectionMiddleware,
)


def test_security_module_imports():
    """Verify all expected symbols are importable from security module"""
    assert callable(verify_api_key)
    assert callable(hash_sensitive_data)
    assert callable(verify_webhook_signature)
    assert callable(setup_security)


def test_verify_api_key_empty():
    """verify_api_key returns False for empty/None/non-string input"""
    assert verify_api_key("") is False
    assert verify_api_key(None) is False


def test_verify_api_key_no_configured_keys():
    """verify_api_key returns False when no API keys are configured"""
    # settings.API_KEYS is None by default in test environment
    assert verify_api_key("some-key") is False


def test_hash_sensitive_data():
    """hash_sensitive_data returns a consistent SHA-256 hex string"""
    result = hash_sensitive_data("test-data")
    assert isinstance(result, str)
    assert len(result) == 64  # SHA-256 produces a 64-char hex string


def test_hash_sensitive_data_deterministic():
    """hash_sensitive_data returns the same value for the same input"""
    assert hash_sensitive_data("hello") == hash_sensitive_data("hello")


def test_hash_sensitive_data_different_inputs():
    """hash_sensitive_data returns different values for different inputs"""
    assert hash_sensitive_data("hello") != hash_sensitive_data("world")


def test_verify_webhook_signature_valid():
    """verify_webhook_signature returns True for a correct signature"""
    payload = b"test-payload"
    secret = "test-secret"
    expected_signature = hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()

    assert verify_webhook_signature(payload, expected_signature, secret) is True


def test_verify_webhook_signature_invalid():
    """verify_webhook_signature returns False for an incorrect signature"""
    assert (
        verify_webhook_signature(b"test-payload", "wrong-signature", "test-secret")
        is False
    )


def test_verify_webhook_signature_wrong_secret():
    """verify_webhook_signature returns False when secret is wrong"""
    payload = b"test-payload"
    correct_secret = "correct-secret"
    wrong_secret = "wrong-secret"
    signature = hmac.new(
        correct_secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    assert verify_webhook_signature(payload, signature, wrong_secret) is False


def test_verify_webhook_signature_empty_payload():
    """verify_webhook_signature handles empty payload"""
    payload = b""
    secret = "test-secret"
    signature = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    assert verify_webhook_signature(payload, signature, secret) is True


def test_middleware_classes_importable():
    """ContentSafetyMiddleware and DataProtectionMiddleware are importable classes"""
    assert ContentSafetyMiddleware is not None
    assert DataProtectionMiddleware is not None
