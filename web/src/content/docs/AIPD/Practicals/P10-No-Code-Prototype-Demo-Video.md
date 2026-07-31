---
title: "P10 — No Code Prototype Demo Video"
sidebar:
  order: 10
---

# P10 — No-Code Prototype (Glide) & 2–3 Minute Demo Video

**Subject:** AI Product Design | **Unit:** 4 | **Approx. Hrs:** 2
**PrO (verbatim):** *Develop prototype using no-code tools and prepare demo video (2–3 minutes).*

---

## 1. Objective
- Build a **clickable prototype** of StudyMate with a no-code tool (this write-up uses **Glide**; FlutterFlow and Bubble work the same way — see the mapping table).
- Prepare a **turnkey 2–3 minute demo video**: this write-up gives the shot-by-shot storyboard — *you* record it on your phone and stitch it with CapCut/Canva video.

## 2. Why Glide (and the alternatives)

| Tool | Skill level | Best for | Data source | Our choice |
|---|---|---|---|---|
| **Glide** | Very low | Mobile-style app from a spreadsheet, fast | Google Sheets | ✅ **Chosen** — fastest to a clickable demo |
| FlutterFlow | Medium | Custom logic, real app feel | Firebase/Supabase | If you want more control |
| Bubble | Medium | Web apps with databases + plugins | Its own DB | If you need AI plugins today |
| Framer | Low | Marketing pages / landing page | — | For P09 landing page |

## 3. Glide build guide (step-by-step, filled)

### 3.1 Data source (Google Sheet: `study_mate_demo`)
| sheet_tab | columns |
|---|---|
| `notes` | `id, title, subject, status(summarized/done), score` |
| `quiz` | `id, question, a, b, c, d, correct, subject, difficulty` |
| `topics` | `topic, subject, strength(weak/ok/strong)` |

### 3.2 Screens & actions

| Screen | Glide element | Action wired |
|---|---|---|
| **Home** | Photo from `notes` (list), relation to `topics` | On tap → Chat |
| **Upload** | File uploader + "Summary" button | Button → show summary card + append row to `notes` |
| **Chat** | Text input + "Ask" button | Button → show a *pre-scripted* grounded answer card (demo-mode: canned + citation, since real LLM calls need a backend) |
| **Quiz** | Single-choice questions bound to `quiz` | On submit → compute score, set `strength` on wrong topics |
| **Results** | Collection of weak topics + retry button | Button → filters quiz to weak topics |
| **Settings** | Switch toggles (privacy) + "Delete data" | Toggle → hides analytics; Delete → clears sheet rows |

> **Demo-mode trick:** in a no-code prototype the AI is **mocked** (canned answers). That's the point of a prototype — test the *flow*, not the model. Write "AI SIMULATED" on the demo's chat card so the examiner knows you understand the difference.

### 3.3 Glide essentials you must name in the report
- **Tables** (data source), **Screens** (tabs), **Components** (list, button, input), **Relations** (notes ↔ quiz via subject), **Actions** (go-to-screen, update-row, send-notification), **Publishing** (Glide gives you a shareable app link).

## 4. Blank Template (copy into `../code/p10_demo_storyboard_template.md`)

```
# <Product> — Glide Prototype + Demo Video (blank)

## Tool choice & why
## Data source
| Table | Columns |
## Screens & actions
| Screen | Component | Action |
## Demo video storyboard (shot-by-shot)
| Shot | Time | Scene (what's on screen) | Audio / narration | Cue to next |
## Checklist (prep → record → edit → publish)
```

## 5. Demo video storyboard (filled — StudyMate, 2:30 total) 🎬

> Record with your phone in landscape, at a desk with good light. Every shot's narration is written; read it naturally, 30–45 s per act.

| Shot | Time | Scene on screen | Narration (write these on a cue card) |
|---|---|---|---|
| **1. Hook** | 0:00–0:15 | Close-up: thick notebook → zoom to phone with StudyMate home | "This notebook is 40 pages of pure panic. This app turns it into a revision plan in under a minute. Meet StudyMate." |
| **2. Upload** | 0:15–0:40 | Screen-record: home → upload PDF → progress bar → summary appears | "I upload my Machine Design notes — StudyMate reads my own PDF, not the whole internet. In about 30 seconds: a one-page summary, with the topics my notes actually cover." |
| **3. Chat (grounded)** | 0:40–1:10 | Ask a question in chat → answer card with citation [slide 14] | "Now the part I care about: I ask 'explain Kirchhoff's law the way MY notes do' — and it answers from my notes, with the exact slide as proof. No generic Google answer." |
| **4. Quiz + weak topics** | 1:10–1:45 | Take 5 MCQs → score card → weak-topic chips → retry weak questions | "Then a practice quiz straight from my material. Eight out of ten — but more importantly it tells me exactly where I keep slipping: Thevenin's theorem. One tap and it re-tests only my weak topics." |
| **5. Privacy + price** | 1:45–2:10 | Settings screen: privacy toggles, "delete my data", plan page ₹0 free | "My notes stay mine — there's a privacy panel, and I can delete everything in one tap. And it's free to start. Ten questions a day, zero rupees." |
| **6. CTA + outro** | 2:10–2:30 | Glide shareable app link + logo on screen | "Try it with one of your own PDFs — link in the description. Your notes are already your question bank; StudyMate just makes them ask you back." |

**Editing checklist (CapCut/Canva video):** add a countdown caption during the upload wait · caption the quiz score with a pop-up · gentle background music at 20% volume · end card with the link + logo · keep total at **2:00–2:30**.

## 6. Field-by-field explanation (how to redo for your idea)
- **Tool choice** — one sentence of *why* (Glide = fastest clickable app from a spreadsheet). "Because my friend told me" is not an answer.
- **Data source** — a prototype is only as good as its tables; name your tables and their columns before touching the UI.
- **Screens & actions** — every screen maps to a **component** + an **action**. If a screen has no action, it's decoration.
- **Storyboard** — every shot needs: *what's on screen, what you say, how you transition.* 6 shots × ~25 s = the whole video; do not free-style in front of the camera.
- **The demo ≠ the product** — the prototype mocks the AI; the video should *say* it's a prototype and show the vision. Honesty about the mock is a mark of an A-grade demo.

## 7. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Tool comparison + choice justification.
3. Data-source table + screens & actions table.
4. The 6-shot storyboard.
5. Recording/edit checklist (prep → record → edit → publish).
6. Link to your published Glide app + your recorded video (2–3 min).
7. Conclusion: 2 things you'd change after watching your own demo.

## 8. Viva Q&A
1. **Why mock the AI in a prototype?** — A prototype tests *flow and value*, not model quality; wiring a live LLM needs a backend (P08). Mocking isolates design questions from engineering questions.
2. **Glide vs a real app?** — Glide gives you tables, screens, and actions from a spreadsheet in hours — real apps need code, auth, and hosting. Prototype = validation, not production.
3. **What if your demo video exceeds 3 minutes?** — Cut a "show less, say more" pass: one upload, one quiz, one CTA. The 6-shot script is already trimmed to fit.
4. **Why is the storyboard more important than the recording?** — It forces the 2:30 target and the hook; recording without a storyboard produces rambling takes you'll redo.

## 9. Resources
- Glide docs (build your first app): https://www.glideapps.com/docs
- FlutterFlow: https://flutterflow.io · Bubble: https://bubble.io
- CapCut (free video editor): https://www.capcut.com · OBS (if recording on PC): https://obsproject.com
- "How to record a product demo" tips: search *how to record product demo video tips* (Loom/Asana blogs)
- Template file: [`p10_demo_storyboard_template.md`](./p10_demo_storyboard_template.md.md)

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **No Code Prototype Demo Video** in a real environment, it almost never works perfectly the first time. 
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

- **turnkey 2–3 minute demo video** — this write-up gives the shot-by-shot storyboard — *you* record it on your phone and stitch it with CapCut/Canva video.
- **Chosen** — fastest to a clickable demo |
- **Tool choice** — one sentence of *why* (Glide = fastest clickable app from a spreadsheet). "Because my friend told me" is not an answer.
- **Data source** — a prototype is only as good as its tables; name your tables and their columns before touching the UI.
- **Screens & actions** — every screen maps to a **component** + an **action**. If a screen has no action, it's decoration.
- **Storyboard** — every shot needs: *what's on screen, what you say, how you transition.* 6 shots × ~25 s = the whole video; do not free-style in front of the camera.
- **The demo ≠ the product** — the prototype mocks the AI; the video should *say* it's a prototype and show the vision. Honesty about the mock is a mark of an A-grade demo.
- **Why mock the AI in a prototype?** — A prototype tests *flow and value*, not model quality; wiring a live LLM needs a backend (P08). Mocking isolates design questions from engineering questions.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
