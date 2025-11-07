import xml.etree.ElementTree as ET
import os

class Config:
    def __init__(self, config_file):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
        
        tree = ET.parse(config_file)
        root = tree.getroot()
        
        self.package_name = self._get_text(root, 'package_name')
        self.repo_url = self._get_text(root, 'repo_url')
        self.test_mode = self._get_bool(root, 'test_mode')
        self.output_file = self._get_text(root, 'output_file')
        self.filter_substring = self._get_text(root, 'filter_substring')
    
    def _get_text(self, root, tag):
        element = root.find(tag)
        if element is None or element.text is None:
            raise ValueError(f"Missing or empty parameter: {tag}")
        return element.text.strip()
    
    def _get_bool(self, root, tag):
        text = self._get_text(root, tag)
        if text.lower() in ('true', '1', 'yes'):
            return True
        elif text.lower() in ('false', '0', 'no'):
            return False
        else:
            raise ValueError(f"Invalid boolean value for {tag}: {text}")
    
    def print_params(self):
        print("Configuration parameters:")
        print(f"package_name: {self.package_name}")
        print(f"repo_url: {self.repo_url}")
        print(f"test_mode: {self.test_mode}")
        print(f"output_file: {self.output_file}")
        print(f"filter_substring: {self.filter_substring}")
