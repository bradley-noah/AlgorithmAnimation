import random

from dinic import *






def verify_stability(events, maxflow):
    


    # Condition 1: flow on an edge doesn't exceed its capacity



    # Condition 2: incoming flow equal to ougoing for all nodes except source and sink




    return True, "Max Flow is Valid."







# Testing Engine
def run_tests():
    print(f"{'Test ID':<10} | {'Size':<6} | {'Result':<10} | {'Notes'}")
    print("-" * 60)




    # 1 - Case: one edge

    g = build_graph(2, [(0, 1, 10)])
    run_single_test(1, 2, g, 1, 10)




# Extra text templates


#    # 2 - Case: 
#
#    g = build_graph(2, [(0, 1, 10)])
#    run_single_test(1, 2, g, 1, 10)
#
#    # 3 - Case: 
#
#    g = build_graph(2, [(0, 1, 10)])
#    run_single_test()




    # 2-20. Randomized Stress Tests
    for i in range(2, 21):
        size = random.randint(3, 10)
        edges = random.randint(size, 15)
        cap = random.randint(1, 10)



        randomGraph = make_random_graph(size, edges, cap)

        graph = build_graph(size, randomGraph)

        run_single_test(i, size, randomGraph, edges, cap, f"Randomized n={size}")



def run_single_test(test_id, size, Graph, edges, cap, note):
    try:

        events, maxflow = dinic(Graph, 0, size-1)





        #UPDATE THIS

        stable, msg = verify_stability(events, maxflow)









        status = "PASS" if stable else "FAIL"
        print(f"{test_id:<10} | {size:<6} | {status:<10} | {note if stable else msg}")
    except Exception as e:
        print(f"{test_id:<10} | Error      | FAIL       | {str(e)}")




# The Is Main!!! dont bother with this
if __name__ == "__main__":
    run_tests()
