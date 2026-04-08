# Christian Lindner
# Verifies Hungarian assignment is valid and optimal by checking
# assignment length, row and column uniqueness, and computed total cost.
# can run with `python hungarian_testing.py` to see all test results.
# Formatted output matches gale_shapley_testing.py from Brock Kitterman
import itertools
import random

from hungarian import hungarian, make_random_cost_matrix

# using brute force to find minimum cost for optimal assignment
def brute_force_min_cost(cost_matrix):
    n = len(cost_matrix)
    if n == 0:
        return 0

    best = float("inf")
    for perm in itertools.permutations(range(n)):
        total = sum(cost_matrix[i][perm[i]] for i in range(n))
        if total < best:
            best = total
    return best

# check if assignment is valid
def verify_assignment(cost_matrix, assignment, reported_total, check_optimal=True):
    n = len(cost_matrix)

    if n == 0:
        if assignment != []:
            return False, "Expected empty assignment for empty matrix."
        if reported_total != 0:
            return False, "Expected zero cost for empty matrix."
        return True, "Valid empty assignment."

    if len(assignment) != n:
        return False, "Assignment size does not match matrix size."

    rows = [pair[0] for pair in assignment]
    cols = [pair[1] for pair in assignment]

    if sorted(rows) != list(range(n)):
        return False, "Rows are not assigned exactly once."
    if sorted(cols) != list(range(n)):
        return False, "Columns are not assigned exactly once."

    computed_total = sum(cost_matrix[i][j] for i, j in assignment)
    if computed_total != reported_total:
        return False, "Reported total cost does not match assignment sum."

    if check_optimal:
        best_possible = brute_force_min_cost(cost_matrix)
        if reported_total != best_possible:
            return False, f"Non-optimal result: got {reported_total}, expected {best_possible}."

    return True, "Assignment is valid and optimal."

# one test
def run_single_test(test_id, cost_matrix, note, check_optimal=True):
    try:
        _, assignment, total_cost = hungarian(cost_matrix, maximize=False)
        is_valid, msg = verify_assignment(cost_matrix, assignment, total_cost, check_optimal)
        status = "PASS" if is_valid else "FAIL"
        n = len(cost_matrix)
        print(f"{test_id:<10} | {n:<6} | {status:<10} | {note if is_valid else msg}")
    except Exception as e:
        print(f"{test_id:<10} | Error  | FAIL       | {str(e)}")


def run_tests():
    print(f"{'Test ID':<10} | {'Size':<6} | {'Result':<10} | {'Notes'}")
    print("-" * 70)

    # 1. Edge case: n=1
    c1 = [[5]]
    run_single_test(1, c1, "Minimal Case (n=1)")

    # 2. Benchmark matrix (known optimum = 13)
    c2 = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4],
    ]
    run_single_test(2, c2, "Known Benchmark")

    # 3. Tie-heavy costs
    c3 = [
        [4, 4, 4],
        [4, 4, 4],
        [4, 4, 4],
    ]
    run_single_test(3, c3, "All Costs Equal")

    # 4. Randomized stress tests
    for i in range(4, 21):
        size = random.randint(2, 7)
        c_random = make_random_cost_matrix(size, lo=1, hi=30)
        run_single_test(i, c_random, f"Randomized n={size}", check_optimal=True)


if __name__ == "__main__":
    run_tests()
