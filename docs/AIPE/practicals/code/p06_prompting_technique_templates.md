# P06 — Prompting Technique Templates (zero-shot, few-shot, role-based)

## Zero-shot template
```
Classify / summarize / translate / generate [task].
Input: [your data here]
Output format: [table | 2 lines | JSON | bullets]
```

## Few-shot template
```
[Task statement]

Example 1:
Input: [ex]
Output: [ex]

Example 2:
Input: [ex]
Output: [ex]

Now do it for:
Input: [real input]
```

### Few-shot design rules
- Use 2-5 examples covering the *edge cases* you care about.
- Keep examples short but exact — the model copies their shape.
- Include one tricky negative example if mistakes are costly.

## Role-based template
```
You are a [role] with expertise in [domain].
[Constraints: audience, tone, length, format]
[Task]
[Input data]
```

### Role ideas per task
| Task | Role |
|---|---|
| Email | professional writing coach |
| Explain concepts | primary-school teacher / engineering mentor |
| Code review | senior Python reviewer |
| Blog | marketing copywriter |
| Quiz | exam setter (GTU style) |
| Summaries | editorial assistant (no fluff) |

## Combined template (all three techniques at once)
```
You are a [role]. Complete the task below.

Examples (use the same format):
[input] -> [output]
[input] -> [output]

Task: [real task]
Input: [data]
Output format: [specified]
```

## Self-test — pick the right technique
1. "Tell me 3 interview tips" → zero-shot / few-shot / role-based?
2. "Convert these 10 sentences into CSV rows exactly like the sample" → ?
3. "Reply as a polite customer-support agent" → ?
4. "Classify reviews as positive/negative, format must match exactly" → ?
5. "Explain recursion to a first-year student" → ?

*(Answers: 1 zero-shot, 2 few-shot, 3 role, 4 few-shot, 5 role/zero-shot with audience)*
