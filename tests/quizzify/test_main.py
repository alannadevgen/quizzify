"""Test main object."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from quizzify.main import app

V1_PREFIX = "/v1"


@pytest.fixture(scope="session")
def quizzify_test_app() -> FastAPI:
    """Create a FastAPI application for testing."""
    with TestClient(app) as client:
        yield client
