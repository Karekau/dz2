import sys
import pkg_resources
import argparse
from collections import defaultdict

def get_dependencies(package_name):
    """Получить зависимости пакета, включая транзитивные."""
    dependencies = defaultdict(list)

    try:
        # Получаем информацию о пакете
        dist = pkg_resources.get_distribution(package_name)
        # Получаем зависимости
        for req in dist.requires():
            dependencies[package_name].append(req.project_name)
            # Рекурсивно получаем зависимости
            sub_dependencies = get_dependencies(req.project_name)
            for sub_dep in sub_dependencies:
                dependencies[package_name].append(sub_dep)
    except pkg_resources.DistributionNotFound:
        print(f"Пакет '{package_name}' не найден.")
    
    return dependencies

def generate_plantuml(dependencies, package_name):
    """Генерирует код PlantUML из зависимостей."""
    plantuml_code = ["@startuml"]
    
    for parent, children in dependencies.items():
        for child in children:
            plantuml_code.append(f"{parent} --> {child}")
    
    plantuml_code.append("@enduml")
    return "\n".join(plantuml_code)

def main():
    parser = argparse.ArgumentParser(description='Визуализатор зависимостей Python пакетов.')
    parser.add_argument('visualizer_path', help='Путь к программе для визуализации графов.')
    parser.add_argument('package_name', help='Имя анализируемого пакета.')
    parser.add_argument('output_file', help='Путь к файлу-результату в виде кода.')
    parser.add_argument('repository_url', help='URL-адрес репозитория.')

    args = parser.parse_args()

    # Получаем зависимости
    dependencies = get_dependencies(args.package_name)

    # Генерируем код PlantUML
    plantuml_code = generate_plantuml(dependencies, args.package_name)

    # Записываем код в файл
    with open(args.output_file, 'w') as f:
        f.write(plantuml_code)

    # Выводим код на экран
    print(plantuml_code)

if __name__ == "__main__":
    main()
