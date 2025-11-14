#!/usr/bin/env python3
"""
depvis_stage1.py
Минимальный CLI-прототип (Этап 1) для проекта "визуализация графа зависимостей".

Требования этапа 1:
1. Источником настраиваемых параметров является конфигурационный файл формата XML.
2. К настраиваемым параметрам относятся:
   - Имя анализируемого пакета
   - URL-адрес репозитория или путь к файлу тестового репозитория
   - Режим работы с тестовым репозиторием
   - Имя сгенерированного файла с изображением графа
   - Подстрока для фильтрации пакетов
3. При запуске вывести все параметры в формате ключ=значение.
4. Реализовать обработку ошибок для всех параметров.
"""
import argparse
import sys
import os
import xml.etree.ElementTree as ET
from urllib.parse import urlparse


# Обязательные параметры конфигурации
REQUIRED_KEYS = [
    "package_name",
    "repo_url_or_path",
    "test_repo_mode",
    "output_image_name",
    "filter_substring"
]


def error(msg, exit_code=1):
    """Вывести сообщение об ошибке и завершить программу."""
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(exit_code)


def parse_bool(text):
    """
    Парсит текстовое булево значение.
    Возвращает True, False или None если значение некорректно.
    """
    if text is None:
        return None
    text_lower = text.strip().lower()
    if text_lower in ("1", "true", "yes", "y"):
        return True
    if text_lower in ("0", "false", "no", "n"):
        return False
    return None


def is_url(s: str) -> bool:
    """Проверяет, является ли строка URL-адресом."""
    try:
        parsed = urlparse(s)
        return parsed.scheme in ("http", "https", "git", "ssh")
    except Exception:
        return False


def read_config(config_path: str) -> dict:
    """
    Читает XML-конфигурационный файл и извлекает параметры.
    
    Структура XML:
    <config>
        <package_name>...</package_name>
        <repo_url_or_path>...</repo_url_or_path>
        <test_repo_mode>...</test_repo_mode>
        <output_image_name>...</output_image_name>
        <filter_substring>...</filter_substring>
    </config>
    """
    # Проверка существования файла
    if not os.path.isfile(config_path):
        error(f"Файл конфигурации не найден: {config_path}")
    
    # Парсинг XML
    try:
        tree = ET.parse(config_path)
        root = tree.getroot()
    except ET.ParseError as e:
        error(f"Ошибка парсинга XML: {e}")
    
    # Извлечение параметров
    config = {}
    for key in REQUIRED_KEYS:
        element = root.find(key)
        if element is None:
            # Элемент отсутствует в XML
            config[key] = None
        else:
            # Элемент существует, извлекаем текст
            # element.text может быть None для пустых элементов <key></key>
            if element.text is None:
                # Пустой элемент - присваиваем пустую строку
                config[key] = ""
            else:
                # Элемент с текстом - обрезаем пробелы
                text = element.text.strip()
                config[key] = text
    
    return config


def validate_config(config: dict, config_path: str) -> dict:
    """
    Валидирует все параметры конфигурации.
    Возвращает словарь с валидными параметрами.
    """
    validated = {}
    
    # 1. Проверка наличия всех обязательных параметров
    for key in REQUIRED_KEYS:
        if key == "filter_substring":
            # filter_substring может быть пустой строкой (фильтр отключен)
            if config.get(key) is None:
                error(f"Параметр '{key}' отсутствует в конфиге {config_path}")
        else:
            # Остальные параметры обязательны и не могут быть пустыми
            if config.get(key) is None or config.get(key) == "":
                error(f"Параметр '{key}' отсутствует или пуст в конфиге {config_path}")
    
    # 2. Валидация package_name (не должен содержать пробелов)
    package_name = config["package_name"]
    if any(c.isspace() for c in package_name):
        error("package_name содержит пробельные символы — допустимо непрерывное имя пакета.")
    validated["package_name"] = package_name
    
    # 3. Валидация test_repo_mode (должно быть булевым значением)
    test_repo_mode_str = config["test_repo_mode"]
    test_repo_mode = parse_bool(test_repo_mode_str)
    if test_repo_mode is None:
        error("test_repo_mode должен быть булевым значением (true/false, 1/0, yes/no).")
    validated["test_repo_mode"] = test_repo_mode
    
    # 4. Валидация repo_url_or_path
    repo_url_or_path = config["repo_url_or_path"]
    if test_repo_mode:
        # В тестовом режиме ожидаем путь к существующему файлу
        if not os.path.isfile(repo_url_or_path):
            error(f"В режиме тестирования путь к файлу репозитория должен существовать: {repo_url_or_path}")
    else:
        # В рабочем режиме ожидаем URL (но допускаем путь с предупреждением)
        if not is_url(repo_url_or_path):
            print(f"WARNING: repo_url_or_path выглядит не как URL. Будет использован как путь: {repo_url_or_path}", 
                  file=sys.stderr)
    validated["repo_url_or_path"] = repo_url_or_path
    
    # 5. Валидация output_image_name
    output_image_name = config["output_image_name"]
    if output_image_name.strip() == "":
        error("output_image_name не должен быть пустым.")
    # Проверка на недопустимые символы
    if "\x00" in output_image_name:
        error("output_image_name содержит недопустимые символы.")
    # Создание директории, если указана
    output_dir = os.path.dirname(output_image_name) or "."
    if output_dir and not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            error(f"Невозможно создать каталог для output_image_name: {output_dir}: {e}")
    validated["output_image_name"] = output_image_name
    
    # 6. Валидация filter_substring (может быть пустой, максимум 200 символов)
    filter_substring = config.get("filter_substring") or ""
    if len(filter_substring) > 200:
        error("filter_substring слишком длинная (макс 200 символов).")
    validated["filter_substring"] = filter_substring
    
    return validated


def print_config(params: dict):
    """
    Выводит все параметры конфигурации в формате ключ=значение.
    Это требование этапа 1.
    """
    for key in REQUIRED_KEYS:
        value = params.get(key)
        # Преобразование булевого значения в строку
        if isinstance(value, bool):
            value = "true" if value else "false"
        print(f"{key}={value}")


def main():
    """Главная функция программы."""
    parser = argparse.ArgumentParser(
        description="depvis — инструмент визуализации графа зависимостей (Этап 1)."
    )
    parser.add_argument(
        "-c", "--config",
        required=True,
        help="Путь к XML-конфигурационному файлу"
    )
    args = parser.parse_args()
    
    # Чтение и валидация конфигурации
    config_raw = read_config(args.config)
    config_validated = validate_config(config_raw, args.config)
    
    # Вывод всех параметров в формате ключ=значение (требование этапа 1)
    print_config(config_validated)
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nПрервано пользователем.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        error(f"Неожиданная ошибка: {e}")
