
names = ['p1', 'p2', 'p3']


# format availability [[one persons schedule entire time],
#                       [another persons schedule entire time],
#                        [a third persons schedule entire time]]
availability = [[1, 1, 1, 1, 0],
                [1, 1, 0, 1, 1],
                [1, 1, 1, 0, 1]]

def recursive_solver(availability, index, names, final_availability):
    # for now, ignore number of days. We'll come back to that.
    #
    # base case:
    #   - found 2 names
    # recurse:
    #   -
    if index >= len(availability[0]):
        return True

    for p1_i in range(len(names)):
        for p2_i in range(p1_i + 1, len(names)):
            # iterates through every possible combination of names
            p1_availability = availability[p1_i][index]
            p2_availability = availability[p2_i][index]
            if p1_availability == 1 and p2_availability == 1:
                # found a successful pair!
                final_availability[p1_i][index] = 1
                final_availability[p2_i][index] = 1
                print(final_availability)
                found = recursive_solver(availability, index+1, names, final_availability)
                if found:
                    return True
                else:
                    # backtrack...
                    final_availability[p1_i][index] = 0
                    final_availability[p2_i][index] = 0
                    return False
    return False




if __name__ == "__main__":
    final_availability = [[0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]]
    recursive_solver(availability, 0, names, final_availability)
    for row in final_availability:
        print(row)
    # print(final_availability)
