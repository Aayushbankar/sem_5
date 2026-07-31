"""P09 - Case study snippets: code generation, debugging, and explanation.

Two worked cases, both runnable so the fixed behaviour can be verified.

Case 1 - Generated code: a function written by an AI assistant on request.
Case 2 - Debugging: a 'buggy' function (as if pasted from a broken project)
         plus its AI-debugged version. Run to see the bug reproduced, then
         confirmed fixed.

Run:  python3 p09_code_gen_debugging_cases.py
"""

import random


# ---------------------------------------------------------------------------
# Case 1: AI-generated function
# Prompt used:
#   "Write a Python function that takes a list of numbers and returns the
#    average, ignoring any non-numeric values. Add a docstring and handle the
#    empty-list case."
# ---------------------------------------------------------------------------
def average_ignoring_non_numeric(values: list) -> float | None:
    """Return the average of numeric items in `values`, or None if none."""
    numbers = [v for v in values if isinstance(v, (int, float))]
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


# ---------------------------------------------------------------------------
# Case 2a: BUGGY function (this is what a student might paste)
# ---------------------------------------------------------------------------
def buggy_flatten(nested: list) -> list:
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.append(buggy_flatten(item))      # BUG 1: appends list
        else:
            flat.append(item.upper())             # BUG 2: assumes strings
    return flat


# ---------------------------------------------------------------------------
# Case 2b: same function after an AI debug session
# ---------------------------------------------------------------------------
def fixed_flatten(nested: list) -> list:
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(fixed_flatten(item))      # FIX 1: extend, not append
        else:
            flat.append(str(item).upper())        # FIX 2: str() cast
    return flat


# ---------------------------------------------------------------------------
# Case 3: a flaky bug (off-by-one / zero division) found with a debugger
# ---------------------------------------------------------------------------
def buggy_avg_of_first_n(values: list, n: int) -> float:
    total = 0
    for i in range(1, n + 1):     # BUG: starts at index 1, skips values[0]
        total += values[i]
    return total / n              # BUG: crashes when n == 0


def fixed_avg_of_first_n(values: list, n: int) -> float:
    if n <= 0 or n > len(values):
        raise ValueError("n must be between 1 and len(values)")
    return sum(values[:n]) / n    # FIX: slice, handles n == 0 with clear error


def main() -> None:
    print("=" * 72)
    print("P09: AI TOOLS FOR SOFTWARE DEVELOPMENT - CODE CASES")
    print("=" * 72)

    print("\n[Case 1] AI-generated function 'average_ignoring_non_numeric'")
    for data in ([10, "x", 20, None, 30], [], [5, "a", 7]):
        result = average_ignoring_non_numeric(data)
        print(f"  {data!r:>28} -> average = {result}")

    print("\n[Case 2] Debugging 'flatten' (bug reproduced, then fixed)")
    sample = ["a", ["b", ["c", "d"]], "e"]
    print("  buggy_flatten ->", buggy_flatten(sample))
    print("  fixed_flatten ->", fixed_flatten(sample))

    print("\n[Case 3] Off-by-one bug in 'avg_of_first_n'")
    values = [10, 20, 30, 40, 50]
    try:
        buggy_result = buggy_avg_of_first_n(values, 3)
        print(f"  buggy_avg_of_first_n(values, 3) = {buggy_result} "
              "(WRONG: starts at index 1, silently skips values[0])")
    except IndexError as exc:
        print(f"  buggy_avg_of_first_n raised IndexError: {exc} "
              "(reads past the end of the list)")
    print(f"  fixed_avg_of_first_n(values, 3) = {fixed_avg_of_first_n(values, 3)}"
          " (correct: 10+20+30 / 3)")


if __name__ == "__main__":
    main()
