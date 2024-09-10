import excel_processing as ep
import sys
import os
from datetime import datetime
import time
import copy

path = 'C:/Users/doyle/Documents/GitHub/MS_Teams_Reminder'
app_path = path + '/main.py'


OPEN_LOCATION = "C:/Users/doyle/OneDrive - University of Toronto/RSS/Automations/Duty Solver/Unsolved/"
SAVE_LOCATION = "C:/Users/doyle/OneDrive - University of Toronto/RSS/Automations/Duty Solver/Solved/"
WORKBOOK_NAME = "Central.xlsx"



if path not in sys.path:
    sys.path.append(path)
    sys.path.append(app_path)



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
#
# - Add errors.txt
# - Increase max diff if timeout occurs
#
#
# --- Optimization ---
# Have a separate method check if someone is available at a given entry when doing tests.
# That way, you can do check if the person is actually available. Check if they're already
# booked on the next day or previous day, or if they're at their max # points, etc.

# Why did increasing the max_difference from 5 to 500 make solving Central SO much faster??

# --- setup ---
num_per_day = 2
print_solution = True
optimize_entropy = False
export_solution = True
repair = True

# --- hyper-parameters ---
# max_diff: maximum difference in number of points between som1 and the average
# max_entropy: higher val means greater tolerance of 2 consecutive days.
# entropy_spread: higher val means greater tolerance of going long periods without duty
max_difference = 500000000000
max_entropy = 10000000
entropy_spread = 1000000000000
max_time = 600

time_start = 0
best_so_far = []

# solution_distances tracks the {distance: time_found}
solution_distances = dict()

# error messages list imported from excel_processing
error_messages = ep.error_messages

def check_valid(fin_av, p_index, t_left, check_entropy=True):
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
    if check_entropy:
        # start by sorting back the days to their original order
        valid = valid and full_entropy_check(fin_av, person_mapping, day_mapping)

    return valid

def check_many_valid(fin_av, given_av, row, t_left, check_entropy=True):
    valid = True
    total_left = t_left * num_per_day
    for p in range(len(fin_av)):
        # -=- OPTIMIZATION -=-
        # When checking to see the maximum number of earnable points
        # for the next final days, do it in a separate method, and check to see
        # not just t_left, but individually calculate based on people's availabilities
        # and whether its a shift they can actually take
        # can_work = single_row_points_left(fin_av, given_av, row, p)
        can_work = 100
        if num_booked[p] > avg + max_diff:
            valid = False
        if num_booked[p] < avg - max_diff - min(t_left, can_work):
            # if it's impossible for us to get to the minimum, return False
            valid = False
        elif num_booked[p] < avg - max_diff:
            # There's only a certain number of points left.
            # if in the best case, we can't get everyone up to the
            # minimum number of points, we cut off this branch!


            total_left += num_booked[p] - (int(avg - max_diff) + bool((avg-max_diff)%1))
            # total_left += num_booked[p] - (avg - max_diff)
    if total_left < 0:
        valid = False


    if check_entropy:
        # start by sorting back the days to their original order
        valid = valid and full_entropy_check(fin_av, person_mapping, day_mapping)

    return valid

def single_row_points_left(fin_av, given_av, row, p):
    # checks how many points left this don can *actually* work!
    # p is the index of the don
    # index is the rows index
    total_workable = 0
    for day in range(row, len(fin_av[0])):
        # check to see if the don can actually work this day!
        # would check day before and after, but would require unwrapping the day.
        # try unwrapping the day
        total_workable += given_av[p][day]
    return total_workable

def full_entropy_check(fin_av, person_mapping, day_mapping):
    valid = True
    if optimize_entropy:
        final_availability = de_order_ppl(fin_av, person_mapping)
        final_availability = de_order_days(final_availability, day_mapping)

        e = calc_entropy(final_availability)
        if e > max_entropy:
            valid = False
            # print(f'***** failing in entropy check first')
    return valid

def calc_spread_out(availability):
    # calc a score based on how spread out a final set of days are!
    # same as calc_entropy but with added functions
    total_cost = 0
    weekday_max_run = 5
    weekend_max_run = 2

    for p in range(len(availability)):
        run = 0
        person_cost = 0

        z_run_v = 0
        z_total_cost = 0
        weekend = False

        for c in range(len(availability[0])):
            if availability[p][c] != 0:
                run += 1

                # print(f'run_length: {z_run_v}')
                z_total_cost += z_run_v ** 2
                z_run_v = 0

                if availability[p][c] == 2:
                    weekend = True
                else:
                    weekend = False

            else:
                z_run_v += 1

                if run > 1:
                    person_cost += run
                # if run != 0:
                #     person_cost += run
                if weekend and run >= weekend_max_run:
                    total_cost += 100000000000000
                elif not weekend and run >= weekday_max_run:
                    total_cost += 100000000000000
                run = 0

        person_cost = (person_cost ** 2) * 1000
        person_cost += z_total_cost

        total_cost += person_cost
    return total_cost

def calc_entropy(availability):
    # calc a score based on how bad a given solution is.
    # add 1 every time a given person has 2 consecutive shifts.
    # for each person, end by squaring the value
    total_cost = 0

    weekday_max_run = 100
    weekend_max_run = 100

    weekend_point_value = 2

    for p in range(len(availability)):
        # run is the length of the run
        # person cost is the sum of lengths of all runs for this person
        run = 0
        person_cost = 0
        weekend = False

        # for every day in this block
        for c in range(len(availability[0])):
            # if the day is not 0, our run continues
            if availability[p][c] != 0:
                run += 1
                if availability[p][c] == weekend_point_value:
                    weekend = True
                else:
                    weekend = False
            else:
                # the run has been broken b/c we reached a 0!
                #
                # if the run was greater than 1 (so an actual run), add the
                # length of the run to the person_cost.
                if run > 1:
                    person_cost += run
                if weekend and run >= weekend_max_run:
                    # uh oh! weekend overran.
                    total_cost += 100000000000000
                elif not weekend and run >= weekday_max_run:
                    # uh oh! Weekday overran
                    # if our run was greater than the max run, shoot up the entropy.
                    total_cost += 100000000000000
                # reset our run
                run = 0
        # square the length of all runs, and multiply by 1000
        person_cost = (person_cost ** 2) * 1000
        total_cost += person_cost

    return total_cost


def check_people_on_day(availability, num_booked):
    # check that there are still people who can take a shift on each day, even when some of
    # the available people have already reached their max number of points.
    #
    # -=- OPTIMIZATION -=-
    # Just return False right if we find a contradiction, don't keep going.
    all_valid_days = True

    for s in range(len(availability[0])):
        num_available = 0
        for d in range(len(availability)):
            if availability[d][s] != 0 and num_booked[d] <= avg + max_diff:
                num_available += 1
        if num_available < 2:
            all_valid_days = False

    return all_valid_days

def check_none_exceed_maxDist(num_booked):
    # true means no one exceeds the maximum distance!
    # False means someone is greater than the maximum distance
    for d in num_booked:
        if d > avg + max_diff:
            return False
    return True


def recursive_solver(availability, index, finished_availability, num_booked):
    # The main recursive call for our solver!
    #
    # number of points must be within the max_diff of the average
    # for the solution to be valid!

    # first check to make sure we didn't time out
    if time.time() - time_start > max_time:
        return found_solution(availability, finished_availability, timeout=True)

    # if we're past the final column...
    if index >= len(availability[0]):
        for person_i in range(len(num_booked)):
            if num_booked[person_i] < avg - max_diff or num_booked[person_i] > avg + max_diff:
                # exists a person who is outside the range!
                return False
        # Found a valid solution!
        # Every person is within range and we've recursed through every day!
        return found_solution(availability, finished_availability)

    t_left = sum_points(availability, index)

    if not check_people_on_day(availability, num_booked):
        print(f'terminating because of me!')
        return False


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
                    found = recursive_solver(availability, index + 1, finished_availability, num_booked)
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

                # our max_distance may have been lowered in a child call.
                # If so, check that our solution doesn't already exceed that max distance!
                if not check_none_exceed_maxDist(num_booked):
                    return False


                if not check_many_valid(finished_availability, availability, index, t_left, check_entropy=True):
                    # print(f'even slighter shortcut!')
                    return False

    # Went through every combination of names and still didn't find a solution.
    # Therefore, outside combination had a fault.
    # print(avg)
    # found_solution(finished_availability)
    return False


def found_solution(availability, finished_availability, timeout=False):
    global best_so_far
    global time_start
    global max_time
    global got_solution

    if timeout:
        print(f'timing out!')
        return True

    final_availability = de_order_ppl(finished_availability, person_mapping)
    final_availability = de_order_days(final_availability, day_mapping)

    # next do our entropy check
    # this significantly slows down our algo...
    global optimize_entropy
    if optimize_entropy and False:
        e = calc_entropy(final_availability)
        e_s = calc_spread_out(final_availability)
        # e_s = 0
        if e > max_entropy or e_s > entropy_spread:
            # skipped solution because of entropy!


            # check here? Weird many calls
            # print(f'max entropy exceeded!')
            # print(f'e: {e}, e_s: {e_s}')
            # for row in finished_availability:
            #     print(row)
            #
            # print(f'===========')
            # for row in final_availability:
            #     print(row)


            return False

    global num_found
    global max_diff

    max_dist = find_max_dist_list(num_booked)
    got_solution = True

    # check here? Weird many calls
    # print(f'final solution found... {max_diff}, {max_dist}')



    if max_dist != max_diff:
        num_found += 1
        print(f'found better solution! ({(time.time() - time_start):06.2f}) New: {max_dist}, Prev: {max_diff}')

        # solution_distances tracks {distance: time_found}
        solution_distances[max_dist] = time.time() - time_start
        best_so_far = copy.deepcopy(finished_availability)
        # subtract small amount from max_dist because we want to find a solution with a better spread, not an equal one
        max_diff = max_dist - 0.01

    if time.time() - time_start < max_time:
        # continues the search until the time limit is reached!
        return False
    else:
        error_messages.append("timing out!")
        print(f'timing out...')

    return True


def export_solution(availability):
    # exports the final solution!
    # takes the original availability as input to help do some swaps
    # if repair is set to true.
    global got_solution
    global best_so_far
    global repair


    if got_solution:

        final_availability = de_order_ppl(best_so_far, person_mapping)
        final_availability = de_order_days(final_availability, day_mapping)
        if repair:
            copy_avail = copy.deepcopy(availability)
            unmapped_availability = de_order_ppl(copy_avail, person_mapping)
            unmapped_availability = de_order_days(unmapped_availability, day_mapping)
            repair_solution(unmapped_availability, final_availability)


        est_num_booked = re_calc_numBooked(final_availability)
        for r in range(len(final_availability)):
            print(f"{final_availability[r]}: {est_num_booked[r]}")
        ep.save_workbook(final_availability)
        print(f"---")


def find_max_dist_list(num_booked):
    # Finds the maximum distance from the average!
    max_dist = 0
    for don in num_booked:
        if abs(don - avg) > max_dist:
            max_dist = abs(don-avg)
    return max_dist

def find_max_dist_dict(num_booked):
    max_dist = 0
    for don in num_booked:
        if abs(num_booked[don] - avg) > max_dist:
            max_dist = abs(num_booked[don] - avg)
    return max_dist

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

def re_calc_numBooked(availability):
    # recalculates num_booked!
    new_num_booked = dict()
    for line in range(len(availability)):
        new_num_booked[line] = 0
        for day in availability[line]:
            new_num_booked[line] = new_num_booked[line] + day

    return new_num_booked

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

    for found_i in range(len(tuples)):
        dict_mapping[tuples[found_i][1]] = found_i


    sorted_array = []
    for i in range(len(tuples)):
        sorted_array.append(availability[tuples[i][1]])

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
    diff2 = 0
    for p in range(len(availability)):
        if availability[p][index] != 0:
            difficulty += 1
            # days are more difficult if the only people who are available are people who don't have a lot of availability
            # diff2 tracks how many easy people are available that day
            diff2 += p




    return difficulty, diff2

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
        difficulty, diff2 = calc_difficulty(availability, d)
        diff_tuples.append((difficulty, diff2, d))

    diff_tuples.sort()
    for t in range(len(diff_tuples)):
        orig_mapping[t] = diff_tuples[t][2]

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

# -------------------
# These are some preliminary checks on the data to see if the schedule can even be solved.
# def do_checks(availability):
#     # takes an already sorted availability
#     days_helping = dict()
#     num_helping = 0
#     # days_helping has format {duty_index : [day helping 1, day helping 2,...]}
#
#     # start with the first day
#     # go on to the day that adds the least people but the most points (# points / # new people)
#
#     for low_index in range(availability[0]):
#         for high_index in range(low_index, availability[0]):
#             #
#             points_required = 0
#             curr_index = low_index
#             utility = get_days_utility(days_helping, availability, curr_index)
#             if utility > 1:
#
#
#
# def get_days_utility(days_helping, availability, curr_index):
#     points_giving = 0
#     new_people = 0
#     for d in availability[curr_index]:
#         if availability[curr_index][d] != 0:
#             points_giving = availability[curr_index][d]
#
#             if d not in days_helping:
#                 new_people += 1

    #         days_helping[d].append(curr_index)
    #
    # if new_people == 0:
    #     return 100000000000000
    # return points_giving / new_people

def repair_solution(availability, final_availability):
    # Takes some final availability and attempts to fix it!
    # Swaps shifts where the swappee has too few points, and swapper
    # has too many.
    num_booked = re_calc_numBooked(final_availability)

    # while making swaps is helpful...
    c = 1
    total_swaps = 0
    while c != 0:
        # do the swaps!
        c = comb(availability, final_availability, num_booked)
        # if any changes are made, track them.
        if c != 0:
            print(f'made {c} changes!')
            total_swaps += c

    if total_swaps != 0:
        error_messages.append(f'Debug: Made {total_swaps} shift swaps!')

    # md = find_max_dist_dict(num_booked)
    # solution_distances[md] = time.time() - time_start




def comb(availability, final_availability, num_booked):
    num_changes = 0

    # we comb through every day!
    for day in range(len(final_availability[0])):
        # first, find which dons are working.
        dons_working = []
        for d in range(len(final_availability)):
            if final_availability[d][day] != 0:
                dons_working.append(d)
        # then, we check which dons are free.
        dons_free = []
        for d in range(len(availability)):
            if availability[d][day] != 0:
                dons_free.append(d)

        # store the value of this day
        day_value = final_availability[dons_working[0]][day]

        # now, check if any of the free dons would benefit from taking the shift (or any busy dons would benefit from giving away)
        for f in dons_free:
            for d in dons_working:
                # see what would happen if we gave this shift away
                distance_start = abs(num_booked[d] - avg) + abs(num_booked[f] - avg)
                distance_swap = abs(num_booked[d] - avg - day_value) + abs(num_booked[f] - avg + day_value)

                # if switching shifts is desirable...
                if distance_swap < distance_start:

                    # first check that the switch would be valid.
                    # A switch is invalid if the swapee now has consecutive shifts.
                    can_swap = True
                    if day > 0:
                        if final_availability[f][day-1] != 0:
                            can_swap = False
                    elif day < len(final_availability[0]) - 1:
                        if final_availability[f][day+1] != 0:
                            can_swap = False

                    # if we can swap, lets swap!
                    if can_swap:
                        # update num_booked to reflect our swap
                        num_booked[d] = num_booked[d] - day_value
                        num_booked[f] = num_booked[f] + day_value
                        # update our availability
                        final_availability[f][day], final_availability[d][day] = final_availability[d][day], final_availability[f][day]
                        # change the working list to reflect our changes
                        dons_working.append(f)
                        dons_working.remove(d)
                        num_changes += 1

    return num_changes


    # for don_t in too_high:
    #     for d_i in range(len(availability[0])):
    #         if availability[don_t[1]] != 0:
    #             for don_swaper_t in too_low:
    #                 if availability[don_t[1]] != 0:
# ------------------




def main_run(num_per_day, availability, end=False, max_difference=3):
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
    global time_start
    global best_so_far
    global solution_distances


    time_start = time.time()

    availability, person_mapping = order_ppl(availability)
    availability, day_mapping = order_days(availability)
    avg = calc_avg(availability)
    num_booked = [0] * len(availability)
    got_solution = False
    solution_distances = dict()
    num_found = 0
    end_quick = end
    max_diff = max_difference
    best_so_far = []


    print(f'--- sorted ---')
    for row in availability:
        print(row)
    # recursive call

    recursive_solver(availability, 0, finished_availability, num_booked)

    if not got_solution:
        print("----- no valid combo found! -----")
        error_messages.append(f'* ERROR: no valid combinations found!')

        error_messages.append(f'          - Ensure at least 2 people are available every day')
        error_messages.append(f'          - Ensure no one is required to work multiple consecutive days')
        error_messages.append(f'          - Ask RSS to increase their availability on days with low availability.')
        error_messages.append(f'          - OR ask to increase the maximum point difference')
        return False
    else:
        export_solution(availability)
        print("-*-*-*- solutions found! -*-*-*-")
        return num_found




def loop_solve(num_per_day, availability, end=True, max_difference=3):
    # Iterates through the main loop until the smallest max_difference is found!
    global got_solution

    created_first = False

    for filename in os.listdir(OPEN_LOCATION):

        # creates the run_data.txt file on the first pass only! This way, doesn't create a run_data.txt
        # when not necessary.
        if not created_first:
            print('opening first file...')
            run_data_directory = SAVE_LOCATION + "run_data.txt"
            run_data = open(run_data_directory, "a+")

            now = datetime.now()
            formatted_time = now.strftime('%H:%M:%S %b %d, %Y')
            run_data.writelines(f"Solving at {formatted_time}\n")
            error_messages.append(f'')
            error_messages.append(f'')
            created_first = True


        f = os.path.join(OPEN_LOCATION, filename)
        if os.path.isfile(f):
            error_messages.append(f'--------------------------------------------------')
            error_messages.append(f'solving {filename}')
            error_messages.append(f'')
            start = time.time()

            print(f'solving...')
            print(f)
            availability, names = ep.open_notebook(f)

            if availability == False:
                # availability is only false if an error occurred during processing
                error_messages.append(f'skipping {filename} due to fatal error.')
                got_solution = False
            else:

                main_run(num_per_day, availability, end=end, max_difference=max_difference)


            os.remove(f)


            if got_solution:
                error_messages.append(f'')
                error_messages.append(f'found solution!')

                distances = solution_distances.keys()
                min_time = solution_distances[min(distances)]

                error_messages.append(f'time taken: {(min_time):06.2f}, worst distance from average: {max(distances)}')
            else:
                error_messages.append(f'* ERROR: Unable to find solution for')
                error_messages.append(f'{filename}')

                end = time.time()
                error_messages.append(f'time taken: {(end - start):06.2f}')

            error_messages.append(f'')

        while error_messages:
            run_data.writelines(f'{error_messages.pop(0)}\n')


def reset_variables():
    # resets the global variables after each iteration
    pass


if __name__ == "__main__":
    availability = [[1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 0, 0, 0]]
    default_path = OPEN_LOCATION + WORKBOOK_NAME

    loop_solve(num_per_day, availability, end=True, max_difference=max_difference)







