import excel_processing as ep

# format availability [[one persons schedule entire time],
#                       [another persons schedule entire time],
#                        [a third persons schedule entire time]]

# - Ideas -
# The difficulty could be based on the number of people available that day.
# Or the difficulty could be a weighted sum of the
# people available that day, with the weights corresponding
# to the "flexibility" of any person. Flexible people give low weight, while
# inflexible people give high weight. high value means more difficulty. Hmm re-think
# the higher or lower part, but this is a good idea! Balance the number of people
# with the value of each people. A day with 3 people who are very flexible should be
# considered after a day with 5 people who are very inflexible.

# --- setup ---
num_per_day = 2
print_solution = True
optimize_entropy = True
export_solution = True

# --- hyper-parameters ---
# max_diff: maximum difference in number of points between som1 and the average
# max_entropy: higher val means greater tolerance of 2 consecutive days.
# entropy_spread: higher val means greater tolerance of going long periods without duty
max_diff = 1.5
max_entropy = 0
entropy_spread = 780
# entropy_spread = 10000

def check_valid(fin_av, p_index, t_left):
    # we assume the current finished_availability is valid,
    # and we try to find if it's not!
    #
    # p_index is index of person
    # r_index is index of current row

    valid = True
    if num_booked[p_index] > avg + max_diff:
        valid = False

    # if in the best case, we still cannot sum to get this current person
    # to a high enough score, we know its not valid.
    # if r_index is 35, will only check 36th column
    total_left = t_left
    if num_booked[p_index] < avg - max_diff - total_left:
        valid = False

    # if we're optimizing the entropy, do that!
    if optimize_entropy:
        # start by sorting back the days to their original order
        final_availability = de_order_ppl(fin_av, person_mapping)
        final_availability = de_order_days(final_availability, day_mapping)

        e = calc_entropy(final_availability)
        if e > max_entropy:
            valid = False

    return valid

def calc_spread_out(availability):
    # calc a score based on how spread out a final set of days are!
    # same as calc_entropy but with added functions
    total_cost = 0

    for p in range(len(availability)):
        run = 0
        person_cost = 0

        z_run_v = 0
        z_total_cost = 0
        for c in range(len(availability[0])):
            if availability[p][c] != 0:
                run += 1

                # print(f'run_length: {z_run_v}')
                z_total_cost += z_run_v ** 2
                z_run_v = 0
            else:
                z_run_v += 1

                if run > 1:
                    person_cost += run
                # if run != 0:
                #     person_cost += run
                if run >= 2:
                    total_cost += 100000000000000
                run = 0

        # print(f'person {p}, person_cost {person_cost}')
        person_cost = (person_cost ** 2) * 1000
        person_cost += z_total_cost
        # # print(f'person {p} new cost {person_cost}')
        # print(f'person {p}, zero r cost {z_total_cost}')

        total_cost += person_cost
    return total_cost

def calc_entropy(availability):
    # calc a score based on how bad a given solution is.
    # add 1 every time a given person has 2 consecutive shifts.
    # for each person, end by squaring the value
    total_cost = 0
    max_run = 2

    for p in range(len(availability)):
        # run is the length of the run
        # person cost is the sum of lengths of all runs for this person
        run = 0
        person_cost = 0

        # for every day in this block
        for c in range(len(availability[0])):
            # if the day is not 0, our run continues
            if availability[p][c] != 0:
                run += 1
            else:
                # the run has been broken b/c we reached a 0!
                #
                # if the run was greater than 1 (so an actual run), add the
                # length of the run to the person_cost.
                if run > 1:
                    person_cost += run
                if run >= max_run:
                    # if our run was greater than the max run, shoot up the entropy.
                    total_cost += 100000000000000
                # reset our run
                run = 0
        # square the length of all runs, and multiply by 1000
        person_cost = (person_cost ** 2) * 1000
        total_cost += person_cost

    return total_cost


def recursive_solver(availability, index, finished_availability, num_booked):
    # The main recursive call for our solver!
    #
    # number of points must be within the max_diff of the average
    # for the solution to be valid!

    # if we're past the final column...
    if index >= len(availability[0]):
        for person_i in range(len(num_booked)):
            if num_booked[person_i] < avg - max_diff or num_booked[person_i] > avg + max_diff:
                # exists a person who is outside the range!
                return False
        # Found a valid solution!
        # Every person is within range and we've recursed through every day!
        return found_solution(finished_availability)

    t_left = sum_points(availability, index)

    for p1_i in range(len(availability)):
        for p2_i in range(p1_i + 1, len(availability)):
            # iterates through every possible combination of ppl.
            # p1_i and p2_i are the indexes of the current pair.

            # quickly terminates bad runs!
            # bad run if we know this current iteration is already off.
            if not check_valid(finished_availability, p1_i, t_left) or not check_valid(finished_availability, p2_i, t_left):
                return False


            p1_availability = availability[p1_i][index]
            p2_availability = availability[p2_i][index]
            # check if both ppl are available on the given day.
            # if pX_availability = 0, we know not available.
            if p1_availability != 0 and p2_availability != 0:
                # found a successful pair!
                # Update final availability to reflect number of points
                finished_availability[p1_i][index] = p1_availability
                finished_availability[p2_i][index] = p2_availability

                # add number of points to the score
                num_booked[p1_i] = num_booked[p1_i] + p1_availability
                num_booked[p2_i] = num_booked[p2_i] + p2_availability

                # recursive call...
                # only do the recursive call if our guess doesn't put us in a bad state.
                if check_valid(finished_availability, p1_i, t_left) and check_valid(finished_availability, p2_i, t_left):
                    found = recursive_solver(availability, index+1, finished_availability, num_booked)

                    if found:
                        # recursive call found a solution, so we did too!
                        return True
                # only get here if no solution was found
                # or if we started off by finding an error!

                # backtrack...
                finished_availability[p1_i][index] = 0
                finished_availability[p2_i][index] = 0
                num_booked[p1_i] = num_booked[p1_i] - availability[p1_i][index]
                num_booked[p2_i] = num_booked[p2_i] - availability[p2_i][index]

    # Went through every combination of names and still didn't find a solution.
    # Therefore, outside combination had a fault.
    # print(avg)
    # found_solution(finished_availability)
    return False



def found_solution(finished_availability):
    final_availability = de_order_ppl(finished_availability, person_mapping)
    final_availability = de_order_days(final_availability, day_mapping)

    # next do our entropy check
    # this significantly slows down our algo...
    global optimize_entropy
    if optimize_entropy:
        e = calc_entropy(final_availability)
        e_s = calc_spread_out(final_availability)
        # print(f'entropy_spread: {e_s}')
        # print(f'entropy of soln: {e}')
        if e > max_entropy or e_s > entropy_spread:
            # print(f'skipped entropy')
            return False
        else:
            if print_solution:
                print(f'entropy of soln: {e}')

    # Handles what should happen when the final solution is found!
    if print_solution:
        for r in range(len(final_availability)):
            print(f"{final_availability[r]}: {num_booked[r]}")

    global export_solution
    if export_solution:
        print("exporting...")
        ep.save_workbook(final_availability)

    print(f"---")


    global got_solution
    global num_found
    got_solution = True
    num_found += 1




    # return False means keep searching
    # return True means stop after finding this solution
    global end_quick
    if end_quick:
        return True
    else:
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


def sum_points(availability, start_index):
    total_points = 0
    for i in range(start_index, len(availability[0])):
        # i is the index for each day
        # x is the index for each person
        x = 0
        while availability[x][i] == 0:
            x += 1
        total_points += availability[x][i]
    return total_points


def calc_avg(availability):
    # Calculates the final average number of points per person!
    # first, calculate the total number of points a day
    total_points = sum_points(availability, 0)

    # avg # of points per person is the total number of points, divided by the number of ppl.
    # multipy total_points by num_per_day b/c points required increases based on number of
    # ppl on call each day.
    avg = (num_per_day * total_points) / len(availability)
    return avg



def main_run(num_per_day, availability, end=False, max_difference=1):
    # Main running harness!

    finished_availability = create_finished_availability(availability)
    global person_mapping
    global day_mapping
    global avg
    global num_booked
    global got_solution
    global num_found
    global end_quick
    global max_diff
    global optimizing
    global entropy_spread
    global print_solution
    global timeout

    availability, person_mapping = order_ppl(availability)
    availability, day_mapping = order_days(availability)
    avg = calc_avg(availability)
    num_booked = [0] * len(availability)
    got_solution = False
    num_found = 0
    end_quick = end
    max_diff = max_difference


    print(f'--- sorted ---')
    # recursive call

    recursive_solver(availability, 0, finished_availability, num_booked)

    if not got_solution:
        print("----- no valid combo found! -----")
        return False
    else:
        print("-*-*-*- solutions found! -*-*-*-")
        return num_found






if __name__ == "__main__":
    availability = [[1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 0, 0, 0]]

    availability, dates, names = ep.open_notebook("Excel_Files/Given_Workbooks/Test.xlsx")

    print(f'Num solutions found: {main_run(num_per_day, availability, end=True, max_difference=max_diff)}')






