import docker
from time import sleep

CONTAINER_NAME = "scrapinghub/splash"


class DockerManager:
    def __init__(self, javascript):
        self.javascript = javascript

    def __enter__(self):
        if self.javascript:
            self.client = docker.from_env()
            running = self._container_running()
            if running:
                return None
            self.client.containers.run(
                CONTAINER_NAME, detach=True, ports={"8050/tcp": 8050}
            )
            print("Container started")
            sleep(0.5)
            print("Container ready")

    def __exit__(self, exc_type, exc_value, tb):
        if self.javascript:
            container = self._get_container()
            if container is not None:
                container.kill()
        if exc_type is not None:
            return False
        return True

    def _container_running(self):
        return self._get_container() is not None

    def _get_container(self):
        containers = self.client.containers.list()
        for container in containers:
            if container.attrs["Config"]["Image"] == CONTAINER_NAME:
                return container
        return None
