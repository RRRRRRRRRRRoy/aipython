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
    def __init__(self,domains,constraints,soft_constraints,soft_cost):
        # get the original variable 'domain' and 'constraints' from the supter class
        super().__init__(domains,constraints)
        self.soft_constraints = soft_constraints
        self.cost = soft_cost

############################################################################################################
################################## extend Search_with_AC_from_CSP class ####################################
# Adding soft_constraints and soft_cost in Search_with_AC_from_CSP class.
class Search_with_AC_from_Cost_CSP(Search_with_AC_from_CSP):
    def __init__(self,csp):
        super().__init__(csp)
        self.cost = list()
        self.soft_constrain = csp.soft_constraints
        # ???
        self.soft_cst = csp.self_cost


############################################################################################################
######################################## binary constraints ################################################
    # check the order of 2 tasks. same day or before.
    def binary_same_day(task1,task2):
        if task1[0]//10 == task2[0]//10:
            return True
        else:
            return False

    # check whether two tasks are start at the same time
    def binary_same_start(task1, task2):
        if task1[0] != task2[1]:
            return False
        else:
            return True

    # check whether task1 is before task2
    def binary_before(task1,task2):
        if task1[1]<=task2[0]:
            return True
        else:
            return False

    # check whether task1 is after task2
    def binary_after(tsk1,task2):
        if tsk1[1] > task2[0]:
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
        hardtime = lambda x:x[0]%10 == time
        return hardtime

    def hard_start_before_daytime(day,time):
        startsbefore = lambda x:x[0] <= day * 10 + time
        return startsbefore

    def hard_starts_before_time(time):
        startsbefore = lambda value:value[0]%10 <= time
        return startsbefore

    def hard_starts_after_daytime(day, time):
        def startsafter(val):
            giventime = day * 10 + time
            return val[0] >= giventime
        return startsafter

    def hard_starts_after_time(time):
        def startsafter(val):
            return val[0] % 10 >= time

        return startsafter

############################################################################################################
########################################## heuristic function ##############################################
