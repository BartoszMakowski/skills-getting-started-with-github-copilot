from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

BASE_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activities so tests stay isolated and deterministic."""
    app_module.activities.clear()
    app_module.activities.update(deepcopy(BASE_ACTIVITIES))
    yield
    app_module.activities.clear()
    app_module.activities.update(deepcopy(BASE_ACTIVITIES))


@pytest.fixture
def client():
    return TestClient(app_module.app)
