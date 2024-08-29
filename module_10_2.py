import threading
from time import sleep

enemies = 100


class Knight(threading.Thread):
    def __init__(self, name, power):
        super().__init__()
        self.name = name
        self.power = power
        self.days = 0

    def run(self):
        global enemies
        print(f"{self.name}, на нас напали!")

        while enemies > 0:
            sleep(1)
            self.days += 1

            enemies = max(0, enemies - self.power)

            print(f"{self.name} сражается {self.days} день(дня)..., осталось {enemies} воинов.")

        print(f"{self.name} одержал победу спустя {self.days} дней(дня)!")


first_knight = Knight('Sir Lancelot', 10)
second_knight = Knight("Sir Galahad", 20)

first_knight.start()
second_knight.start()

first_knight.join()
second_knight.join()

print("Все битвы закончились!")
