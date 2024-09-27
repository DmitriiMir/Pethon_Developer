import unittest


class Runner:
    def __init__(self, name):
        self.name = name
        self.distance = 0

    def run(self):
        self.distance += 10

    def walk(self):
        self.distance += 5

    def __str__(self):
        return self.name


class RunnerTest(unittest.TestCase):

    # test_walk
    def test_walk(self):
        runner = Runner("TestRunner")
        for _ in range(10):
            runner.walk()
        # Проверка дистанции
        self.assertEqual(runner.distance, 50)

    # test_run
    def test_run(self):
        runner = Runner("TestRunner")
        for _ in range(10):
            runner.run()
        # Проверяем, что distance равно 100 после 10 вызовов run
        self.assertEqual(runner.distance, 100)

    # test_challenge
    def test_challenge(self):
        runner1 = Runner("Runner1")
        runner2 = Runner("Runner2")

        for _ in range(10):
            runner1.run()
            runner2.walk()

        # Проверяем, что дистанции отличаются
        self.assertNotEqual(runner1.distance, runner2.distance)


if __name__ == '__main__':
    unittest.main()
