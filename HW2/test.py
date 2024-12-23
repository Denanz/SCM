import unittest
from visualizer import DependencyVisualizer

class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        self.visualizer = DependencyVisualizer("test_config.xml")
        self.visualizer.dependencies = {
            "SomePackage": ["PackageA", "PackageB"],
            "PackageA": ["PackageC"],
            "PackageB": ["PackageD"],
            "PackageC": [],
            "PackageD": ["PackageE"],
            "PackageE": []
        }

    def test_generate_graphviz_dot(self):
        expected_dot = (
            "digraph G {\n"
            "    \"SomePackage\" -> \"PackageA\";\n"
            "    \"SomePackage\" -> \"PackageB\";\n"
            "    \"PackageA\" -> \"PackageC\";\n"
            "    \"PackageB\" -> \"PackageD\";\n"
            "    \"PackageD\" -> \"PackageE\";\n"
            "}"
        )
        self.assertEqual(self.visualizer.generate_graphviz_dot(), expected_dot)

    def test_fetch_dependencies(self):
        self.visualizer.dependencies = {}
        self.visualizer.fetch_dependencies("SomePackage")
        self.assertIn("SomePackage", self.visualizer.dependencies)
        self.assertIn("PackageA", self.visualizer.dependencies)
        self.assertIn("PackageD", self.visualizer.dependencies)

if __name__ == "__main__":
    unittest.main()
