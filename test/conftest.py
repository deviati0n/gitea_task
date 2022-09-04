import time

import docker
import pytest
from docker.errors import APIError
from requests.exceptions import HTTPError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from project_config.project_context import ProjectContext

context = ProjectContext()


@pytest.fixture(autouse=True, scope="session")
def run_container():
    """
    Запуск контейнера, который активен до тех пор, пока скрипт работает.
    После он останавливается и удаляется
    """
    client = docker.from_env()
    try:
        container = client.containers.run(
            image='gitea/gitea:1.17.1',
            ports={'3000/tcp': ('0.0.0.0', 3000)},
            detach=True
        )
    except (HTTPError, APIError):
        raise Exception('Целевой порт (3000) контейнера уже занят.')

    while container.attrs['State']['Running'] is not True:
        time.sleep(5)
        container.reload()

    yield container
    container.stop()
    container.remove()


@pytest.fixture(scope="session")
def run_webdriver():
    """
    Запуск веб-драйвера, который также активен до тех пор, пока скрипт работает
    """
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(service=Service(context.test_config.get_chrome_path), options=options)
    driver.implicitly_wait(3)

    yield driver

    driver.close()
