# Практическое задание №1. 

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
