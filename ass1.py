############################################################################################################
# Analysis:
# giving a series tasks let all these task satisfy the constraints.
# STEP 1: Change the question into CSP problem
# STEP 2: Use arc consistency during the search process
# STEP 3: Use greedy search to find the best solution
############################################################################################################

import sys
from cspProblem import CSP, Constraint
from cspConsistency import Search_with_AC_from_CSP
from searchGeneric import AStarSearcher


############################################################################################################
# Notice 1:
# Change class Arc in searchProblem.py:
# Change the value of 'cost' in the function def __init__(self, from_node, to_node, cost=0, action=None) to 0.
# Without the variable 'cost' we can reduce the problem cost by 'cost' during the arrangement.
#
# Notice 2:
# Change the class dispaly in dispaly.py:
# Change the variable 'max_display_level' to 0.
# This change can help us disable the function display to print extra path.
############################################################################################################


############################################################################################################
######################################## extend CSP class ##################################################
# There is not variable called soft_constraints and soft_cost in the original source file in AIPython.
# To solve this assignment, extend the original class to a new one New_CSP can deal with the problem
# brought by the soft_constraints and soft_cost in the input files.
############################################################################################################


class New_CSP(CSP):
    def __init__(self, domains, constraints, soft_constraints, soft_cost):
        super().__init__(domains, constraints)
        self.soft_constraints = soft_constraints
        self.soft_cost = soft_cost


############################################################################################################
################################## extend Search_with_AC_from_CSP class ####################################
# Adding soft_constraints and soft_cost in Search_with_AC_from_CSP class.

class Search_with_AC_from_Cost_CSP(Search_with_AC_from_CSP):
    def __init__(self, csp):
        super().__init__(csp)
        self.cost = []
        self.soft_cons = csp.soft_constraints
        self.soft_cost = soft_cost

    ############################################################################################################
    ########################################## heuristic function ##############################################

    def heuristic(self, node):
        cost = 0
        cost_list = list()
        for task in node:
            if task in self.soft_cons:
                temp = list()
                expect_time = self.soft_cons[task]
                for index in node[task]:
                    actual_time = index[1]
                    if actual_time <= expect_time:
                        temp.append(0)
                    else:
                        delay_days = (actual_time // 10 - expect_time // 10) * 24
                        delay_hours = (actual_time % 10) - (expect_time % 10)
                        temp.append(self.soft_cost[task] * (delay_days + delay_hours))

                if len(temp) != 0:
                    mini = min(temp)
                    cost_list.append(mini)
        cost = sum(cost_list)
        return cost


############################################################################################################
######################################## binary constraints ################################################
# check the order of 2 tasks. same day or before.
def binary_same_day(task1, task2):
    get_task1_day = task1[0] // 10
    get_task2_day = task2[0] // 10
    if get_task1_day != get_task2_day:
        return False
    else:
        return True


# check whether two tasks are start at the same time
def binary_same_start(task1, task2):
    if task1[0] != task2[1]:
        return False
    else:
        return True


# check whether task1 is before task2
def binary_before(task1, task2):
    if task1[1] <= task2[0]:
        return True
    else:
        return False


# check whether task1 is after task2
def binary_after(task1, task2):
    if task1[1] > task2[0]:
        return True
    else:
        return False


############################################################################################################
########################################## hard constraints ################################################
# To check different situation of two tasks
# we can write all these function in Lambda expression
# we can also use nested function to solve this problem
# nestes function:
#   def xxxxxx():
#       def yyyyyyy();
#           return yyyyyy
#        return xxxxxxx
############################################################################################################

# To make the code more clean, just using the lambda func
def hard_day(day):
    # lambda function to express
    hardday = lambda x: x[0] // 10 == day
    return hardday


def hard_time(time):
    # can also use the same way(lambda expression) as hard_day to express, e.g.
    '''
    def hardtime(val):
    return val[0] % 10 == time
    '''
    hardtime = lambda x: x[0] % 10 == time
    return hardtime

# check whether starts before the day and time
def hard_start_before_daytime(day, time):
    startsbefore = lambda x: x[0] <= day * 10 + time
    return startsbefore

#
def hard_start_before_time(time):
    startsbefore = lambda value: value[0] % 10 <= time
    return startsbefore


def hard_start_after_daytime(day, time):
    startsafter = lambda x: x[0] >= day * 10 + time
    return startsafter


def hard_start_after_time(time):
    startsafter = lambda value: value[0] % 10 >= time
    return startsafter


def hard_end_before_daytime(day, time):
    endbefore = lambda value: value[1] <= day * 10 + time
    return endbefore


def hard_end_before_time(time):
    endbefore = lambda x: x[1] % 10 <= time
    return endbefore


def hard_end_after_daytime(day, time):
    endafter = lambda x: x[1] >= day * 10 + time
    return endafter


def hard_end_after_time(time):
    endafter = lambda val: val[1] % 10 >= time
    return endafter


def hard_startin_range(day1, time1, day2, time2):
    start_range = lambda x: day1 * 10 + time1 <= x[0] <= day2 * 10 + time2
    return start_range


def hard_endin_range(day1, time1, day2, time2):
    end_range = lambda x: day1 * 10 + time1 <= x[1] <= day2 * 10 + time2
    return end_range

############################################################################################################
########################################## Tool Functions ################################################
# function 1: check_content_in_line
# check content in the line or not based on the bool
# if bool is empty(default value is True), then check word in line or not
# if bool is False, them check word not in line or not.
#
# function 2: show_result
# after finishing the calculation,
# then pass the AStarSearcher object into this function
# check whether the solution is empty or not
# them traversal the dictionary and show the result
############################################################################################################

def check_content_in_line(check_word, line, bool=True):
    # boole will effect in/not in
    # this method can
    if bool:
        # check in
        if check_word in line:
            return True
        else:
            return False
    else:
        # check not in
        if check_word not in line:
            return True
        else:
            return False


def show_result(solution):
    if not solution:
        print('No solution')
    else:
        solution = solution.end()
        for task in solution:
            for key in week_to_num.keys():
                if week_to_num[key] == list(solution[task])[0][0] // 10:
                    day = key
            for key in time_to_num.keys():
                if time_to_num[key] == list(solution[task])[0][0] % 10:
                    time = key

            print(f'{task}:{day} {time}')
        print(f'cost:{problem.heuristic(solution)}')



# test in terminal
# filename = sys.argv[1]
# input1.txt is used to do the local test in Pycharm
filename = 'input1.txt'

# The reason of designing week_to_num and time_to_num in this way
# by this designing we can use the operator // or % to get the weekday and time.
# You can also use the 24-hour timing method
# eg: let Sunday be the first day, monday is 24 * 1 = 24
# the disadvantage of this method is that it is not intuitive as the following method

week_to_num = {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5}
time_to_num = {'9am': 1, '10am': 2, '11am': 3, '12pm': 4, '1pm': 5, '2pm': 6, '3pm': 7, '4pm': 8, '5pm': 9}
input_key_words = {0: "\n", 1: "#", 2: "task", 3: "constraint", 4: "domain"}
operation_key_word = {0: "same", 1: "starts", 2: "ends", 3: "before", 4: "after"}
operate_binary_constraints = {'before': binary_before, 'after': binary_after, 'same': binary_same_day,
                              'starts': binary_same_start}
operate_hard_constraints = {1: hard_day, 2: hard_time, 3: hard_start_before_daytime, 4: hard_start_before_time,
                            5: hard_start_after_daytime, 6: hard_start_after_time, 7: hard_end_before_daytime,
                            8: hard_end_before_time, 9: hard_end_after_daytime, 10: hard_end_after_time,
                            11: hard_startin_range, 12: hard_endin_range}
domain = list()

# double loop to create a list with weekday and time
for i in range(1, 6):
    for j in range(1, 10):
        week_n_time = i * 10 + j
        domain.append(week_n_time)
        # check the current of week_n_time
        # print(week_n_time)

task_duration = dict()
task_domain = dict()
soft_cost = dict()
soft_constraint = dict()
hard_constraint = list()
task_list = list()

file = open(filename, 'r', encoding='utf-8')
for line in file:
    # Remove '\n' and avoid the normal annotation
    if (line == input_key_words[0]) or (line[0] == input_key_words[1]):
        continue
    # Like COMP9021 read file operation
    # avoid space, empty line , and other punctuation
    line = line.strip()
    line = line.replace('\n', '')
    line = line.replace(',', '')
    line = line.replace('-', ' ')
    line = line.split(' ')
    ### get task and duration
    if line[0] == input_key_words[2]:
        # test the content of line
        # print(line)
        int_duration = int(line[2])
        task_duration.setdefault(line[1], int(line[2]))
        check_set = set()
        duration = int_duration
        for item in domain:
            if item % 10 + duration <= 9:
                check_set.add(item)
        task_domain[line[1]] = set((x, x + duration) for x in check_set)

    # check binary constraints
    elif line[0] == input_key_words[3]:
        task1 = line[::-1][-2]
        task2 = line[::-1][0]
        # check before
        if check_content_in_line(operation_key_word[3],line):
            hard_constraint.append(Constraint((task1, task2), operate_binary_constraints[operation_key_word[3]]))
        # check after
        if check_content_in_line(operation_key_word[4],line):
            hard_constraint.append(Constraint((task1, task2), operate_binary_constraints[operation_key_word[4]]))
        # check same day
        if check_content_in_line(operation_key_word[0],line):
            hard_constraint.append(Constraint((task1, task2), operate_binary_constraints[operation_key_word[0]]))
        # check starts at
        if check_content_in_line(operation_key_word[1],line):
            hard_constraint.append(Constraint((task1, task2), operate_binary_constraints[operation_key_word[1]]))

    # check domain input and get soft constraints
    elif line[0] == input_key_words[4] \
            and check_content_in_line(line[-1], week_to_num, False) \
            and check_content_in_line(line[-1], time_to_num, False):
        task = line[::-1][-2]
        day = week_to_num[line[4]]
        time = time_to_num[line[5]]
        change_info_2_num = day * 10 + time
        soft_cost.setdefault(task, int(line[-1]))
        soft_constraint.setdefault(task, change_info_2_num)

    else:
        # from the pdf, the input format is
        # domain t day
        #   0    1  2
        task = line[::-1][-2]
        # chenge task to tuple due to the parameter of function "Constraint"
        # only accept tuple
        tuple_task = (task,)
        line_in_2 = line[::-1][-3]
        if check_content_in_line(line_in_2, week_to_num):
            day = week_to_num[line[::-1][-3]]
            hard_constraint.append(Constraint(tuple_task, operate_hard_constraints[1](day)))

        elif check_content_in_line(line_in_2, time_to_num):
            time = time_to_num[line_in_2]
            hard_constraint.append(Constraint(tuple_task, operate_hard_constraints[2](time)))


        elif check_content_in_line(operation_key_word[1] , line) and\
                check_content_in_line(operation_key_word[3] , line):
            # domain t starts before day time
            if len(line) == 6:
                day = week_to_num[line[-2]]
                time = time_to_num[line[-1]]
                hard_constraint.append(Constraint(tuple_task, operate_hard_constraints[3](day, time)))
            # domain t starts before time
            if len(line) == 5:
                time = time_to_num[line[-1]]
                hard_constraint.append(Constraint(tuple_task, operate_hard_constraints[4](time)))

        elif check_content_in_line(operation_key_word[1] , line) and\
                check_content_in_line(operation_key_word[4] , line):
            # domain t starts after day time
            if len(line) == 6:
                day = week_to_num[line[-2]]
                time = time_to_num[line[-1]]
                hard_constraint.append(Constraint(tuple_task, operate_hard_constraints[5](day, time)))
            # domain t starts after time
            if len(line) == 5:
                time = time_to_num[line[-1]]
                hard_constraint.append(Constraint(tuple_task, operate_hard_constraints[6](time)))

        elif check_content_in_line(operation_key_word[2] , line) and\
                check_content_in_line(operation_key_word[3] , line):
            # domain t ends before day time
            if len(line) == 6:
                day = week_to_num[line[-2]]
                time = time_to_num[line[-1]]
                hard_constraint.append(Constraint(tuple_task, operate_hard_constraints[7](day, time)))
            # domain t ends before time
            if len(line) == 5:
                time = time_to_num[line[-1]]
                hard_constraint.append(Constraint(tuple_task, operate_hard_constraints[8](time)))

        # check 'ends' and 'after' in line or not
        elif check_content_in_line(operation_key_word[2] , line) and\
                check_content_in_line(operation_key_word[4] , line):
            # domain t ends after day time
            if len(line) == 6:
                day = week_to_num[line[-2]]
                time = time_to_num[line[-1]]
                hard_constraint.append(Constraint(tuple_task, operate_hard_constraints[9](day, time)))
            # domain t ends after time
            if len(line) == 5:
                time = time_to_num[line[-1]]
                hard_constraint.append(Constraint(tuple_task, operate_hard_constraints[10](time)))
        # day-time range
        else:
            # domain t starts in day time day time
            # check starts in line
            if check_content_in_line(operation_key_word[1] , line):
                day1 = week_to_num[line[4]]
                time1 = time_to_num[line[5]]
                day2 = week_to_num[line[6]]
                time2 = time_to_num[line[7]]
                hard_constraint.append(Constraint(tuple_task, operate_hard_constraints[11](day1, time1, day2, time2)))
            # check ends in line
            if check_content_in_line(operation_key_word[2] , line):
                day1 = week_to_num[line[4]]
                time1 = time_to_num[line[5]]
                day2 = week_to_num[line[6]]
                time2 = time_to_num[line[7]]
                hard_constraint.append(Constraint(tuple_task, operate_hard_constraints[12](day1, time1, day2, time2)))

csp = New_CSP(task_domain, hard_constraint, soft_constraint, soft_cost)
problem = Search_with_AC_from_Cost_CSP(csp)
solution = AStarSearcher(problem).search()


show_result(solution)