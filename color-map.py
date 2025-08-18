VARIABLES = ["A", "B", "C", "D", "E", "F", "G"]
CONSTRAINTS = [
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("B", "D"),
    ("B", "E"),
    ("C", "E"),
    ("C", "F"),
    ("D", "E"),
    ("E", "F"),
    ("E", "G"),
    ("F", "G")
]


def backtrack(map):
    """Runs backtracking search to find an assignment."""

    # Check if map is complete
    if len(map) == len(VARIABLES):
        return map

    # Try a new variable
    var = select_unassigned_variable(map)
    for value in ["Red", "Blue", "Green"]:
        new_map = map.copy()
        new_map[var] = value
        if consistent(new_map):
            result = backtrack(new_map)
            if result is not None:
                return result
    return None


def select_unassigned_variable(map):
    """Chooses a variable not yet assigned."""
    for variable in VARIABLES:
        if variable not in map:
            return variable
    return None


def consistent(map):
    """Checks to see if an assignment is consistent."""
    for (x, y) in CONSTRAINTS:

        # Only consider values where both are assigned
        if x not in map or y not in map:
            continue

        # If both have same value, then not consistent
        if map[x] == map[y]:
            return False

    # If nothing inconsistent, then assignment is consistent
    return True


solution = backtrack(dict())
print(solution)