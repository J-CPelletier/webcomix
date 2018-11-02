import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--check-supported-comics",
        action="store_true",
        default=False,
        help="checks if supported comics XPath are still working",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--check-supported-comics"):
        return
    skip_slow = pytest.mark.skip(reason="need --check-supported_comics option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
