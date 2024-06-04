import random

# Sort days based on estimated "difficulty" (entropy?).
# So like, easy days have many options, and they should be solved last.
# hard days have few options, and should be solved first.
#
# The difficulty could be based on the number of people available that day.
# Or the difficulty could be a weighted sum of the
# people available that day, with the weights corresponding
# to the "flexibility" of any person. Flexible people give low weight, while
# inflexible people give high weight. high value means more difficulty. Hmm re-think
# the higher or lower part, but this is a good idea! Balance the number of people
# with the value of each people. A day with 3 people who are very flexible should be
# considered after a day with 5 people who are very inflexible.


names = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8']
max_diff = 1
num_solutions_found = [0]
num_per_day = 2


# format availability [[one persons schedule entire time],
#                       [another persons schedule entire time],
#                        [a third persons schedule entire time]]
# availability = [[1, 1, 1, 1, 0],
#                 [1, 1, 0, 1, 1],
#                 [1, 1, 1, 0, 1]]

availability = [[1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 0],]

availability = [[1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 0]]

# this one is hard!
availability = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]]

# availability = [[1, 1, 2, 1, 1, 1],
#                 [1, 1, 2, 1, 1, 1],
#                 [1, 1, 2, 0, 0, 0],]


# random availability
# availability = []
# days = 12
# ppl = 8
# frequency = 0.8
# for p in range(ppl):
#     row = []
#     for day in range(days):
#         if random.random() > frequency:
#             row.append(0)
#         else:
#             row.append(1)
#     availability.append(row)


# this is the solution!
# availability =[[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#                [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
#                [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
#                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# this one is extra hard!
# availability =[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
#                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
#                [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
#                [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
#                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# availability = [[1, 1, 1],
#                 [1, 1, 1],
#                 [1, 1, 1]]

def recursive_solver(availability, index, names, final_availability):
    # update avg to reflect number of 2 point days and 1 point days
    # avg = (len(availability[0]) * 2) / len(names)
    # avg = (7 * 2) / len(names)
    # print(avg)
    # must be within +- avg for every name when the algo finishes!

    if index >= len(availability[0]):
        # make sure every person is within range!
        for person_i in range(len(num_booked)):
            if num_booked[person_i] < avg - max_diff or num_booked[person_i] > avg + max_diff:
                # print(f"exploiting person {person_i} with {num_booked[person_i]}")
                # for row in final_availability:
                #     print(row)
                return False
        # found a valid solution. Printing!
        for r in range(len(final_availability)):
            print(f"{final_availability[r]}:{num_booked[r]}")
        print(f"---")
        # return True
        # num_found[0] = num_found[0] + 1
        # print(num_found[0])
        return False


    for p1_i in range(len(availability)):
        for p2_i in range(p1_i + 1, len(availability)):
            # quickly terminates bad runs!
            # bad run if we know this current iteration is already off.
            # ----- OPTIMIZATION -------
            # put this in the recursive call!
            # Never call a run if it's doomed from the start!
            if num_booked[p1_i] > avg + max_diff or num_booked[p2_i] > avg + max_diff:
                return False
            # print(index)
            # iterates through every possible combination of names
            p1_availability = availability[p1_i][index]
            p2_availability = availability[p2_i][index]
            if p1_availability != 0 and p2_availability != 0:
                # found a successful pair!
                # Update final availability to reflect number of points
                final_availability[p1_i][index] = availability[p1_i][index]
                final_availability[p2_i][index] = availability[p2_i][index]

                # add number of points to the score
                num_booked[p1_i] = num_booked[p1_i] + availability[p1_i][index]
                num_booked[p2_i] = num_booked[p2_i] + availability[p2_i][index]
                # print(final_availability)
                found = recursive_solver(availability, index+1, names, final_availability)
                # print(f"passing...")
                if found:
                    return True
                else:
                    # backtrack...
                    final_availability[p1_i][index] = 0
                    final_availability[p2_i][index] = 0
                    num_booked[p1_i] = num_booked[p1_i] - availability[p1_i][index]
                    num_booked[p2_i] = num_booked[p2_i] - availability[p2_i][index]

    return False


def find_final_availability(availability):
    num_ppl = len(availability)
    num_days = len(availability[0])
    final = []
    for person in range(num_ppl):
        row = []
        for day in range(num_days):
            row.append(0)
        final.append(row)
    return final


def optimize_order(availability):
    # orders people based on their availability
    #
    # returns the new availability, alongside a dict_mapping.
    # the dict mapping shows for each index produced, what original index it came from.
    # for example {0:6} means that the first row of the new array came from the 6th row of the original array
    num_days_free = dict()
    dict_mapping = dict()
    for i in range(len(availability)):
        num_days_free[i] = 0
        dict_mapping[i] = 0
    num_f = [0] * len(availability)
    for row_i in range(len(availability)):
        for day in availability[row_i]:
            if day == 1:
                num_f[row_i] = num_f[row_i] + 1
                num_days_free[row_i] = num_days_free[row_i] + 1

    tuples = []
    for input in range(len(num_f)):
        tuples.append((num_f[input], input))
    tuples.sort()
    num_f.sort()
    # print(tuples)
    # print(dict_mapping)

    for found_i in range(len(tuples)):
        dict_mapping[tuples[found_i][1]] = found_i

    # print(dict_mapping)

    sorted_array = []
    for i in range(len(tuples)):
        sorted_array.append(availability[tuples[i][1]])

    # for row in sorted_array:
    #     print(row)
    return sorted_array, dict_mapping


def calc_avg(availability):
    # Calculates the final average number of points per person!
    # first, calculate the total number of points a day
    total_points = 0
    for i in range(len(availability[0])):
        # i is the index for each day
        # x is the index for each person
        x = 0
        while availability[x][i] == 0:
            x += 1
        total_points += availability[x][i]

    # avg # of points per person is the total number of points, divided by the number of ppl.
    # multipy total_points by num_per_day b/c points required increases based on number of
    # ppl on call each day.
    avg = (num_per_day * total_points) / len(availability)
    return avg






if __name__ == "__main__":
    # final_availability = [[0, 0, 0, 0, 0],
    #                       [0, 0, 0, 0, 0],
    #                       [0, 0, 0, 0, 0]]

    # final_availability = [[0, 0, 0, 0, 0, 0],
    #                       [0, 0, 0, 0, 0, 0],
    #                       [0, 0, 0, 0, 0, 0]]

    # final_availability = [[0, 0, 0],
    #                       [0, 0, 0],
    #                       [0, 0, 0]]

    # print(f'final availability:')
    final_availability = find_final_availability(availability)
    # print()
    # print(f"---")
    print(f'---')
    availability, dict_mapping = optimize_order(availability)
    for row in availability:
        print(row)
    print(f'---')

    avg = calc_avg(availability)
    num_booked = [0] * len(availability)
    print(f'avg points: {avg}')
    if not recursive_solver(availability, 0, names, final_availability):
        print("----- no valid combo found! -----")


    for row in final_availability:
        print(row)
    # print(final_availability)
    # print(num_found[0])
    print(f"---")
    availability = [[1, 1, 2, 0, 0, 0],
                    [0, 0, 2, 1, 1, 1],
                    [1, 1, 0, 1, 1, 1]]



