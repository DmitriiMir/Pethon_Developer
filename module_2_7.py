def print_params(a=1, b='строка', c=True):
    print(a, b, c)

# Вызов функции с разным количеством аргументов
print_params()
print_params(10)
print_params(10, 'новая строка')
print_params(b=25)
print_params(c=[1, 2, 3])

# Создаем список с тремя элементами разных типов
values_list = [21, 'Дмитрий', False]

# Создаем словарь
values_dict = {
    "a": 100,
    "b": "для_примера",
    "c": [1, 2, 3]
}

# Распаковка параметров
print_params(*values_list)
print_params(**values_dict)

# Создаем список с двумя элементами разных типов
values_list_2 = [54.32, 'строка']

# Проверяем работу функции
print_params(*values_list_2, 42)
