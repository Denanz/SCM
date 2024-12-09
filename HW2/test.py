import pytest
from tree import DependencyVisualizer
import tempfile
import subprocess

@pytest.fixture
def visualizer():
    return DependencyVisualizer('config.xml')

def test_parse_dependencies(visualizer):
    visualizer.parse_dependencies('SomePackage')
    assert 'SomePackage' in visualizer.dependencies
    assert len(visualizer.dependencies['SomePackage']) > 0

def test_generate_graphviz_code(visualizer):
    visualizer.parse_dependencies('SomePackage')
    dot_code = visualizer.generate_graphviz_code()
    assert 'digraph G {' in dot_code
    assert 'SomePackage' in dot_code
    assert 'dependency1' in dot_code
    assert 'dependency2' in dot_code
    assert '}' in dot_code

def test_visualize(visualizer, monkeypatch):
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a mock dot file and png file
        dot_file_path = os.path.join(temp_dir, 'graph.dot')
        png_file_path = os.path.join(temp_dir, 'graph.png')

        # Mock the open_image method to prevent actual image opening
        def mock_open_image(image_path):
            assert image_path == png_file_path

        monkeypatch.setattr(visualizer, 'open_image', mock_open_image)

        # Mock subprocess.run to prevent actual subprocess execution
        def mock_subprocess_run(args, **kwargs):
            if args[0] == 'dot':
                assert args[1:] == ['-Tpng', dot_file_path, '-o', png_file_path]
            elif args[0] == 'rm':
                assert args[1] in [dot_file_path, png_file_path]
            else:
                raise ValueError(f"Unexpected subprocess call: {args}")

        monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)

        visualizer.visualize()