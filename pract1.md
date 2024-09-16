# Практическое задание №1. 

Знакомство с Linux консолью

## Задача 1

```
cut -d: -f1 /etc/passwd | sort
```

![{192BE454-1447-4196-9C1F-C4EE0BA14D8A}](https://github.com/user-attachments/assets/f93356a5-37cc-464d-afb7-20474bb1263e)

### Объяснение

cut -d: -f1 /etc/passwd — команда cut извлекает первый столбец из файла /etc/passwd, используя двоеточие : как разделитель полей и выводит его.

sort — сортирует строки в алфавитном порядке.



## Задача 2

```
awk '{print $2, $1}' /etc/protocols | sort -k1,1nr | head -n 5
```
![{D60AF2B9-70F1-426B-8B43-A1925B360B05}](https://github.com/user-attachments/assets/296de080-b3b5-49a6-ad8e-9cff2bb4bcda)

### Объяснение

awk '{print $2, $1}' /etc/protocols: Эта команда извлекает второй столбец и первый столбец из файла /etc/protocols и выводит их в формате номер имя.

sort -k1,1nr: Сортирует вывод по первому столбцу численно и в обратном порядке.

head -n 5: Выводит только первые пять строк.



## Задача 3

```
if [ -z "$1" ]; then
    echo "Usage: $0 \"Your message here\""
    exit 1
fi

message="$1"

length=${#message}

border="+$(printf -- '-%.0s' $(seq 1 $((length + 2))))+"

echo "$border"
echo "| $message |"
echo "$border"
```

![{DB01CF3E-DAD4-44E4-AE95-9688760038AC}](https://github.com/user-attachments/assets/550916dc-c9d5-4bf5-b50e-fad2fe8a7711)

### Объяснение

if [ -z "$1"]; then... - если при вызове скрипта поле ввода пустое то мы выводим условия выполнения скрипта 

message="$1" - присваивам аргументу название message

length=${#message} - вычисляем длину строки

border="+$(printf -- '-%.0s' $(seq 1 $((length + 2))))+" - Создание рамок

printF -- '-%.0s' - печать символа '-'

$(seq 1 $((length + 2))) - вывод символа '-' от 1 до length + 2



## Задача 4 

```
if [ -z "$1" ]; then
    echo "Usage: $0 <source_file>"
    exit 1
fi

grep -o -E '\b[_a-zA-Z][_a-zA-Z0-9]*\b' "$1" | sort | uniq
```
### Вывод программы
![{4B3F628A-BB82-445C-8444-2293B9C3EBC5}](https://github.com/user-attachments/assets/1876da5d-6c79-4633-b385-edcb7d0873b0)

### Код из файла hello.c

```
#include <stdio.h>

void hello_world() {
    printf("Hello, world!\n");
}

int main() {
    hello_world();
    return 0;
}

```

### Объяснение 

grep -o -E '\b[_a-zA-Z][_a-zA-Z0-9]*\b' "$1" | sort | uniq - скрипт отбора и сортировки

\b[_a-zA-Z][_a-zA-Z0-9]*\b - первый символ может быть нижним подчёркиванием или любой буквой а все остальные символы могут быть как нижним подчёркиванием так и числом или буквой

sort - сортировка 

uniq - оставляет только уникальные значения

## Задача 5 

```
chmod +x $1
sudo cp $1 /usr/local/bin
```

![{78697D9E-24C4-4493-92D2-78600DE8A534}](https://github.com/user-attachments/assets/663f45db-b5cb-4aef-bf93-783bf18a396e)

## Задача 6

```
#!/bin/bash

# Проверяем все файлы с расширениями .c, .js и .py
for file in *.{c,js,py}; do
  # Проверяем, существует ли файл с таким расширением (может не быть файлов с таким расширением в папке)
  if [ -f "$file" ]; then
    # Читаем первую строку файла
    first_line=$(head -n 1 "$file")

    # Проверяем наличие комментария
    if [[ "$file" == *.c || "$file" == *.js ]]; then
      # Для .c и .js проверяем // или /*
      if [[ "$first_line" =~ ^\s*// || "$first_line" =~ ^\s*/\* ]]; then
        echo "$file: содержит комментарий в первой строке"
      else
        echo "$file: не содержит комментарий в первой строке"
      fi
    elif [[ "$file" == *.py ]]; then
      # Для .py проверяем #
      if [[ "$first_line" =~ ^\s*# ]]; then
        echo "$file: содержит комментарий в первой строке"
      else
        echo "$file: не содержит комментарий в первой строке"
      fi
    fi
  fi
done
```
![image](https://github.com/user-attachments/assets/5ec2e663-adfe-4df6-99c5-57b51160df14)

## Задача 7

```
#!/bin/bash
# Проверяем, что путь передан как аргумент
if [ -z "$1" ]; then
  echo "Ошибка: не указан путь."
  echo "Использование: ./find_duplicates.sh <путь>"
  exit 1
fi

# Заданная директория
directory=$1

# Ассоциативный массив для хранения файлов по их хешам
declare -A file_hashes

# Поиск всех файлов в директории и подкаталогах
find "$directory" -type f | while read -r file; do
  # Вычисляем хеш файла
  hash=$(sha256sum "$file" | awk '{print $1}')

  # Проверяем, есть ли уже файл с таким хешем
  if [[ -n "${file_hashes[$hash]}" ]]; then
    echo "Найден дубликат:"
    echo "Оригинал: ${file_hashes[$hash]}"
    echo "Дубликат: $file"
  else
    # Если хеша нет, добавляем файл в массив
    file_hashes[$hash]="$file"
  fi
done
```
![image](https://github.com/user-attachments/assets/5d0b4423-b1b9-4714-8d31-a49eb3c3d1fe)

## Задача 8
```
#!/bin/bash

# Проверка количества аргументов
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <directory> <extension> <archive_name>"
    exit 1
fi

# Получаем аргументы
directory=$1
extension=$2
archive_name=$3

# Находим все файлы с указанным расширением и архивируем их
find "$directory" -type f -name "*$extension" | tar -cvf "$archive_name" -T -

echo "Файлы с расширением $extension успешно заархивированы в $archive_name."
```
![image](https://github.com/user-attachments/assets/18c6acac-464f-42dd-b4c7-f39177ee73c7)


## Задача 9
```
#!/bin/bash

# Проверка количества аргументов
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_file> <output_file>"
    exit 1
fi

# Входной и выходной файлы
input_file="$1"
output_file="$2"

# Проверка, существует ли входной файл
if [ ! -f "$input_file" ]; then
    echo "Ошибка: файл $input_file не найден."
    exit 1
fi

# Заменяем 4 пробела на символ табуляции и записываем результат в новый файл
sed 's/    /\t/g' "$input_file" > "$output_file"

# Выводим сообщение о завершении
echo "Файл $input_file был обработан, результат записан в $output_file."
```

## Задача 10
```

