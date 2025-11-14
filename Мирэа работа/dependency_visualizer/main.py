#!/usr/bin/env python3
# Test commit to verify git functionality
#2312
import sys
import os
from config import Config
def print_hello():
    print("hello")
def print_welcome():
    print("Welcome to dependency visualizer")

def main():
    print_welcome()
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        config = Config(config_file)
        config.print_params()
        
        # Этап 2: Вывести прямые зависимости
        dependencies = config.get_direct_dependencies()
        print("Direct dependencies:")
        for dep in dependencies:
            print(f"- {dep}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
