import os
import xml.etree.ElementTree as ET
import subprocess
from typing import Dict, List

class DependencyVisualizer:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.graphviz_path = None
        self.package_name = None
        self.dependencies = {}

    def parse_config(self):
        tree = ET.parse(self.config_path)
        root = tree.getroot()

        paths = root.find('paths')
        if paths is None:
            raise ValueError("Missing 'paths' element in configuration file.")

        self.graphviz_path = paths.find('dot').text if paths.find('dot') is not None else None
        self.package_name = paths.find('package').text if paths.find('package') is not None else None

        if not self.graphviz_path:
            raise ValueError("Missing 'dot' element in 'paths' in configuration file.")
        if not self.package_name:
            raise ValueError("Missing 'package' element in 'paths' in configuration file.")

        if not os.path.exists(self.graphviz_path):
            raise FileNotFoundError(f"Graphviz program not found at {self.graphviz_path}")

    def fetch_dependencies(self, package_name: str):
        simulated_dependencies = {
            "SomePackage": ["PackageA", "PackageB", "PackageC"],
            "PackageA": ["PackageC"],
            "PackageB": ["PackageD"],
            "PackageC": [],
            "PackageD": ["PackageE"],
            "PackageE": []
        }

        self.dependencies[package_name] = simulated_dependencies.get(package_name, [])
        for dep in self.dependencies[package_name]:
            if dep not in self.dependencies:
                self.fetch_dependencies(dep)

    def generate_graphviz_dot(self) -> str:
        lines = ["digraph G {"]
        for package, deps in self.dependencies.items():
            for dep in deps:
                lines.append(f'    "{package}" -> "{dep}";')
        lines.append("}")
        return "\n".join(lines)

    def visualize_graph(self, dot_content: str):
        dot_file = "output.dot"
        png_file = "output.png"

        with open(dot_file, "w") as f:
            f.write(dot_content)

        subprocess.run([self.graphviz_path, "-Tpng", dot_file, "-o", png_file], check=True)
        print(f"Graph visualization saved to {png_file}")

    def run(self):
        self.parse_config()
        self.fetch_dependencies(self.package_name)
        dot_content = self.generate_graphviz_dot()
        self.visualize_graph(dot_content)

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "config.xml")
    visualizer = DependencyVisualizer(config_path)
    visualizer.run()
