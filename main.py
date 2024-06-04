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
#
# Include consideration of total number of days worked?
# Like, having someone work all 2s and someone work zero 2s isn't fair.
# Try to make equal the number of days someone works.
# Well, thats what's trying to be addressed by the point system!
#
# Add some automated testing?


names = ['p1', 'p2', 'p3', 'p4', 'p5']
max_diff = 10
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
# availability = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
#                 [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
#                 [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
#                 [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]]

availability = [[1, 2, 3, 4, 5, 6],
                [1, 2, 3, 4, 5, 6],
                [1, 2, 3, 0, 0, 0],
                [1, 2, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0]]


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
        return found_solution()


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


def found_solution():
    final_availability = de_order_ppl(finished_availability, person_mapping)
    final_availability = de_order_days(final_availability, day_mapping)
    # Handles what should happen when the final solution is found!
    for r in range(len(final_availability)):
        print(f"{final_availability[r]}: {num_booked[r]}")
    print(f"---")


    # return False means keep searching
    # return True means stop after finding this solution
    return False


def create_finished_availability(availability):
    # creates the final_availability base data structure
    # Essentially, just a copy of availability, but filled with 0s.
    num_ppl = len(availability)
    num_days = len(availability[0])
    final = []
    for person in range(num_ppl):
        row = []
        for day in range(num_days):
            row.append(0)
        final.append(row)
    return final


def order_ppl(availability):
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

def de_order_ppl(finished_availability, availability_dict):
    # un-orders the availability of ppl
    # creates a copy of the array, does not modify original

    final_availability = []
    for r in range(len(finished_availability)):
        i = availability_dict[r]
        final_availability.append(finished_availability[i])
    return final_availability


def calc_difficulty(availability, index):
    # Calculates the difficulty of a given day!
    # small difficulty = very difficult
    difficulty = 0
    for p in range(len(availability)):
        if availability[p][index] != 0:
            difficulty += 1
    return difficulty

def order_days(availability):
    # orders days based on their "difficulty".
    # difficult days come first, easy days come last.
    # Difficult days have very little availability
    # Easy have have a lot of availability.
    # Solving easy days first allows us to do the hard part as few times as possible.
    # Otherwise, our algorithm would explore a lot of solutions, all which fail
    # for the same reason.

    diff_tuples = []
    orig_mapping = {}
    # orig_mapping goes {new_index: previous_index}
    # think "the row at index "key" came from the row at index "value"
    # dict_mapping goes {new_index: previous_index}

    # d is day index
    for d in range(len(availability[0])):
        # small difficulty = very difficult
        difficulty = calc_difficulty(availability, d)
        diff_tuples.append((difficulty, d))

    diff_tuples.sort()
    for t in range(len(diff_tuples)):
        orig_mapping[t] = diff_tuples[t][1]

    # reconstruct the availability
    new_availability = []
    for p in range(len(availability)):
        new_availability.append([])

    for d in range(len(availability[0])):
        for p in range(len(availability)):
            orig_index = orig_mapping[d]
            new_availability[p].append(availability[p][orig_index])

    return new_availability, orig_mapping

def de_order_days(finished_availability, day_mapping):
    # takes the day_mapping and returns the days to their original order
    final_availability = []
    for p in range(len(finished_availability)):
        final_availability.append([0] * len(finished_availability[0]))

    for d in range(len(finished_availability[0])):
        orig_index = day_mapping[d]
        for p in range(len(finished_availability)):
            final_availability[p][orig_index] = finished_availability[p][d]

    return final_availability





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
    finished_availability = create_finished_availability(availability)
    # print()
    # print(f"---")
    print(f'---')
    availability, person_mapping = order_ppl(availability)
    availability, day_mapping = order_days(availability)
    # availability, day_mapping = order_days(availability)
    for row in availability:
        print(row)
    print(f'---')

    avg = calc_avg(availability)
    num_booked = [0] * len(availability)
    print(f'avg points: {avg}')
    if not recursive_solver(availability, 0, names, finished_availability):
        print("----- no valid combo found! -----")


    for row in finished_availability:
        print(row)

    final_availability = de_order_ppl(availability, person_mapping)
    print(f'---')
    for r in range(len(final_availability)):
        print(final_availability[r])

    print(f'*********')
    
    for row in availability:
        print(row)
    print(f'-*-*-*-*-*-')
    final_availability = de_order_days(availability, day_mapping)
    for row in final_availability:
        print(row)




