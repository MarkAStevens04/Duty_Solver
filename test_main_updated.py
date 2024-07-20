import unittest
import main
import random

names = ['p1', 'p2', 'p3', 'p4', 'p5']
num_per_day = 2

# helper function
def basic_run(availability, max_difference):
    # takes some availability and does a basic run!
    return main.main_run(num_per_day, availability, max_difference=max_difference)


class TestEntropy(unittest.TestCase):
    # Tests the entropy function
    def test_simple(self):
        availability = [[1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1]]
        self.assertNotEqual(False, basic_run(availability, 0.5))

    def test_simple_impossible(self):
        # Impossible because cannot work 2 consecutive days
        availability = [[1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1]]
        self.assertEqual(False, basic_run(availability, 5))





class TestLonger(unittest.TestCase):
    # These tests check if the algo can run performantly!
    def test_simple(self):
        availability = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
                        [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
                        [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
                        [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
                        [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                        [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1]]
        main.print_solution = True
        self.assertNotEqual(False, basic_run(availability, 1))


    def test_many_soln(self):
        # Tricky because first pair MUST go first
        availability = [[1, 1, 1],
                        [1, 1, 1],
                        [0, 1, 1],
                        [0, 1, 1]]
        main.print_solution = True
        result = basic_run(availability, 2)
        print(result)
        self.assertNotEqual(False, result)


    def test_kinda_hard_soln(self):
        availability = [[1, 1, 1],
                        [1, 1, 1],
                        [0, 1, 1],
                        [0, 1, 1]]
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

        main.optimize_entropy = False
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
