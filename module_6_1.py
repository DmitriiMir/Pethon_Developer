class Animal:
    alive = True
    fed = False
    def __init__(self, name):
        self.name = name

class Plant:
    edible = False
    def __init__(self, name):
        self.name = name

class Mammal(Animal):
    def eat(self, food):
        if food.edible:
            print(f"{self.name} съел {food.name}")
            self.fed = True
        else:
            print(f"{self.name} не стал есть {food.name}")
            self.alive = False

class Predator(Animal):
    def eat(self, food):
        if food.edible:
            print(f"{self.name} съел {food.name}")
            self.fed = True
        else:
            print(f"{self.name} не стал есть {food.name}")
            self.alive = False

class Flower(Plant):
    def __init__(self, name):
        self.name = name

class Fruit(Plant):
    edible = True
    def __init__(self, name):
        self.name = name





# Создаем объекты классов
a1 = Predator('Волк с Уолл-Стрит')
a2 = Mammal('Хатико')
p1 = Flower('Цветик семицветик')
p2 = Fruit('Заводной апельсин')

# Выводим имена объектов
print(a1.name)
print(p1.name)

# Проверяем начальное состояние объектов
print(a1.alive)
print(a2.fed)

# Кормим животных
a1.eat(p1)
a2.eat(p2)

# Проверяем состояние объектов после кормления
print(a1.alive)
print(a2.fed)
