"""
Модуль для визуализации графа зависимостей.
Генерирует представление на языке D2 и сохраняет в SVG.
"""
import subprocess
import os
import tempfile


class Visualizer:
    """Класс для визуализации графа зависимостей."""
    
    def __init__(self, graph, output_file="graph.svg"):
        """
        Инициализация.
        
        Args:
            graph: Словарь графа зависимостей
            output_file: Имя выходного файла SVG
        """
        self.graph = graph
        self.output_file = output_file
    
    def generate_d2_code(self):
        """
        Сгенерировать код на языке D2 для графа.
        
        Returns:
            Строка с кодом D2
        """
        lines = []
        lines.append("// Dependency graph visualization")
        lines.append("")
        
        # Собираем все пакеты
        all_packages = set()
        root_packages = set()  # Пакеты, которые не являются зависимостями других
        for package, deps in self.graph.items():
            all_packages.add(package)
            all_packages.update(deps)
            root_packages.add(package)
        
        # Убираем из корневых те, которые являются зависимостями
        for package, deps in self.graph.items():
            for dep in deps:
                if dep in root_packages:
                    root_packages.discard(dep)
        
        # Если есть корневой пакет, выделяем его
        if root_packages:
            root_pkg = list(root_packages)[0]
            lines.append(f'{self._escape_d2_identifier(root_pkg)}: {{')
            lines.append(f'  label: "{root_pkg}"')
            lines.append(f'  style.fill: "#4A90E2"')
            lines.append(f'  style.stroke: "#2E5C8A"')
            lines.append(f'  style.stroke-width: 3')
            lines.append('}')
            lines.append("")
        
        # Определяем стили для зависимостей
        # Находим глубину каждого узла для цветового кодирования
        depth_map = self._calculate_depths(root_packages if root_packages else set(self.graph.keys()))
        colors = ["#E8F4F8", "#D4E8F1", "#B8D9E8", "#9CC5DF", "#7FB1D6", "#639DCD"]
        
        # Создаем узлы с стилями
        for package in sorted(all_packages):
            if package in root_packages:
                continue  # Уже создан выше
            
            depth = depth_map.get(package, 0)
            color = colors[min(depth, len(colors) - 1)]
            
            lines.append(f'{self._escape_d2_identifier(package)}: {{')
            lines.append(f'  label: "{package}"')
            lines.append(f'  style.fill: "{color}"')
            lines.append(f'  style.stroke: "#5A7A9A"')
            lines.append('}')
        
        lines.append("")
        
        # Определяем связи
        for package, deps in self.graph.items():
            for dep in deps:
                pkg_escaped = self._escape_d2_identifier(package)
                dep_escaped = self._escape_d2_identifier(dep)
                lines.append(f'{pkg_escaped} -> {dep_escaped}')
        
        return '\n'.join(lines)
    
    def _calculate_depths(self, root_packages):
        """
        Вычислить минимальную глубину каждого узла от корня.
        
        Args:
            root_packages: Множество корневых пакетов
            
        Returns:
            Словарь: пакет -> глубина
        """
        depth_map = {}
        queue = [(pkg, 0) for pkg in root_packages]
        
        while queue:
            package, depth = queue.pop(0)
            
            # Если уже посетили с меньшей глубиной, пропускаем
            if package in depth_map and depth_map[package] <= depth:
                continue
            
            depth_map[package] = depth
            
            if package in self.graph:
                for dep in self.graph[package]:
                    # Добавляем зависимость с увеличенной глубиной
                    queue.append((dep, depth + 1))
        
        return depth_map
    
    def _escape_d2_identifier(self, identifier):
        """
        Экранировать идентификатор для D2.
        
        Args:
            identifier: Имя пакета
            
        Returns:
            Экранированное имя
        """
        # Если содержит специальные символы, заключаем в кавычки
        if any(c in identifier for c in ['-', '.', ' ', ':', '/', '\\']):
            return f'"{identifier}"'
        return identifier
    
    def save_d2_file(self, d2_code, filename="graph.d2"):
        """
        Сохранить код D2 в файл.
        
        Args:
            d2_code: Код на языке D2
            filename: Имя файла
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(d2_code)
        return filename
    
    def generate_svg(self, d2_file=None):
        """
        Сгенерировать SVG из D2 файла.
        
        Args:
            d2_file: Путь к файлу D2 (если None, создается временный)
            
        Returns:
            Путь к созданному SVG файлу
        """
        # Генерируем D2 код
        d2_code = self.generate_d2_code()
        
        # Сохраняем во временный файл, если не указан
        if d2_file is None:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.d2', delete=False, encoding='utf-8') as f:
                f.write(d2_code)
                d2_file = f.name
        
        try:
            # Проверяем наличие d2
            try:
                subprocess.run(['d2', '--version'], 
                             capture_output=True, 
                             check=True, 
                             timeout=5)
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                print("Warning: D2 compiler not found. Install it from https://d2lang.com/")
                print("D2 code saved to:", d2_file)
                print("\nTo generate SVG, run:")
                print(f"  d2 {d2_file} {self.output_file}")
                return None
            
            # Компилируем D2 в SVG
            result = subprocess.run(
                ['d2', d2_file, self.output_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"Error generating SVG: {result.stderr}")
                print("D2 code saved to:", d2_file)
                return None
            
            print(f"SVG file generated: {self.output_file}")
            return self.output_file
        
        except Exception as e:
            print(f"Error during SVG generation: {e}")
            print("D2 code saved to:", d2_file)
            return None
    
    def visualize(self):
        """
        Выполнить полную визуализацию: сгенерировать D2 код и SVG.
        
        Returns:
            Путь к созданному SVG файлу или None
        """
        d2_code = self.generate_d2_code()
        d2_file = self.output_file.replace('.svg', '.d2')
        self.save_d2_file(d2_code, d2_file)
        
        print("\nD2 code:")
        print("=" * 50)
        print(d2_code)
        print("=" * 50)
        
        return self.generate_svg(d2_file)

