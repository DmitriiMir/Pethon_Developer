grades = [[5, 3, 3, 5, 4], [2, 2, 2, 3], [4, 5, 5, 2], [4, 4, 3], [5, 5, 5, 4, 5]]
students = {'Johnny', 'Bilbo', 'Steve', 'Khendrik', 'Aaron'}

sorted_students = sorted(students)                  # Сортировка студентов в алфавитном порядке

average_grades = {}                                 # Пустой словарь для хранения среднего бала для каждого студента

for i, student in enumerate(sorted_students):       # запускаем цикл, вычисляем средний бал и заполняем словарь
    average_grade = sum(grades[i]) / len(grades[i])
    average_grades[student] = average_grade

print(average_grades)                               # Вывод результата
