import threading
import time


class Knight(threading.Thread):
    def __init__(self, name, power):
        super().__init__()
        self.name = name
        self.power = power
        self.days_fighting = 0
        self.enemies = 100

    def run(self):
        print(f"{self.name}, на нас напали!")

        while self.enemies > 0:
            time.sleep(1)
            self.days_fighting += 1

            self.enemies -= self.power
            if self.enemies < 0:
                self.enemies = 0

            print(f"{self.name} сражается {self.days_fighting} день(дня)..., осталось {self.enemies} воинов.")

        print(f"{self.name} одержал победу спустя {self.days_fighting} дней(дня)!")


first_knight = Knight('Sir Lancelot', 10)
second_knight = Knight("Sir Galahad", 20)

first_knight.start()
second_knight.start()

first_knight.join()
second_knight.join()

print("Все битвы закончились!")