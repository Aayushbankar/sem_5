# P03 — LLM Behavior Test Matrix (fill-in template)

Use one LLM (ChatGPT / Gemini / Claude). Paste every output. Then fill the
"observed" columns and write a 5-line conclusion.

## Test A — Prompt variation (same task, 3 phrasings)

| # | Prompt | LLM output (paste below) | Observed differences |
|---|---|---|---|
| A1 | Explain machine learning. | | |
| A2 | Explain machine learning in 2 lines for a school student. | | |
| A3 | Explain machine learning with a concrete example, in a formal tone. | | |

**My notes (what changed between A1, A2, A3):**
- Length: ...
- Simplicity / vocabulary: ...
- Tone: ...
- Facts kept / dropped: ...

## Test B — Context understanding (add/remove context)

| # | Prompt | LLM output (paste below) | Observed differences |
|---|---|---|---|
| B1 | Summarize the meeting notes. | | |
| B2 | Summarize: {paste 3 lines of real notes here} | | |
| B3 | Summarize: {same notes}. Focus only on action items, list them as bullets. | | |

**My notes (which context mattered most):**
- Did B1 invent content? ...
- Did B2 stay closer to the text? ...
- Did B3 follow the output format? ...

## Test C — Response consistency (same prompt x3)

| # | Prompt | Output 1 | Output 2 | Output 3 | Same wording? |
|---|---|---|---|---|---|
| C1 | Give me one career tip. | | | | |
| C2 | 1+1 = ? Answer with only the number. | | | | |

**My notes:**
- C1 (creative) varied? ...
- C2 (constrained) stayed identical? ...
- Conclusion about temperature + format constraints: ...

## Conclusion (write 5 lines)
1. ...
2. ...
3. ...
4. ...
5. ...
