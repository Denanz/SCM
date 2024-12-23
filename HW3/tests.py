import pytest
import os
from programm import parse_toml, translate, evaluate_expression

def test_parse_toml(tmp_path):
    toml_content = """
    name = "Test"
    version = 1.0
    [section]
    key = "value"
    ; This is a comment
    """
    toml_file = tmp_path / "test.toml"
    toml_file.write_text(toml_content)

    parsed = parse_toml(toml_file)
    assert parsed["name"] == "Test"
    assert parsed["version"] == 1.0
    assert parsed["section"]["key"] == "value"

def test_translate_with_constants():
    data = {
        "name": "Test",
        "constant": "#(2 + 3)",
        "nested": {
            "key": "value",
        },
        "list": ["item1", "item2"],
    }

    result = translate(data)
    assert "name := \"Test\"" in result
    assert "constant := 5" in result
    assert "nested := $[\nkey : \"value\"\n]" in result
    assert "list := { \"item1\". \"item2\". }" in result

def test_evaluate_expression():
    constants = {"x": 2, "y": 3}
    assert evaluate_expression("#(x + y)", constants) == 5
    assert evaluate_expression("#(sqrt(16))", constants) == 4
    with pytest.raises(ValueError):
        evaluate_expression("#(invalid + 2)", constants)

def test_invalid_name():
    data = {
        "1invalid": "value",  # Invalid key name
    }
    with pytest.raises(ValueError, match="Недопустимое имя"):
        translate(data)

def test_save_result(tmp_path):
    data = {
        "name": "Test",
        "version": 1.0,
    }
    result = translate(data)

    output_file = tmp_path / "output.txt"
    with open(output_file, "w") as file:
        file.write(result)

    assert output_file.read_text() == result

if __name__ == "__main__":
    pytest.main()
