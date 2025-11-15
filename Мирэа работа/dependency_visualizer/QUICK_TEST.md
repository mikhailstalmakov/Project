# Быстрая проверка работы программы

## Способ 1: Через командную строку (рекомендуется)

### Шаг 1: Откройте PowerShell или командную строку

### Шаг 2: Перейдите в директорию проекта
```powershell
cd "C:\Users\misha\OneDrive\Desktop\git мирэа работа\Project\Мирэа работа\dependency_visualizer"
```

### Шаг 3: Запустите программу

**Тест 1: Базовый тест с тестовым репозиторием**
```powershell
python main.py config_test.xml
```

**Тест 2: С фильтрацией**
```powershell
python main.py config_test_filter.xml
```

**Тест 3: Обратные зависимости**
```powershell
python main.py config_test.xml --reverse E
```

**Тест 4: Реальный пакет из PyPI**
```powershell
python main.py config.xml
```

## Способ 2: Через двойной клик (Windows)

Просто дважды кликните на файл `run_test.bat` в папке `dependency_visualizer`.

## Способ 3: Через VS Code

1. Откройте терминал в VS Code (Terminal → New Terminal)
2. Убедитесь, что вы в директории `dependency_visualizer`
3. Выполните команду:
   ```powershell
   python main.py config_test.xml
   ```

## Что должно произойти при успешном запуске

Вы увидите следующий вывод:

```
Welcome to dependency visualizer
Configuration parameters:
  package_name: A
  repo_url: test_repo.txt
  test_mode: True
  output_file: graph_test.svg
  filter_substring: 

============================================================
Stage 2: Direct Dependencies
============================================================
Direct dependencies of 'A':
  - B
  - C
  - D

============================================================
Stage 3: Dependency Graph Construction
============================================================
Dependency graph for 'A':
Total packages in graph: 26

A -> B, C, D
B -> E, F
C -> E, G
...

Warning: Circular dependencies detected:
  Cycle: Z -> A -> B -> ... -> Z

============================================================
Stage 5: Visualization
============================================================
D2 code:
==================================================
// Dependency graph visualization

A -> B
A -> C
...
==================================================
SVG file generated: graph_test.svg
```

## Если Python не найден

Попробуйте использовать `py` вместо `python`:
```powershell
py main.py config_test.xml
```

## Проверка всех этапов

- ✅ **Этап 1**: Параметры конфигурации выводятся в начале
- ✅ **Этап 2**: Прямые зависимости выводятся в разделе "Stage 2"
- ✅ **Этап 3**: Полный граф строится и выводятся циклы
- ✅ **Этап 4**: Используйте `--reverse` для проверки обратных зависимостей
- ✅ **Этап 5**: Генерируется D2 код и SVG файл

## Проверка обработки ошибок

### Тест отсутствующего файла:
```powershell
python main.py nonexistent.xml
```
Ожидается ошибка: `FileNotFoundError`

### Тест несуществующего пакета:
Измените в `config_test.xml` `package_name` на `NONEXISTENT` и запустите.
Ожидается: пустой список зависимостей (для тестового режима)

## Результаты

После успешного запуска будут созданы файлы:
- `graph_test.d2` - код на языке D2
- `graph_test.svg` - визуализация графа (если установлен D2)

