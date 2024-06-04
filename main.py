
names = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8']
num_booked = [0, 0, 0, 0, 0, 0, 0, 0]
max_diff = 1
num_found = [0]


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

availability =[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# availability = [[1, 1, 1],
#                 [1, 1, 1],
#                 [1, 1, 1]]

def recursive_solver(availability, index, names, final_availability):
    # for now, ignore number of days. We'll come back to that.
    #
    # base case:
    #   - found 2 names
    # recurse:

    avg = (len(availability[0]) * 2) / len(names)
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
        # return False


    for p1_i in range(len(names)):
        for p2_i in range(p1_i + 1, len(names)):
            # quickly terminates bad runs!
            if num_booked[p1_i] > avg + max_diff or num_booked[p2_i] > avg + max_diff:
                return False


            # iterates through every possible combination of names
            p1_availability = availability[p1_i][index]
            p2_availability = availability[p2_i][index]
            if p1_availability == 1 and p2_availability == 1:
                # found a successful pair!
                final_availability[p1_i][index] = 1
                final_availability[p2_i][index] = 1
                num_booked[p1_i] = num_booked[p1_i] + 1
                num_booked[p2_i] = num_booked[p2_i] + 1
                # print(final_availability)
                found = recursive_solver(availability, index+1, names, final_availability)
                # print(f"passing...")
                if found:
                    return True
                else:
                    # backtrack...
                    final_availability[p1_i][index] = 0
                    final_availability[p2_i][index] = 0
                    num_booked[p1_i] = num_booked[p1_i] - 1
                    num_booked[p2_i] = num_booked[p2_i] - 1

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

    print(f'final availability:')
    final_availability = find_final_availability(availability)
    for row in final_availability:
        print(row)
    print()
    print(f"---")

    if not recursive_solver(availability, 0, names, final_availability):
        print("----- no valid combo found! -----")


    for row in final_availability:
        print(row)
    # print(final_availability)
    # print(num_found[0])
