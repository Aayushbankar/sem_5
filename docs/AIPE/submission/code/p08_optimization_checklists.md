# P08 — Task-Based Prompt Engineering: Optimization Checklists

## Before/after tracker (3 tasks)
| Task | Before prompt (short) | Before output quality (1-5) | After prompt (short) | After output quality (1-5) | Biggest single fix |
|---|---|---|---|---|---|
| Summarization | | | | | |
| Blog generation | | | | | |
| Code generation | | | | | |

## Summarization checklist
- [ ] Input data pasted (don't write "summarize this article")
- [ ] Length + format fixed (bullets / N lines / paragraph)
- [ ] "Keep all numbers, dates, names" stated
- [ ] "Drop X (marketing, opinions)" stated
- [ ] Audience named (manager / child / engineer)
- [ ] Conclusion requested explicitly
- [ ] Long doc? Use chunked chain (P07)

## Blog generation checklist
- [ ] Title + angle supplied
- [ ] Audience + tone supplied
- [ ] Structure demanded (H1, sections, CTA)
- [ ] Word count set
- [ ] "No filler / no hype" stated
- [ ] Examples demanded ("one real example per section")
- [ ] Follow-ups: "rewrite hook 3 ways", "add FAQ", "give 3 heading options"

## Code generation checklist
- [ ] Language + function signature named
- [ ] Example input -> output given
- [ ] Edge cases listed (empty, wrong type, big input)
- [ ] Style demanded (docstring, type hints, names)
- [ ] Tests / asserts requested
- [ ] Explanation requested ("comment each block")
- [ ] CODE WAS RUN AND VERIFIED (never ship unverified AI code)

## Evaluation rubric (score each run 0-2)
| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Correctness | wrong | partial | fully correct |
| Completeness | misses core | covers core, skips details | all points + edges |
| Format | not followed | partially | exactly as asked |
| Usability | needs rewrite | light edits | ready to use |

## Meta-tip
Evaluate the OUTPUT, not the effort. If score < 8/8, change exactly ONE
prompt component and rerun. Record what changed and whether it helped.
