---
subject: <% tp.system.prompt("Subject code (FOB/IOT/AIPE/AIPD/CDCT)") %>
practical: <% tp.system.prompt("Practical number (e.g. 1)") %>
unit:
hours:
status: not-started
code_file: ""
tags: [subject/<% tp.system.prompt("Subject code").toLowerCase() %>, practical]
created: <% tp.date.now("YYYY-MM-DD") %>
---

# P<% tp.system.prompt("Practical number").padStart(2, '0') %> — <% tp.file.title.replace(/^P\d+ — /, '') %>

**Subject:** <% tp.system.prompt("Subject code") %> | **Unit:** | **Approx. Hrs:**
**PrO (verbatim):** *

---

## 1. Objective

-

## 2. Theory (exam-ready)

### Key Concepts

| Concept | Meaning |
|---|---|
|   |   |

## 3. Steps Performed

1.

## 4. Code

```python
# Code here
```

> Full runnable script: [[filename]]

## 5. Expected Output

```
Output here
```

## 6. Conclusion

In this practical, we learned:
-
