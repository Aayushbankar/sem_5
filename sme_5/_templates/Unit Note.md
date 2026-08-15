---
subject: <% tp.system.prompt("Subject code (FOB/IOT/AIPE/AIPD/CDCT)") %>
unit: <% tp.system.prompt("Unit number") %>
title: <% tp.file.title.replace(/^Unit \d+ — /, '') %>
weightage: ""
hours:
status: not-started
related_practicals: []
tags: [subject/<% tp.system.prompt("Subject code").toLowerCase() %>, unit/<% tp.system.prompt("Unit number") %>]
created: <% tp.date.now("YYYY-MM-DD") %>
---

# UNIT <% tp.system.prompt("Unit number") %> — <% tp.file.title.replace(/^Unit \d+ — /, '') %>

> **<% tp.system.prompt("Subject code") %>** · **hrs · % weightage**
> **Covers syllabus sections:**
> **Related practicals:**

---

## 🧭 Chapter Roadmap

| # | Concept | Exam importance | Code demo |
|---|---------|-----------------|-----------|
|   |         |                 |           |

### Learning outcomes — after this unit you can:
1.

---

## Content

*(Add unit content here)*

---

## 📝 PYQ Map

| Year | Q# | Question | Marks | Section |
|------|-----|----------|-------|---------|
|      |     |          |       |         |

---

## 🎥 Video Study Guide

| Topic | YouTube search keywords | Best channels |
|---|---|---|
|   |   |   |

---

*Next: [[Unit N+1 — Title]]*
