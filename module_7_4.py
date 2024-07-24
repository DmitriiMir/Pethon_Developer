# Пример входных данных:
team1_num = 6
team2_num = 6
score_1 = 40
score_2 = 42
team1_time = 1552.512
team2_time = 2153.31451
tasks_total = 82
time_avg = 45.2

if score_1 > score_2 or (score_1 == score_2 and team1_time > team2_time):
    challenge_result = 'Победа команды Мастера кода!'
elif score_1 < score_2 or (score_1 == score_2 and team1_time < team2_time):
    challenge_result = 'Победа команды Волшебники данных!'
else:
    challenge_result = 'Ничья!'

# Использование %
team1_num_str = "В команде Мастера кода участников: %d !" % team1_num
team_participants_str = "Итого сегодня в командах участников: %d и %d !" % (team1_num, team2_num)

# Использование format()
score_2_str = "Команда Волшебники данных решила задач: {} !".format(score_2)
team2_time_str = "Волшебники данных решили задачи за {:.1f} с !".format(team2_time)

# Использование f-строк
score_str = f"Команды решили {score_1} и {score_2} задач."
result_str = f"Результат битвы: {challenge_result}"
tasks_time_avg_str = f"Сегодня было решено {tasks_total} задач, в среднем по {time_avg:.1f} секунды на задачу!"

# Вывод результата:
print(team1_num_str)
print(team_participants_str)
print(score_2_str)
print(team2_time_str)
print(score_str)
print(result_str)
print(tasks_time_avg_str)
