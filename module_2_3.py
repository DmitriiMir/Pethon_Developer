my_list = [42, 69, 322, 13, 0, 99, -5, 9, 8, 7, -6, 5]

index = 0  # Начальный индекс

positive_list = []  # Создаем список для положительных чисел

while index < len(my_list):  # Цикл while
    if my_list[index] < 0:  # Если число отрицательное, прерываем цикл
        break
    if my_list[index] > 0:  # Если число положительное, добавляем его в положительный список
        positive_list.append(my_list[index])
    index += 1

print(positive_list)  # Вывод списка положительных чисел
