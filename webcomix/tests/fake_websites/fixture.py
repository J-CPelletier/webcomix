from pathlib import Path

import pytest

@pytest.fixture
def fake_website_uri(path):
    return str(Path(path).resolve().as_uri())
