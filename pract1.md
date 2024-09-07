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
awk '{print $3, $1}' /etc/protocols | sort -k1,1nr | head -n 5
```
![{D60AF2B9-70F1-426B-8B43-A1925B360B05}](https://github.com/user-attachments/assets/296de080-b3b5-49a6-ad8e-9cff2bb4bcda)

### Объяснение

awk '{print $3, $1}' /etc/protocols: Эта команда извлекает третий столбец и первый столбец из файла /etc/protocols и выводит их в формате номер имя.

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

\b[_a-zA-Z][_a-zA-Z0-9]*\b - первый символ может быть '_' или любой буквой а все остальные символы могут быть как '_' так и числом или буквой

sort - сортировка 

uniq - оставляет только уникальные значения
