import unittest
import main
names = ['p1', 'p2', 'p3', 'p4', 'p5']
num_per_day = 2

def basic_run(availability):
    # takes some availability and does a basic run!
    return main.main_run(names, num_per_day, availability)

class TestBasic(unittest.TestCase):
    def test_simple(self):
        availability = [[1, 2, 3, 4, 5, 6],
                        [1, 2, 3, 4, 5, 6],
                        [1, 2, 3, 0, 0, 0],
                        [1, 2, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0]]

        self.assertEqual(39, basic_run(availability))


    def test_simple_two(self):
        availability = [[1, 1, 1, 1, 0],
                        [1, 1, 0, 1, 1],
                        [1, 1, 1, 0, 1]]

        self.assertEqual(9, basic_run(availability))

    def test_simple_two(self):
        availability = [[1, 1, 1, 1, 0],
                        [1, 1, 0, 1, 1],
                        [1, 1, 1, 0, 1]]

        self.assertEqual(9, basic_run(availability))


class TestDuration(unittest.TestCase):
    # These tests check if the algo can run in the correct time!
    def test_simple(self):
        availability = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(90000, basic_run(availability))



class TestEdge(unittest.TestCase):
    def test_no_availability(self):
        availability = [[1, 2, 3, 4, 5, 6],
                        [1, 2, 3, 4, 5, 0],
                        [1, 2, 3, 0, 0, 0],
                        [1, 2, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0]]
        found = main.main_run(names, num_per_day, availability)
        self.assertEqual(False, found)  # add assertion here



if __name__ == '__main__':
    unittest.main()
