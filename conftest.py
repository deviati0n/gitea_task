import time

import docker
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from project_config.project_context import ProjectContext

context = ProjectContext()


@pytest.fixture(autouse=True, scope="session")
def generate_container():
    client = docker.from_env()
    container = client.containers.run(
        image='gitea/gitea:latest',
        ports={'3000/tcp': ('0.0.0.0', 3000)},
        detach=True
    )
    time.sleep(2)

    yield container

    container.stop()
    container.remove()


@pytest.fixture(scope="session")
def get_webdriver():
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(service=Service(context.test_config.get_chrome_path), options=options)
    driver.implicitly_wait(3)

    yield driver

    driver.close()
