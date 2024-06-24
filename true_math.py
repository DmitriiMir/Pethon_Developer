'''Модуль для учебного проекта "Модули и проекты". Функция true_divide.'''
from math import inf
def true_divide(first, second):
    if second == 0:
        return inf
    return first / second
