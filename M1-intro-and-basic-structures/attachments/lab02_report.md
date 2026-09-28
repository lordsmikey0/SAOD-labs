## МИНИСТЕРСТВО ЦИФРОВОГО РАЗВИТИЯ И МАССОВЫХ КОММУНИКАЦИЙ РОССИЙСКОЙ ФЕДЕРАЦИИ
## Ордена трудового Красного Знамени федеральное государственное бюджетное образовательное учреждение "Московский технический университет связи и информатики"

### Отчет по лабораторной работе №2: "Реализация рекурсивных функций и динамического массива, стека и дека"
### **Выполнил**: Студент группы БВТ-2502, Провкин Алексей Сергеевич
___

**Цель**: Освоить рекурсию как метод построения алгоритмов и реализовать базовые линейные структуры данных, подтвердив их асимптотические свойства (включая амортизированную сложность) экспериментально.

___
## Информация:
**Версия Python**: Python 3.10.11

**Процессор**: Intel(R) Core(TM) i5-10500H-CPU (базовая скорость: 2.5 GHz, максимальная скорость: 4.5 GHz)
___
### Ход выполнения работы:
1. Были сгенерированы данные по варианту 10
    ```bash
   (venv) PS C:\Users\Alexey\PycharmProjects\data-structures-and-algorithms> python scripts/generate_data.py --variant 10 --only ops
    Вариант 10 (seed=40), каталог C:\Users\Alexey\PycharmProjects\data-structures-and-algorithms\data\generated; создано файлов: 3
    C:\Users\Alexey\PycharmProjects\data-structures-and-algorithms\data\generated\ops_stack.txt
     C:\Users\Alexey\PycharmProjects\data-structures-and-algorithms\data\generated\ops_deque.txt
    C:\Users\Alexey\PycharmProjects\data-structures-and-algorithms\data\generated\ops_append_sizes.txt
    Паспорт данных: C:\Users\Alexey\PycharmProjects\data-structures-and-algorithms\data\generated\manifest.json

2. 