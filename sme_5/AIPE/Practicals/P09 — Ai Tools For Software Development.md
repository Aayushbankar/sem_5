---
subject: AIPE
status: not-started
tags: [subject/aipe, practical, unit/5]
practical: 9
unit: 5
hours: 2
---
# P09 — AI Tools for Software Development: Code Generation, Debugging, Explanation

**Subject:** Artificial Intelligence with Prompt Engineering | **Unit:** 5 | **Approx. Hrs:** 2
**PrO (verbatim):** *Use AI tools for software development tasks such as code generation, debugging, and code explanation.*

---

## 1. Objective
- Use an AI tool (ChatGPT/Gemini/Copilot) to **generate** a working function.
- Use the same tool to **debug** a buggy snippet and verify the fix.
- Use it to **explain** unfamiliar code.
- Distill **best-practice tips** for AI-assisted development.

## 2. Theory (exam-ready)

AI tools for software development (syllabus §5.2–5.3) cover four activities:

| Activity | What the AI does | Student skill needed |
|---|---|---|
| **Code generation** | Writes functions/scripts from a spec | Reviewing, running, testing |
| **Code explanation** | Explains what existing code does | Verifying the explanation |
| **Code documentation** | Adds docstrings/comments/READMEs | Checking accuracy |
| **Debugging** | Finds bugs and proposes fixes | Understanding the root cause |

**Golden rule:** the AI is a *pair programmer*, not an authority. Every generated or fixed line must be **run and tested**. The practicals below demonstrate exactly that workflow.

## 3. Case 1 — Code generation (function from a spec)

**Prompt used:**
> Write a Python function that takes a list of numbers and returns the average,
> ignoring any non-numeric values. Add a docstring and handle the empty-list case.

**AI output (function):**
```python
def average_ignoring_non_numeric(values: list) -> float | None:
    """Return the average of numeric items in `values`, or None if none."""
    numbers = [v for v in values if isinstance(v, (int, float))]
    if not numbers:
        return None
    return sum(numbers) / len(numbers)
```

**Verification (actual run of [[p09_code_gen_debugging_cases.py|`p09_code_gen_debugging_cases.py`]]):**
```
[Case 1] AI-generated function 'average_ignoring_non_numeric'
       [10, 'x', 20, None, 30] -> average = 20.0
                            [] -> average = None
                   [5, 'a', 7] -> average = 6.0
```
**Evaluation:** correct on mixed types, empty list, and clean numbers. ✅ Follow-up prompts that improve results: *"add type hints"*, *"write tests for the edge cases"*, *"explain each line"*.

## 4. Case 2 — Debugging a buggy snippet

**Buggy code given to the AI** (a broken recursive `flatten`):
```python
def buggy_flatten(nested):
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.append(buggy_flatten(item))      # BUG: appends the sub-list
        else:
            flat.append(item.upper())             # BUG: assumes strings
    return flat
```

**AI debug conversation (typical):**
> **User:** "This function should flatten a nested list but the output has
> nested lists still inside. Why?"
> **AI:** "`append()` adds the whole sub-list as one element. Use `extend()`
> to merge its items. Also `item.upper()` crashes on non-strings — cast with
> `str()`."

**AI-fixed version:**
```python
def fixed_flatten(nested):
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(fixed_flatten(item))      # FIX: extend, not append
        else:
            flat.append(str(item).upper())        # FIX: str() cast
    return flat
```

**Verification (actual run):**
```
[Case 2] Debugging 'flatten' (bug reproduced, then fixed)
  buggy_flatten -> ['A', ['B', ['C', 'D']], 'E']
  fixed_flatten -> ['A', 'B', 'C', 'D', 'E']
```

**Second bug** (off-by-one): the AI also found that `range(1, n + 1)` silently skips index 0:
```
[Case 3] Off-by-one bug in 'avg_of_first_n'
  buggy_avg_of_first_n(values, 3) = 30.0 (WRONG: starts at index 1, silently skips values[0])
  fixed_avg_of_first_n(values, 3) = 20.0 (correct: 10+20+30 / 3)
```
Notice the bug produced a **wrong answer with no error** — the worst kind. The AI fixed it with a slice `values[:n]` plus a clear `ValueError` for `n = 0`.

## 5. Case 3 — Code explanation

**Prompt:** "Explain this function line by line, and tell me the time complexity."
```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []
```
**AI explanation (summary):**
> One pass over the list. For each number `n`, check whether the *complement*
> `target - n` was already seen; if yes return both indices, else store the
> current number's index. Time O(n), space O(n). This is the classic
> hash-map solution, faster than the O(n²) nested-loop version.

**Verification:** trace by hand with `[2, 7, 11, 15], target=9` → `{2:0}`, `9-7=2 ∈ seen` → returns `[0, 1]`. ✅ Explanation is correct.

## 6. Best-practice tips (exam + lab ready)
1. **Give the AI a complete spec** — language, signature, examples, edge cases. Half-specs give half-working code.
2. **Ask for tests.** "Write 3 assert statements" forces edge-case thinking.
3. **Reproduce the bug before fixing it.** Run the buggy code, capture the error, then paste it *with the error message* to the AI — the traceback is the best debugging context.
4. **Never trust output blindly** — run it. Wrong-but-crash-free answers are the AI's scariest failure.
5. **Ask "why" as well as "how".** "Why does append fail here?" builds understanding; "fix it" alone doesn't.
6. **Prefer small prompts** — one function, one bug, one question per prompt (chaining, P07).
7. **Treat the AI as a rubber duck** — explaining your code to it (or asking it to explain) finds bugs.
8. **Don't paste secrets.** Never send API keys/passwords into a chat tool.

## 7. Deliverable — report skeleton
1. Case 1: prompt → generated code → run output → your evaluation.
2. Case 2: buggy code → error/behaviour → debug conversation → fixed code → verified output.
3. Case 3: code → explanation → your manual trace confirming it.
4. Best-practice tips (Section 6) with 3 examples from your own session.
5. Conclusion.

## 8. Conclusion
AI tools turn a developer's job from *writing every line* into *specifying, reviewing, running, and fixing*. The workflow that produced all three correct results above was the same: **precise prompt → generated/fixed code → run it → verify → ask why**. That loop is the professional skill.

## 9. Viva Q&A
1. **What are the 4 AI software-dev tasks?** — Generation, explanation, documentation, debugging.
2. **Why must you run AI-generated code?** — It can be wrong yet look perfect (silent wrong-answer bugs).
3. **What's the best thing to paste when debugging?** — The buggy code **plus** the exact error message/traceback.
4. **append vs extend in recursion?** — append adds a nested element; extend merges the sub-list's items.
5. **Why ask for tests?** — Forces the AI to handle edge cases and gives you verification.

## 10. Resources
- Run the cases: [[p09_code_gen_debugging_cases.py|`p09_code_gen_debugging_cases.py`]]
- GitHub Copilot docs: https://docs.github.com/en/copilot
- OpenAI cookbook (code generation): https://cookbook.openai.com
- Google AI for developers: https://developers.google.com

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Ai Tools For Software Development** in a real environment, it almost never works perfectly the first time. 
> 
> **Common Edge Cases to Test:**
> 1. **Network partitions:** What happens to this code if the Wi-Fi drops halfway through execution?
> 2. **Malformed Inputs:** How does the system behave if fed null values, extremely large datasets, or unexpected data types?
> 3. **Resource Exhaustion:** Does this script handle memory leaks or rate-limiting from APIs?

## 🔬 Extension Challenge

> [!example] Prove your expertise
> To truly master this practical, try modifying the code to achieve the following:
> - **Add robust error handling** (try/catch blocks) and structured logging instead of print statements.
> - **Parameterize the inputs** so the script can be run dynamically from the CLI without hardcoding values.
> - **Optimize it:** Can you reduce the execution time or memory footprint?

## 🎯 Key Takeaways

- **wrong answer with no error** — the worst kind. The AI fixed it with a slice `values[:n]` plus a clear `ValueError` for `n = 0`.
- **Give the AI a complete spec** — language, signature, examples, edge cases. Half-specs give half-working code.
- **Never trust output blindly** — run it. Wrong-but-crash-free answers are the AI's scariest failure.
- **Prefer small prompts** — one function, one bug, one question per prompt (chaining, P07).
- **Treat the AI as a rubber duck** — explaining your code to it (or asking it to explain) finds bugs.
- **What are the 4 AI software-dev tasks?** — Generation, explanation, documentation, debugging.
- **Why must you run AI-generated code?** — It can be wrong yet look perfect (silent wrong-answer bugs).
- **What's the best thing to paste when debugging?** — The buggy code **plus** the exact error message/traceback.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
