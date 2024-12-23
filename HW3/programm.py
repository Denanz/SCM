import argparse
import re
import toml
from math import sqrt

def parse_toml(file_path):
    """Парсинг TOML-файла, игнорируя комментарии."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            filtered_lines = [line.split(";")[0].strip() for line in lines if not line.strip().startswith(";")]
            content = "\n".join(filtered_lines)
            return toml.loads(content)
    except toml.TomlDecodeError as e:
        raise SyntaxError(f"Ошибка синтаксиса TOML: {e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден.")

def evaluate_expression(expression, constants):
    if not expression.startswith("#(") or not expression.endswith(")"):
        raise ValueError(f"Неправильное выражение: {expression}")
    expression = expression[2:-1]

    try:
        for name, value in constants.items():
            expression = expression.replace(name, str(value))
        return eval(expression, {"sqrt": sqrt})
    except Exception as e:
        raise ValueError(f"Ошибка в выражении: {expression}. {e}")

def translate(data, constants=None):
    constants = constants or {}

    def format_value(value):
        if isinstance(value, dict):
            items = ",\n".join(f"{k} : {format_value(v)}" for k, v in value.items())
            return f"$[\n{items}\n]"
        elif isinstance(value, list):
            items = ". ".join(format_value(v) for v in value)
            return f"{{ {items}. }}"
        elif isinstance(value, str):
            if value.startswith("#("):  # Обработка выражений
                return evaluate_expression(value, constants)
            return f'"{value}"'
        else:
            return str(value)

    result = []
    for key, value in data.items():
        # Проверка имени
        if not re.match(r"^[a-zA-Z][_a-zA-Z0-9]*$", key):
            raise ValueError(f"Недопустимое имя: {key}")
        # Добавляем в константы, если это объявление
        if isinstance(value, str) and value.startswith("#("):
            constants[key] = evaluate_expression(value, constants)
        result.append(f"{key} := {format_value(value)}")
    return "\n".join(result)

def main():
    parser = argparse.ArgumentParser(description="TOML Translator CLI")
    parser.add_argument("--input", required=True, help="Путь к входному TOML-файлу")
    parser.add_argument("--output", required=True, help="Путь к выходному конфигурационному файлу")
    args = parser.parse_args()

    try:
        data = parse_toml(args.input)
        result = translate(data)

        with open(args.output, "w") as output_file:
            output_file.write(result)
        print(f"Конфигурация сохранена в {args.output}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
