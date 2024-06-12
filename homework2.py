homework_count = 12
number_of_hours = 1.5
name_of_course = 'Python'
time_for_one_task = number_of_hours / homework_count
print('Курс: '+ name_of_course, 'всего задач: ' + str(homework_count), 'затрачено часов: ' +
      str(number_of_hours),'среднее время выполнения ' + str(time_for_one_task) + ' часа.', sep=', ')
