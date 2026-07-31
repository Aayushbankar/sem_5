# AI System Architecture Template — <Your Product>

> Reusable blank for [P02](../writeups/P02_ai_system_architecture.md). Every block must be filled with *your* product's version of it.

## 1. Block map
| Block | Role (generic) | What it is in MY product |
|---|---|---|
| **Data** | Everything the system learns from / uses at run-time | ____ |
| **Model** | The AI brain that transforms input → output | ____ |
| **Interface** | Where human and machine meet | ____ |
| **Feedback loop** | Output → user reaction → better data/model over time | ____ |

## 2. ASCII diagram (draw the four blocks + labelled arrows)
```
                ┌────────────────────────────┐
                │         USER               │
                └─────────────┬──────────────┘
                              │  ask / input
                              ▼
        ┌───────────────────────────────────────────────┐
        │ ③ INTERFACE  (screens of your product)         │
        └───────────────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────────┐
        │ ② MODEL   (your AI: what kind? API or local?) │
        └───────────────────────────────────────────────┘
                              ▲                 │
                              │                 ▼
              ┌───────────────┴────────┐   ┌────────────────────┐
              │ ① DATA                  │   │ ④ FEEDBACK LOOP    │
              │                         │   │                    │
              └─────────────────────────┘   └────────────────────┘
```

## 3. Data-flow steps
1. **Input:** ____
2. **Data capture:** ____
3. **Model call:** ____
4. **Output:** ____
5. **Feedback:** ____

## 4. Field notes (viva reminders)
- Name the *kind* of AI in the Model block — you do not need a specific API here (that's P08).
- Every arrow must answer "what travels along it?"
- If your model is a third-party API, add a small security/API-gateway block between Interface and Model.
