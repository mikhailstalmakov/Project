# Инструмент визуализации графа зависимостей

## Общее описание
Это CLI-приложение для визуализации графа зависимостей пакетов Python. Разработка ведется поэтапно согласно требованиям практической работы.

## Этап 1: Минимальный прототип с конфигурацией
- Конфигурация задается в XML-файле.
- Параметры: имя пакета, URL репозитория, режим тестирования, имя выходного файла, подстрока фильтра.
- При запуске выводятся все параметры в формате ключ-значение.
- Реализована обработка ошибок для всех параметров.

## Описание функций и настроек
- `package_name`: Имя анализируемого пакета.
- `repo_url`: URL-адрес репозитория или путь к тестовому репозиторию.
- `test_mode`: Режим работы с тестовым репозиторием (true/false).
- `output_file`: Имя сгенерированного файла с изображением графа.
- `filter_substring`: Подстрока для фильтрации пакетов.

## Описание команд для сборки проекта и запуска тестов
Проект на Python, не требует сборки. Запуск:
```
python main.py config.xml
```

## Примеры использования
Пример config.xml:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
    <package_name>requests</package_name>
    <repo_url>https://pypi.org/pypi/requests/json</repo_url>
    <test_mode>false</test_mode>
    <output_file>graph.svg</output_file>
    <filter_substring>test</filter_substring>
</config>
```

Запуск:
```
python main.py config.xml
```

Вывод:
```
Configuration parameters:
package_name: requests
repo_url: https://pypi.org/pypi/requests/json
test_mode: False
output_file: graph.svg
filter_substring: test
