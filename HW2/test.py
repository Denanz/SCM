import pytest
from visualizer import DependencyVisualizer
import subprocess
import platform

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
    def mock_open_image(image_path):
        assert image_path == 'graph.png'

    monkeypatch.setattr(visualizer, 'open_image', mock_open_image)

    def mock_subprocess_run(args, **kwargs):
        if args[0] == 'dot':
            assert args[1:] == ['-Tpng', 'graph.dot', '-o', 'graph.png']
        elif args[0] == 'rm':
            assert args[1] in ['graph.dot', 'graph.png']
        else:
            raise ValueError(f"Unexpected subprocess call: {args}")

    monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)

    visualizer.visualize()