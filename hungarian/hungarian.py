import random


def hungarian(cost_matrix, maximize=False):
    n = len(cost_matrix)
    if n == 0:
        return [], [], 0

    events = []
    original = [row[:] for row in cost_matrix]

    if maximize:
        max_val = max(max(row) for row in cost_matrix)
        C = [[max_val - cost_matrix[i][j] for j in range(n)] for i in range(n)]
    else:
        C = [row[:] for row in cost_matrix]

    events.append({"type": "init", "matrix": _snap(C), "original": _snap(original), "maximize": maximize})

    # row reduction
    row_mins = []
    for i in range(n):
        rm = min(C[i])
        row_mins.append(rm)
        C[i] = [C[i][j] - rm for j in range(n)]
    events.append({"type": "row_reduce", "matrix": _snap(C), "row_mins": row_mins})

    # col reduction
    col_mins = []
    for j in range(n):
        cm = min(C[i][j] for i in range(n))
        col_mins.append(cm)
        for i in range(n):
            C[i][j] -= cm
    events.append({"type": "col_reduce", "matrix": _snap(C), "col_mins": col_mins})

    # cover and adjust until we get a full matching
    iteration = 0
    while True:
        iteration += 1
        match_row, match_col = _max_matching(C, n)
        matching = [(i, match_row[i]) for i in range(n) if match_row[i] != -1]

        events.append({"type": "match", "matrix": _snap(C), "matching": matching,
                        "cover_count": len(matching), "iteration": iteration})

        if len(matching) == n:
            break

        row_covered, col_covered = _min_cover(C, n, match_row, match_col)
        events.append({"type": "cover", "matrix": _snap(C), "row_covered": list(row_covered),
                        "col_covered": list(col_covered), "matching": matching, "iteration": iteration})

        # subtract min uncovered from uncovered cells, add to doubly covered
        min_val = min(C[i][j] for i in range(n) for j in range(n)
                    if not row_covered[i] and not col_covered[j])
        for i in range(n):
            for j in range(n):
                if not row_covered[i] and not col_covered[j]:
                    C[i][j] -= min_val
                elif row_covered[i] and col_covered[j]:
                    C[i][j] += min_val
        events.append({"type": "adjust", "matrix": _snap(C), "min_val": min_val, "iteration": iteration})

    assignment = [(i, match_row[i]) for i in range(n)]
    total_cost = sum(original[i][j] for i, j in assignment)
    events.append({"type": "done", "matrix": _snap(C), "assignment": assignment, "total_cost": total_cost})

    return events, assignment, total_cost


def _snap(matrix):
    return [row[:] for row in matrix]


def _max_matching(C, n):
    match_row = [-1] * n
    match_col = [-1] * n
    for i in range(n):
        visited = [False] * n
        _augment(C, n, i, match_row, match_col, visited)
    return match_row, match_col


def _augment(C, n, i, match_row, match_col, visited):
    for j in range(n):
        if C[i][j] == 0 and not visited[j]:
            visited[j] = True
            if match_col[j] == -1 or _augment(C, n, match_col[j], match_row, match_col, visited):
                match_row[i] = j
                match_col[j] = i
                return True
    return False


def _min_cover(C, n, match_row, match_col):
    # konig's theorem: start from unmatched rows, alternate marking
    marked_rows = set(i for i in range(n) if match_row[i] == -1)
    marked_cols = set()

    changed = True
    while changed:
        changed = False
        for i in list(marked_rows):
            for j in range(n):
                if C[i][j] == 0 and j not in marked_cols:
                    marked_cols.add(j)
                    changed = True
        for j in list(marked_cols):
            i = match_col[j]
            if i != -1 and i not in marked_rows:
                marked_rows.add(i)
                changed = True

    # cover = unmarked rows + marked cols
    row_covered = [i not in marked_rows for i in range(n)]
    col_covered = [j in marked_cols for j in range(n)]
    return row_covered, col_covered


def make_random_cost_matrix(n=4, lo=1, hi=20):
    return [[random.randint(lo, hi) for _ in range(n)] for _ in range(n)]


if __name__ == "__main__":
    test = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4],
    ]
    events, assignment, cost = hungarian(test)
    print(f"assignment: {assignment}, cost: {cost}")