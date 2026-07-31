# P04 — User Personas, Empathy Map & Customer Journey Map

**Subject:** AI Product Design | **Unit:** 2 | **Approx. Hrs:** 4
**PrO (verbatim):** *Develop User Persona, Empathy Map, and Customer Journey Map.*

---

## 1. Objective
- Create **2 user personas** for StudyMate (demographics, goals, frustrations).
- Fill an **empathy map** for the primary persona (Says / Thinks / Does / Feels).
- Map the **customer journey** end-to-end with pain points and opportunities at each stage.

## 2. Personas (filled)

### Persona 1 — Riya (primary)

| Field | Value |
|---|---|
| **Name / age / course** | Riya Patel, 19, Diploma IT (Year 2, Semester 4) |
| **Situation** | Lives at home in a mid-size city; studies on a mid-range Android phone + college lab PC; internet is mobile data (limited). |
| **Daily routine** | Classes 9–5, then 2–3 hrs self-study late evening; relies on handwritten notes + WhatsApp groups. |
| **Goals** | Pass semester with 70%+; create revision notes fast; feel prepared before the exam rather than anxious. |
| **Frustrations** | Notes scattered across pages/PDFs; can't self-test quickly; asking doubts in class feels awkward; free YouTube videos are too long. |
| **AI literacy** | Uses ChatGPT occasionally for definitions; never uploaded her own notes; worried about cost and privacy. |
| **Motivator / objection** | Would pay ₹100–200/month **if** it clearly uses *her* material and shows score improvements. |

### Persona 2 — Kunal (secondary)

| Field | Value |
|---|---|
| **Name / age / course** | Kunal Desai, 21, Diploma ME (Year 3) — preparing for placement exams + GTU final sem |
| **Situation** | Has a laptop, is comfortable with apps, follows tech channels; time-poor (project + interviews + exams). |
| **Goals** | Reuse one set of notes for *both* college viva and placement aptitude prep; practise 200+ questions in the last 10 days. |
| **Frustrations** | Old notes are unstructured; making practice papers by hand is slow; resists "one more app" unless it saves real hours. |
| **AI literacy** | High — prompts, browser extensions, knows what an LLM is. |
| **Motivator / objection** | Wants fast output + export (PDF/Anki) over fancy UI; will drop the app if summaries are generic. |

## 3. Empathy Map (filled — for Riya)

| Quadrant | Contents (typed into the map) |
|---|---|
| **👂 Says** (out loud) | *"I have no time to make question papers." · "Which chapter should I even do first?" · "Is this topic in our syllabus or not?"* |
| **💭 Thinks** (inner voice) | *"Everyone else seems prepared. I should have started earlier." · "I can't afford coaching for every subject." · "If I upload my notes, will someone see them?"* |
| **🧩 Does** (actions) | Scrolls WhatsApp notes, re-reads the same pages twice, watches 2-hr YouTube videos, last-minute all-nighters, copies classmates' summaries. |
| **❤️ Feels** (emotions) | Anxious, overwhelmed, a little ashamed ("should have been better"), hopeful when a tool works instantly, distrustful of "AI magic". |

> **Empathy-map reading:** Riya's *thinks ≠ says* (privacy worry + shame). A product that lowers the barrier to first use (one upload, visible "no one else sees this") targets her unspoken fears — that's the design insight the journey map will use.

## 4. Customer Journey Map (filled — for Riya, "first exam-prep session")

| Stage | 1. Discover | 2. Sign-up & first upload | 3. Get summary | 4. Do the quiz | 5. Retain / come back |
|---|---|---|---|---|---|
| **User actions** | Sees Instagram ad / friend's reel → visits landing page | Creates free account, uploads 1 PDF | Waits ~20–30 s, reads 1-page summary | Answers 10 MCQs, sees score + weak-topic tags | Returns before next exam, exports flashcards |
| **Touchpoints** | Instagram, landing page | Sign-up form, upload button | Progress bar, summary screen | Quiz screen, score card | Dashboard, notifications |
| **Thoughts / feelings** | "Is this actually for my syllabus?" / curious | "Why ask for email? Is my file safe?" | "Fast — but is it right? It matched my notes, wow." | "Oh I keep failing unit 4 questions." / motivated to fix | "Saved me hours" / habit forming |
| **Pain points** 🔴 | Generic ads feel scammy; no trust | Doubt about privacy; upload friction on phone | Long wait → closes tab; generic summary | Questions too easy or out of syllabus | Forgets app exists; no reminder |
| **Opportunities** 🟢 | Use a real student's testimonial + "works with GTU syllabus" tagline | "Upload a dummy file to try" sandbox; no-email guest mode | Show "grounded in YOUR notes ✓" badge; show topic list | Adaptive difficulty + "explain why my answer was wrong" | 3-day revision reminder + streak + shareable score card |
| **Owners / metrics** | Marketing / CTR | Product / sign-up → upload % | ML / time-to-summary | Product / quiz completion % | Retention / D7 return rate |

## 5. Blank Templates (copy into `../code/p04_persona_empathy_journey_template.md`)

```
# <Product> — Persona / Empathy / Journey (blank)

## Persona <N> — <Name>
| Field | Value |
| Name / age / course | |
| Situation | |
| Daily routine | |
| Goals | |
| Frustrations | |
| AI literacy | |
| Motivator / objection | |

## Empathy Map — <Persona>
| Quadrant | What they say / think / do / feel |
| Says | |
| Thinks | |
| Does | |
| Feels | |

## Customer Journey — <Scenario>
| Stage | 1. | 2. | 3. | 4. | 5. |
| User actions | | | | | |
| Touchpoints | | | | | |
| Thoughts / feelings | | | | | |
| Pain points 🔴 | | | | | |
| Opportunities 🟢 | | | | | |
| Metrics | | | | | |
```

## 6. Field-by-field explanation (so you can redo it for your idea)

- **Persona ≠ stereotype.** A persona is a *research summary* — each row must trace to a real observation (interview, survey, analytics). In viva: *"Where did Riya come from?"* → "from 5 student interviews + support tickets".
- **Empathy map quadrants:**
  - **Says** — verbatim quotes you actually heard.
  - **Thinks** — what they won't say (fears, self-judgement). This is the *design gold*.
  - **Does** — observable behaviour (what they *actually* do, not what they claim).
  - **Feels** — emotions. If you can't name an emotion, the quadrant is empty — go do research.
- **Journey stages** — always 4–6, from *before the product* (discover) to *after the product* (retain). A journey that starts at the login screen is half a journey.
- **Touchpoints** — where the user meets your product (screen, notification, email, ad).
- **Pain points 🔴 / Opportunities 🟢** — every 🔴 must map to ≥1 🟢 that your product (or a roadmap feature) could fix. Unmatched pain points are missed requirements.
- **Metrics** — one per stage, so the journey is testable (see P06 for how priorities flow from this).

## 7. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Two personas (tables) + one line each on why they differ.
3. Filled empathy map with 3+ entries per quadrant.
4. Customer journey with 5 stages, pain points and opportunities.
5. "Design insight" paragraph: which 2 opportunities would you build first and why (ties to P06 MVP).
6. Conclusion.

## 8. Viva Q&A
1. **Why two personas and not one?** — One misses secondary segments (e.g., Kunal's high-AI-literacy export needs differ from Riya's simplicity needs); two covers the primary revenue + the vocal power-user.
2. **Empathy map vs persona?** — Persona = *who* they are (table); empathy map = *what's inside their head* at a moment (4 quadrants).
3. **What is a "job to be done"?** — The underlying task the user "hires" the product for — Riya "hires" StudyMate to *feel exam-ready*, not to "use a chatbot".
4. **How do pain points become features?** — Each 🔴 is ranked (frequency × intensity × strategic fit) in P06's prioritization matrix; only top ones reach the MVP.

## 9. Resources
- Empathy map guide (NN/g): search *nngroup empathy map*
- Journey mapping guide (NN/g): search *nngroup customer journey map*
- "Personas: why and how" (UXPA / IxDF): https://www.interaction-design.org/literature/topics/personas
- Google People + AI Guidebook (persona patterns for AI products): https://pair.withgoogle.com
- Template file: [`p04_persona_empathy_journey_template.md`](../code/p04_persona_empathy_journey_template.md)
