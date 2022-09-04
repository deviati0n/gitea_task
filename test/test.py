import time
from http.client import RemoteDisconnected
from io import StringIO

import requests
from lxml import etree
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from urllib3.exceptions import ProtocolError

from project_config.project_context import ProjectContext

context = ProjectContext()


def test_container():
    """
    Проверка, что веб-страница сервиса Gitea на целевом порту доступна
    и на ней находится 4 эталонных css-селектора + эталонный текст
    """
    try:
        response = requests.get(context.gitea_config.root_url)
    except (RemoteDisconnected, ProtocolError, ConnectionError):
        raise Exception('Веб-страница недоступна.')

    assert response.status_code == 200

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(response.text), parser)
    test_checkers = [
        '//*[@class="page-content install"]',
        '//*[@class="ui primary button"]',
        '//*[@class="ui language bottom floating slide up dropdown link item"]',
        '//*[@class="ui right links"]',
        '//*[contains(text(), "Gitea HTTP")]'
    ]

    assert all(tree.xpath(el) for el in test_checkers) is True


def test_registration(run_webdriver: 'webdriver.Chrome'):
    """
    Регистрации нового пользователя на сервисе Gitea с помощью Selenium
    :param run_webdriver: экземпляр веб-драйвера
    :return: None
    """
    driver = run_webdriver
    driver.get(context.gitea_config.root_url)

    driver.find_element(By.XPATH, f'//button[@class="ui primary button"]').click()
    for i in range(10):
        try:
            driver.find_element(By.XPATH, f'//a[contains(@href, "/sign_up")]').click()
            break
        except NoSuchElementException:
            time.sleep(3)
            driver.get(context.gitea_config.root_url)

    assert 'Регистрация - Gitea' in driver.title

    elements_name = {
        'user_name': 'user_name',
        'email': 'test_email@gitea.com',
        'password': 'password',
        'retype': 'password'
    }

    for k, v in elements_name.items():
        elements = driver.find_element(By.NAME, k)
        elements.clear()
        elements.send_keys(v)

    driver.find_element(By.XPATH, f'//button[contains(text(), "Регистрация аккаунта")]').click()


def test_create_repository(run_webdriver: 'webdriver.Chrome'):
    """
    Создание нового репозитория на сервисе Gitea с помощью Selenium
    :param run_webdriver: экземпляр веб-драйвера
    :return: None
    """
    driver = run_webdriver
    driver.get(context.gitea_config.root_url)
    driver.find_element(By.XPATH, f'//*[@id="dashboard-repo-list"]/div/div[2]/h4/a').click()

    repo_name = driver.find_element(By.NAME, 'repo_name')
    repo_name.clear()
    repo_name.send_keys(context.test_config.get_repo_name)

    driver.find_element(By.XPATH, f'//*[@id="auto-init"]').click()
    driver.find_element(By.XPATH, f'//button[contains(text(), "Создать репозиторий")]').click()


def test_create_commit(run_webdriver: 'webdriver.Chrome'):
    """
    Создание коммита файла с помощью Selenium
    :param run_webdriver: экземпляр веб-драйвера
    :return: None
    """
    driver = run_webdriver
    driver.find_element(By.XPATH, f'//a[contains(text(), "Новый файл")]').click()

    file_name = driver.find_element(By.ID, 'file-name')
    file_name.send_keys(context.test_config.get_file_name)

    driver.find_element(By.XPATH, f'//div[contains(@class, "view-overlays")]').click()

    driver.find_element(
        By.XPATH, f'//*[contains(@class,"inputarea monaco-mouse-cursor-text")]'
    ).send_keys(
        context.test_config.get_file_msg
    )

    commit_msg = driver.find_element(By.NAME, 'commit_summary')
    commit_msg.send_keys('create')

    commit_msg.submit()


def test_open_file(run_webdriver: 'webdriver.Chrome'):
    """
    Проверка, что итоговый текст в файле соответствует оригинальному
    :param run_webdriver: экземпляр веб-драйвера
    :return: None
    """
    driver = run_webdriver

    driver.find_element(By.XPATH, f'//a[contains(text(), "Исходник")]').click()
    output_text_file = driver.find_element(By.TAG_NAME, 'pre').text
    assert output_text_file == context.test_config.get_file_msg
