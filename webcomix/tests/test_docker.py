import docker

from webcomix.docker import DockerManager

def test_no_javascript_spawns_no_container():
    manager = DockerManager(False)
    manager.__enter__()
    manager.client = docker.from_env()
    assert manager._get_container() is None

def test_javascript_spawns_container():
    manager = DockerManager(True)
    manager.__enter__()
    assert manager._get_container() is not None
    manager.__exit__(None, None, None)

def test_javascript_exit_removes_container():
    manager = DockerManager(True)
    manager.__enter__()
    manager.__exit__(None, None, None)
    assert manager._get_container() is None
