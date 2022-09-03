import time
from io import StringIO

import requests
from lxml import etree
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from project_config.project_context import ProjectContext

context = ProjectContext()


def test_container():
    response = None
    try:
        response = requests.get(context.gitea_config.root_url)
    except requests.exceptions.ConnectionError:
        time.sleep(3)

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


def test_registration(get_webdriver: webdriver.Chrome):
    driver = get_webdriver
    driver.get(context.gitea_config.root_url)

    driver.find_element(By.XPATH, f'//button[@class="ui primary button"]').click()
    for i in range(10):
        try:
            driver.find_element(By.XPATH, f'//a[contains(@href, "/sign_up")]').click()
            break
        except NoSuchElementException:
            time.sleep(3)
            driver.get(context.gitea_config.root_url)

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


def test_create_repository(get_webdriver: webdriver.Chrome):
    driver = get_webdriver
    driver.get(context.gitea_config.root_url)
    driver.find_element(By.XPATH, f'//*[@id="dashboard-repo-list"]/div/div[2]/h4/a').click()

    repo_name = driver.find_element(By.NAME, 'repo_name')
    repo_name.clear()
    repo_name.send_keys(context.test_config.get_repo_name)

    driver.find_element(By.XPATH, f'//*[@id="auto-init"]').click()
    driver.find_element(By.XPATH, f'//button[contains(text(), "Создать репозиторий")]').click()
    driver.find_element(By.XPATH, f'//a[contains(text(), "Новый файл")]').click()


def test_create_commit(get_webdriver: webdriver.Chrome):
    driver = get_webdriver
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


def test_open_file(get_webdriver: webdriver.Chrome):
    driver = get_webdriver

    driver.find_element(By.XPATH, f'//a[contains(text(), "Исходник")]').click()
    output_text_file = driver.find_element(By.TAG_NAME, 'pre').text
    assert output_text_file == context.test_config.get_file_msg
