import unified_planning as up
from unified_planning.shortcuts import *

class Planner:
    def __init__(self):
        self.reader = up.io.PDDLReader()
        self.domain_file_path = "pddl/domain.pddl"

    def solve(self, problem_str):
        with open(self.domain_file_path, 'r') as domain_file:
            domain_str = domain_file.read()

        problem = self.reader.parse_problem_string(domain_str, problem_str)

        with OneshotPlanner(name="fast-downward") as planner:
            result = planner.solve(problem)
            if result.status in unified_planning.engines.results.POSITIVE_OUTCOMES:
                return result.plan
            else:
                return "No plan found."