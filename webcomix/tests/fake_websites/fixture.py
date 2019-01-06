import os
from pathlib import Path

import pytest


def get_dir_path_of_script():
    return Path(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def three_webpages_uri():
    return str(
        get_dir_path_of_script().joinpath("three_webpages/1.html").resolve().as_uri()
    )
