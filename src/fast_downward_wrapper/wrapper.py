import subprocess
import tempfile
import os

class FastDownwardWrapper:
    def __init__(self):
        self.fd_path = './external/fast_downward/fast-downward.py'
        self.domain_file_path = "./pddl/domain.pddl"

    def solve(self, problem_str):
        # Create temporary file for the problem
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.pddl') as problem_file:
            problem_file.write(problem_str)
            problem_file_path = problem_file.name
        
        # Construct the Fast Downward command
        cmd = [self.fd_path, "--alias", "seq-sat-lama-2011", self.domain_file_path, problem_file_path]
        
        plan_file_path = 'sas_plan.1'
        try:
            # Run Fast Downward
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            # Optionally, parse the result.stdout to extract the plan
            if os.path.exists(plan_file_path):
                with open(plan_file_path, 'r') as plan_file:
                    plan_content = plan_file.read()
                    return plan_content
            else:
                return "No plan found."
        finally:
            # Clean up temporary file
            os.remove(problem_file_path)
            if plan_file_path and os.path.exists(plan_file_path):
                os.remove(plan_file_path)

# Example use:
# fd_wrapper = FastDownwardWrapper()
# fd_wrapper.solve(problem_pddl_string)
