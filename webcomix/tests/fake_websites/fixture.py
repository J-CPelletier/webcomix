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


@pytest.fixture
def one_webpage_uri():
    return str(
        get_dir_path_of_script().joinpath("one_webpage/1.html").resolve().as_uri()
    )


@pytest.fixture
def one_webpage_searchable_uri():
    return str(
        get_dir_path_of_script()
        .joinpath("one_webpage_searchable/1.html")
        .resolve()
        .as_uri()
    )
