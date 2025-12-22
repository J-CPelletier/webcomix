import docker
import pytest

from webcomix.docker import DockerManager, CONTAINER_NAME


@pytest.fixture
def cleanup_container():
    yield None
    client = docker.from_env()
    for container in client.containers.list():
        if container.attrs["Config"]["Image"] == CONTAINER_NAME:
            container.kill()


def test_no_javascript_spawns_no_container(cleanup_container):
    manager = DockerManager(False)
    manager.__enter__()
    manager.client = docker.from_env()
    assert manager._get_container() is None


def test_javascript_spawns_container(cleanup_container):
    manager = DockerManager(True)
    manager.__enter__()
    assert manager._get_container() is not None
    manager.__exit__(None, None, None)


def test_javascript_exit_removes_container(cleanup_container):
    manager = DockerManager(True)
    manager.__enter__()
    manager.__exit__(None, None, None)
    assert manager._get_container() is None
