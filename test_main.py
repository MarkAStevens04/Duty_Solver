import unittest
import main
import random

names = ['p1', 'p2', 'p3', 'p4', 'p5']
num_per_day = 2

def basic_run(availability, max_diff):
    # takes some availability and does a basic run!
    return main.main_run(num_per_day, availability, max_difference=max_diff)

class TestBasic(unittest.TestCase):
    def test_very_simple(self):
        availability = [[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]]

    def test_simple_one(self):
        availability = [[1, 1, 1, 1, 0],
                        [1, 1, 0, 1, 1],
                        [1, 1, 1, 0, 1]]

        self.assertEqual(6, basic_run(availability, 1))

    def test_simple_two(self):
        availability = [[1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0],]

        self.assertEqual(6, basic_run(availability, 1))

    def test_many_number(self):
        availability = [[1, 2, 3, 4, 5, 6],
                        [1, 2, 3, 4, 5, 6],
                        [1, 2, 3, 0, 0, 0],
                        [1, 2, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0]]

        self.assertEqual(39, basic_run(availability, 10))


class TestDuration(unittest.TestCase):
    # These tests check if the algo can run in the correct time!
    def test_simple(self):
        availability = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(1, basic_run(availability, 0.5))

    def test_many_soln(self):
        availability = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]]

        main.print_solution = False
        self.assertEqual(90000, basic_run(availability, 10))

    def test_kinda_hard_soln(self):
        availability =[[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                       [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                       [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                       [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(1, basic_run(availability, 0.5))

    def test_kinda_hard(self):
        availability =[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                       [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                       [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                       [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(1, basic_run(availability, 0.5))
        print('passed!!!!')



class TestRandom(unittest.TestCase):
    def test_random_ones_only(self):
        # only fills availability with ones
        print_start = True
        availability = []
        days = 12
        ppl = 8
        frequency = 0.8
        for p in range(ppl):
            row = []
            for day in range(days):
                if random.random() > frequency:
                    row.append(0)
                else:
                    row.append(1)
            availability.append(row)

        if print_start:
            for row in availability:
                print(row)

        run_result = main.main_run(num_per_day, availability, end=True)

        self.assertIsNotNone(run_result)

class TestEdge(unittest.TestCase):
    def test_no_availability(self):
        availability = [[1, 2, 3, 4, 5, 6],
                        [1, 2, 3, 4, 5, 0],
                        [1, 2, 3, 0, 0, 0],
                        [1, 2, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0]]
        found = main.main_run(num_per_day, availability)
        self.assertEqual(False, found)  # add assertion here



if __name__ == '__main__':
    unittest.main()
