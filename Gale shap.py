//Test
from gale_shapley import *

"""
This is a test to see if matching is stable. An unstable matching exists if there is a blocking pair.
"""
def verify_stability(matching, p_prefs, r_prefs):
    proposers = list(p_prefs.keys())
    receivers = list(r_prefs.keys())
    
    # Check for all matching
    if len(matching) != len(proposers):
        return False, "Not everyone is matched."
    
    matched_receivers = set(matching.values())
    if len(matched_receivers) != len(receivers):
        return False, "Not all receivers are matched or someone is matched twice."

    # Check for blocking pairs
    for m, current_w in matching.items():
        m_pref_list = p_prefs[m]
        
        current_w_rank = m_pref_list.index(current_w)
        better_receivers = m_pref_list[:current_w_rank]
        
        for w in better_receivers:
            current_m_of_w = next(m_key for m_key, w_val in matching.items() if w_val == w)
            
            w_pref_list = r_prefs[w]
            if w_pref_list.index(m) < w_pref_list.index(current_m_of_w):
                return False, f"Blocking pair found: ({m}, {w})"

    return True, "Matching is stable."

# Testing Engine
def run_tests():
    print(f"{'Test ID':<10} | {'Size':<6} | {'Result':<10} | {'Notes'}")
    print("-" * 60)

    # 1. Edge Case: n=1
    p1 = {'M1': ['W1']}; r1 = {'W1': ['M1']}
    run_single_test(1, p1, r1, "Minimal Case (n=1)")

    # 2. Case: Everyone gets their first choice
    p2 = {'M1': ['W1', 'W2'], 'M2': ['W2', 'W1']}
    r2 = {'W1': ['M1', 'M2'], 'W2': ['M2', 'M1']}
    run_single_test(2, p2, r2, "Optimal Harmony")

    # 3. Case: Complete Conflict (All proposers want same receiver)
    p3 = {'M1': ['W1', 'W2'], 'M2': ['W1', 'W2']}
    r3 = {'W1': ['M2', 'M1'], 'W2': ['M1', 'M2']}
    run_single_test(3, p3, r3, "Total Conflict")

    # 4-20. Randomized Stress Tests
    for i in range(4, 21):
        size = random.randint(3, 10)
        p_random, r_random = make_random_scenario(size)
        run_single_test(i, p_random, r_random, f"Randomized n={size}")

# Run exactly one test of the algorithm.
def run_single_test(test_id, p_prefs, r_prefs, note):
    try:
        _, matching = gale_shapley(p_prefs, r_prefs)
        stable, msg = verify_stability(matching, p_prefs, r_prefs)
        status = "PASS" if stable else "FAIL"
        print(f"{test_id:<10} | {len(p_prefs):<6} | {status:<10} | {note if stable else msg}")
    except Exception as e:
        print(f"{test_id:<10} | Error      | FAIL       | {str(e)}")

if __name__ == "__main__":
    run_tests()
