import xml.etree.ElementTree as ET
import subprocess
import tempfile
import sys
import platform

class DependencyVisualizer:
    def __init__(self, config_path):
        self.config = ET.parse(config_path).getroot()
        self.dot_path = self.config.find('.//dot').text
        self.package_name = self.config.find('.//package').text
        self.dependencies = {}

    def parse_dependencies(self, package_name):
        # Placeholder for parsing dependencies
        # Here we simulate parsing dependencies
        self.dependencies[package_name] = ['dependency1', 'dependency2']
        for dependency in self.dependencies[package_name]:
            if dependency not in self.dependencies:
                self.parse_dependencies(dependency)

    def generate_graphviz_code(self):
        dot_code = 'digraph G {\n'
        for package, deps in self.dependencies.items():
            for dep in deps:
                dot_code += f'    "{package}" -> "{dep}";\n'
        dot_code += '}'
        return dot_code

    def visualize(self):
        self.parse_dependencies(self.package_name)
        dot_code = self.generate_graphviz_code()
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.dot') as dot_file:
            dot_file.write(dot_code)
            dot_file_path = dot_file.name

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as png_file:
            png_file_path = png_file.name

        try:
            subprocess.run([self.dot_path, '-Tpng', dot_file_path, '-o', png_file_path], check=True)
            self.open_image(png_file_path)
        finally:
            # Clean up temporary files
            subprocess.run(['rm', dot_file_path], check=True)
            subprocess.run(['rm', png_file_path], check=True)

    def open_image(self, image_path):
        if platform.system() == 'Windows':
            subprocess.run(['start', image_path], shell=True)
        elif platform.system() == 'Darwin':
            subprocess.run(['open', image_path])
        else:
            subprocess.run(['xdg-open', image_path])

if __name__ == '__main__':
    visualizer = DependencyVisualizer('config.xml')
    visualizer.visualize()