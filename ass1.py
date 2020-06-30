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
# Change the value of cost in the function def __init__(self, from_node, to_node, cost=0, action=None) to 0.
# Without the variable cost we can reduce the problem cost by 'cost' during the arrangement.
############################################################################################################
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
        # get the original variable domain and constraints from the supter class
        super().__init__(domains,constraints)