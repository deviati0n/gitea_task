# Тестовое задание

Скрипт запускает контейнер с образом Gitea и выполняет ряд тестов.

## Установка 

``` commandline
$ git clone https://github.com/deviati0n/gitea_task.git <project_name>
$ cd <project_name>
$ pip install -r requirements.txt
```

Переименовать `default_config.py` в `config.py`. </br>
Загрузить на свой компьютер `chromedriver.exe` и прописать путь к нему в конфиге.


## Запуск
Проверьте, что Docker запущен и целевой порт (3000) свободен. 

Если есть желание, чтобы Selenium запускал браузер явно, то в `test/conftest.py` изменить `options.headless = True`.

``` commandline
$ pytest test/test.py
```