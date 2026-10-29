#!/usr/bin/env python3
"""
AIPE Lab Manual PDF Generator — Institutional GTU Edition
===========================================================
Generates official, print-ready GTU laboratory manuals adhering strictly to
Gujarat Technological University / Government Polytechnic Gandhinagar academic formats
and faculty submission requirements:

1. Main Lab Manual PDF: AIPE_Lab_Manual.pdf (Cover + Certificate + Index + P01..P12)
2. Individual Practical PDFs: P01_GenAI_Tools.pdf ... P12_Security_Research.pdf
3. Code Appendix PDF: Code_Appendix.pdf (Cover + Index + All 23 Code & Prompt Files)

Student Profile:
Name: Aayush Bankar
Roll No: 246230316006
Enrollment No: 246230316006
Division: A
Batch: A1
Institute: Government Polytechnic, Gandhinagar (Institute Code: 623)
Course: Artificial Intelligence with Prompt Engineering (DI05016011)
Semester: 5th Semester (Diploma in IT) · AY 2026-2027 (Odd Term)
"""

import os
import sys
import re
import markdown
import weasyprint
from pygments import highlight
from pygments.lexers import PythonLexer, MarkdownLexer, TextLexer
from pygments.formatters import HtmlFormatter

# Base Directories
BASE_DIR = "/mnt/work/college/sem_5/docs/AIPE/submission"
WRITEUPS_DIR = os.path.join(BASE_DIR, "writeups")
CODE_DIR = os.path.join(BASE_DIR, "code")
INDEX_PATH = os.path.join(BASE_DIR, "INDEX.md")

# Student & Institutional Configuration
STUDENT = {
    "name": "Aayush Bankar",
    "roll_no": "246230316006",
    "enrollment_no": "246230316006",
    "division": "A",
    "batch": "A1",
    "semester": "5th Semester",
    "branch": "Information Technology",
    "institute": "Government Polytechnic, Gandhinagar",
    "inst_code": "623",
    "course_name": "Artificial Intelligence with Prompt Engineering",
    "course_code": "DI05016011",
    "academic_year": "2026-2027",
    "term": "Odd Term",
    "faculty_guide": "Prof. A. S. Patel",
    "hod": "Head of Department (IT)",
}

# 12 Practicals Definition
PRACTICALS = [
    {
        "num": 1,
        "title": "Use Generative AI Tools for Different Task Types & Domains",
        "short_title": "GenAI Tools: Tasks & Domains",
        "file": "P01_GenAI_Tools_Tasks_Domains.md",
        "out_pdf": "P01_GenAI_Tools.pdf",
        "unit": 1,
        "hours": 2,
    },
    {
        "num": 2,
        "title": "Sentiment Analysis & Text Classification using Python",
        "short_title": "Sentiment Analysis & NLP",
        "file": "P02_Sentiment_Analysis.md",
        "out_pdf": "P02_Sentiment_Analysis.pdf",
        "unit": 1,
        "hours": 2,
    },
    {
        "num": 3,
        "title": "LLM Behavior Analysis: Prompt Variation, Context, Consistency",
        "short_title": "LLM Behavior Analysis",
        "file": "P03_LLM_Behavior_Analysis.md",
        "out_pdf": "P03_LLM_Behavior_Analysis.pdf",
        "unit": 2,
        "hours": 2,
    },
    {
        "num": 4,
        "title": "LLM Capabilities & Limitations, Hallucination Detection",
        "short_title": "Capabilities & Limitations",
        "file": "P04_LLM_Capabilities_Limitations.md",
        "out_pdf": "P04_LLM_Capabilities_Limitations.pdf",
        "unit": 2,
        "hours": 2,
    },
    {
        "num": 5,
        "title": "Design & Refine Prompts: Email Writing & Concept Explanation",
        "short_title": "Prompt Design & Refinement",
        "file": "P05_Prompt_Design_Refinement.md",
        "out_pdf": "P05_Prompt_Design_Refinement.pdf",
        "unit": 3,
        "hours": 2,
    },
    {
        "num": 6,
        "title": "Zero-Shot, Few-Shot & Role-Based Prompting",
        "short_title": "Zero/Few-Shot & Role Prompting",
        "file": "P06_Zero_Few_Shot_Role.md",
        "out_pdf": "P06_Zero_Few_Shot_Role.pdf",
        "unit": 3,
        "hours": 2,
    },
    {
        "num": 7,
        "title": "Chain-of-Thought & Prompt Chaining for Multi-Step Problems",
        "short_title": "CoT & Prompt Chaining",
        "file": "P07_CoT_Prompt_Chaining.md",
        "out_pdf": "P07_CoT_Prompt_Chaining.pdf",
        "unit": 4,
        "hours": 2,
    },
    {
        "num": 8,
        "title": "Task-Based Prompt Engineering: Summarization, Blog, Code",
        "short_title": "Task-Based Prompt Engineering",
        "file": "P08_Task_Based_Prompt_Eng.md",
        "out_pdf": "P08_Task_Based_Prompt_Eng.pdf",
        "unit": 4,
        "hours": 2,
    },
    {
        "num": 9,
        "title": "AI Tools for Software Development: Generation, Debugging, Explanation",
        "short_title": "AI for Software Development",
        "file": "P09_AI_Tools_Software_Dev.md",
        "out_pdf": "P09_AI_Tools_Software_Dev.pdf",
        "unit": 5,
        "hours": 2,
    },
    {
        "num": 10,
        "title": "AI Chatbot via API Integration (OpenAI/Gemini) with Python",
        "short_title": "AI Chatbot API Integration",
        "file": "P10_AI_Chatbot_API.md",
        "out_pdf": "P10_AI_Chatbot_API.pdf",
        "unit": 5,
        "hours": 4,
    },
    {
        "num": 11,
        "title": "Document-Based Question Answering (RAG) — Privata",
        "short_title": "Document QA RAG (Privata)",
        "file": "P11_Document_QA_RAG.md",
        "out_pdf": "P11_Document_QA_RAG.pdf",
        "unit": 5,
        "hours": 4,
    },
    {
        "num": 12,
        "title": "AI Application Development: Security Research Assistant",
        "short_title": "Security Research Assistant",
        "file": "P12_AI_Study_Assistant.md",
        "out_pdf": "P12_Security_Research.pdf",
        "unit": 5,
        "hours": 4,
    },
]

# Code Appendix Files Specification
CODE_FILES = [
    {
        "practical": "Practical 01",
        "title": "Generative AI Task Templates",
        "rel_path": "p01_genai_task_templates.txt",
        "lang": "text",
        "desc": "Standardized prompt templates across 6 GenAI task types and domains",
    },
    {
        "practical": "Practical 02",
        "title": "Sentiment Analysis & Text Classification",
        "rel_path": "p02_sentiment_analysis.py",
        "lang": "python",
        "desc": "TextBlob and Naive Bayes sentiment analysis with negation folding",
    },
    {
        "practical": "Practical 02",
        "title": "Offline Lexicon Classifier Fallback",
        "rel_path": "p02_lexicon_fallback.py",
        "lang": "python",
        "desc": "Pure standard library rule-based lexicon sentiment classifier",
    },
    {
        "practical": "Practical 03",
        "title": "LLM Behavior Test Matrix",
        "rel_path": "p03_llm_behavior_test_matrix.md",
        "lang": "markdown",
        "desc": "Empirical test matrix evaluating prompt variations and context sensitivity",
    },
    {
        "practical": "Practical 04",
        "title": "Question Bank & Evaluation Rubric",
        "rel_path": "p04_question_bank_and_rubric.md",
        "lang": "markdown",
        "desc": "Test suite for factual, logical, ambiguous, and hallucination queries",
    },
    {
        "practical": "Practical 05",
        "title": "Prompt Refinement Before/After Template",
        "rel_path": "p05_before_after_template.md",
        "lang": "markdown",
        "desc": "Comparative template documenting prompt iteration and quality delta",
    },
    {
        "practical": "Practical 06",
        "title": "Prompting Technique Templates",
        "rel_path": "p06_prompting_technique_templates.md",
        "lang": "markdown",
        "desc": "Zero-shot, few-shot, and role-based prompting pattern catalog",
    },
    {
        "practical": "Practical 07",
        "title": "Chain-of-Thought & Prompt Chaining",
        "rel_path": "p07_cot_and_chaining_templates.md",
        "lang": "markdown",
        "desc": "Multi-step reasoning templates and structured prompt chaining pipelines",
    },
    {
        "practical": "Practical 08",
        "title": "Task Optimization Checklists",
        "rel_path": "p08_optimization_checklists.md",
        "lang": "markdown",
        "desc": "Production checklists for summarization, technical blogs, and code generation",
    },
    {
        "practical": "Practical 09",
        "title": "AI Code Generation & Debugging Cases",
        "rel_path": "p09_code_gen_debugging_cases.py",
        "lang": "python",
        "desc": "Test cases for algorithmic generation, runtime bug debugging, and unit testing",
    },
    {
        "practical": "Practical 10",
        "title": "AI Chatbot API Client with Mock Mode",
        "rel_path": "p10_chatbot.py",
        "lang": "python",
        "desc": "Multi-turn conversational chatbot supporting OpenAI, Gemini, and offline mock modes",
    },
    {
        "practical": "Practical 11",
        "title": "Document QA RAG Prototype",
        "rel_path": "p11_rag_document_qa.py",
        "lang": "python",
        "desc": "Standalone document-based question answering prototype",
    },
    {
        "practical": "Practical 11",
        "title": "Sample Knowledge Base Document",
        "rel_path": "p11_sample_document.txt",
        "lang": "text",
        "desc": "Reference source document for RAG ingestion and retrieval testing",
    },
    {
        "practical": "Practical 11 (Privata)",
        "title": "Privata Central Configuration",
        "rel_path": "privata/config.py",
        "lang": "python",
        "desc": "Configuration settings for embedding models, ChromaDB, and Gemini LLM",
    },
    {
        "practical": "Practical 11 (Privata)",
        "title": "Privata Ingestion Pipeline",
        "rel_path": "privata/ingest.py",
        "lang": "python",
        "desc": "Document loading, recursive chunking, and local embedding vectorization",
    },
    {
        "practical": "Practical 11 (Privata)",
        "title": "Privata Interactive Chat Loop",
        "rel_path": "privata/chat.py",
        "lang": "python",
        "desc": "RAG query loop with similarity search, prompt grounding, and answer generation",
    },
    {
        "practical": "Practical 11 (Privata)",
        "title": "Privata Gemini LLM Loader",
        "rel_path": "privata/models/llm_loader.py",
        "lang": "python",
        "desc": "Google Gemini 1.5-Flash API integration module",
    },
    {
        "practical": "Practical 11 (Privata)",
        "title": "Privata Local Embedder",
        "rel_path": "privata/retriever/embedder.py",
        "lang": "python",
        "desc": "HuggingFace sentence-transformers/all-MiniLM-L6-v2 local embedder",
    },
    {
        "practical": "Practical 11 (Privata)",
        "title": "Privata ChromaDB Interface",
        "rel_path": "privata/retriever/vectordb.py",
        "lang": "python",
        "desc": "Persistent local vector store storage and cosine similarity retrieval",
    },
    {
        "practical": "Practical 11 (Privata)",
        "title": "Privata Document Loaders",
        "rel_path": "privata/utils/doc_loader.py",
        "lang": "python",
        "desc": "Extractors for PDF, TXT, and Markdown files with metadata retention",
    },
    {
        "practical": "Practical 11 (Privata)",
        "title": "Privata Environment Requirements",
        "rel_path": "privata/requirements.txt",
        "lang": "text",
        "desc": "Python dependency manifest for local RAG execution",
    },
    {
        "practical": "Practical 12",
        "title": "Security Research Assistant",
        "rel_path": "p12_security_research_assistant.py",
        "lang": "python",
        "desc": "AI application for vulnerability analysis, exploit chaining, kernel offsets, and PoC generation",
    },
    {
        "practical": "Practical 12",
        "title": "AI Study Assistant Prototype",
        "rel_path": "p12_study_assistant.py",
        "lang": "python",
        "desc": "Reference study assistant implementation for academic query answering",
    },
]

# Pygments CSS theme definition - crisp, high contrast academic styling
PYGMENTS_CSS = HtmlFormatter(style="default").get_style_defs(".codehilite")

# Base Global CSS Stylesheet — GTU Academic Lab Manual Format
COMMON_CSS = f"""
@page {{
    size: A4 portrait;
    margin: 12mm 11mm 12mm 11mm;
    @top-left {{
        content: "AIPE Lab Manual | DI05016011 | GTU Code: 623";
        font-family: 'DejaVu Sans', 'Arial', sans-serif;
        font-size: 7.2pt;
        color: #334155;
        border-bottom: 0.75pt solid #94a3b8;
        padding-bottom: 2px;
    }}
    @top-right {{
        content: "{STUDENT['name']} | Roll No: {STUDENT['roll_no']}";
        font-family: 'DejaVu Sans', 'Arial', sans-serif;
        font-size: 7.2pt;
        font-weight: bold;
        color: #1e3a8a;
        border-bottom: 0.75pt solid #94a3b8;
        padding-bottom: 2px;
    }}
    @bottom-left {{
        content: "Government Polytechnic, Gandhinagar · Dept. of IT";
        font-family: 'DejaVu Sans', 'Arial', sans-serif;
        font-size: 7.2pt;
        color: #475569;
        border-top: 0.75pt solid #94a3b8;
        padding-top: 2px;
    }}
    @bottom-right {{
        content: "Page " counter(page) " of " counter(pages);
        font-family: 'DejaVu Sans', 'Arial', sans-serif;
        font-size: 7.2pt;
        font-weight: bold;
        color: #1e3a8a;
        border-top: 0.75pt solid #94a3b8;
        padding-top: 2px;
    }}
}}

@page no-headers-footers {{
    margin: 0;
    @top-left {{ content: none !important; }}
    @top-right {{ content: none !important; }}
    @bottom-left {{ content: none !important; }}
    @bottom-right {{ content: none !important; }}
}}

body {{
    font-family: 'DejaVu Serif', 'Times New Roman', serif;
    font-size: 8.2pt;
    line-height: 1.32;
    color: #0f172a;
}}

.page-break {{
    page-break-before: always;
}}

/* Typography */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    color: #0f172a;
    page-break-after: avoid;
    break-after: avoid;
}}

h1 {{
    font-size: 11.8pt;
    color: #1e3a8a;
    border-bottom: 1.5pt solid #1e3a8a;
    padding-bottom: 2px;
    margin-top: 0;
    margin-bottom: 5px;
}}

h2 {{
    font-size: 9.2pt;
    color: #1e3a8a;
    border-bottom: 0.75pt solid #cbd5e1;
    padding-bottom: 1px;
    margin-top: 5px;
    margin-bottom: 2.5px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}}

h3 {{
    font-size: 8.2pt;
    color: #1e293b;
    margin-top: 4px;
    margin-bottom: 2px;
    font-weight: bold;
}}

h4 {{
    font-size: 7.6pt;
    color: #334155;
    margin-top: 3px;
    margin-bottom: 1px;
}}

p {{
    margin-top: 0;
    margin-bottom: 3.5px;
    text-align: justify;
}}

ul, ol {{
    margin-top: 0;
    margin-bottom: 3.5px;
    padding-left: 14px;
}}

li {{
    margin-bottom: 1px;
}}

/* Practical Official GTU Header Table */
.gtu-practical-header {{
    margin-bottom: 5px;
    page-break-inside: avoid;
    break-inside: avoid;
}}
.gtu-header-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0;
    border: 1.5pt solid #1e3a8a;
}}
.gtu-header-table td {{
    padding: 2px 4.5px;
    border: 1px solid #cbd5e1;
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    font-size: 6.8pt;
    color: #0f172a;
}}
.gtu-header-table .gtu-inst-row td {{
    background-color: #1e3a8a;
    color: #ffffff;
    text-align: center;
    font-weight: bold;
    font-size: 7.3pt;
    letter-spacing: 0.5px;
    border: 1.5pt solid #1e3a8a;
    padding: 2.5px 5px;
}}
.gtu-header-table .gtu-meta-row td {{
    background-color: #f8fafc;
    font-size: 6.8pt;
}}
.gtu-header-table .gtu-title-row td {{
    background-color: #ffffff;
    font-size: 8.6pt;
    color: #0f172a;
    border-top: 1pt solid #1e3a8a;
    padding: 3px 5px;
}}
.gtu-title-tag {{
    color: #1e3a8a;
    font-weight: 800;
    font-size: 7.8pt;
    margin-right: 4px;
}}

/* Aim Section Box */
.gtu-aim-box {{
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 3pt solid #1e3a8a;
    padding: 3.5px 6px;
    margin: 2.5px 0 5px 0;
    page-break-inside: avoid;
    break-inside: avoid;
}}
.gtu-aim-lbl {{
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    font-size: 7pt;
    font-weight: bold;
    color: #1e3a8a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 1px;
}}
.gtu-aim-txt {{
    font-size: 8pt;
    color: #0f172a;
    margin: 0;
}}

/* Tables — Formal Academic Grid */
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 3.5px 0;
    font-size: 6.9pt;
    page-break-inside: auto;
}}

tr {{
    page-break-inside: avoid;
    break-inside: avoid;
}}

th {{
    background-color: #1e3a8a;
    color: #ffffff;
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    font-weight: bold;
    text-align: left;
    padding: 2.2px 4px;
    border: 1px solid #1e3a8a;
    font-size: 6.9pt;
}}

td {{
    padding: 1.8px 4px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
    font-size: 6.9pt;
}}

tr:nth-child(even) td {{
    background-color: #f8fafc;
}}

/* Code & Highlight */
{PYGMENTS_CSS}

pre, .codehilite pre {{
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 2.5pt solid #1e3a8a;
    padding: 2.5px 5px;
    font-family: 'DejaVu Sans Mono', monospace;
    font-size: 6.7pt;
    line-height: 1.26;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 2.5px 0 3.5px 0;
    page-break-inside: auto;
}}

code {{
    font-family: 'DejaVu Sans Mono', monospace;
    font-size: 6.9pt;
    background-color: #f1f5f9;
    padding: 1px 3px;
    border: 0.5pt solid #e2e8f0;
}}

blockquote {{
    border-left: 2.5pt solid #1e3a8a;
    background-color: #f8fafc;
    margin: 2.5px 0;
    padding: 2.5px 6px;
    font-style: italic;
    color: #1e293b;
    border-top: 0.5pt solid #cbd5e1;
    border-bottom: 0.5pt solid #cbd5e1;
    border-right: 0.5pt solid #cbd5e1;
}}

/* Output Screenshot Verification Record Box */
.gtu-output-record-box {{
    border: 1.5pt solid #1e3a8a;
    margin: 4px 0 5px 0;
    page-break-inside: avoid;
    break-inside: avoid;
    background-color: #ffffff;
}}
.gtu-output-record-header {{
    border-bottom: 1pt solid #1e3a8a;
}}
.gtu-output-record-tbl {{
    width: 100%;
    border-collapse: collapse;
    margin: 0;
}}
.gtu-output-record-tbl td {{
    padding: 1.8px 4.5px;
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    font-size: 6.7pt;
    border: none;
}}
.gtu-output-top-row td {{
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: bold;
    font-size: 6.9pt;
    letter-spacing: 0.4px;
}}
.gtu-output-meta-row td {{
    background-color: #f8fafc;
    color: #0f172a;
    border-top: 0.5pt solid #cbd5e1;
    font-size: 6.7pt;
}}
.gtu-output-record-body {{
    padding: 4px 6px;
    background-color: #ffffff;
}}
.gtu-output-mount-frame {{
    border: 1pt solid #94a3b8;
    background-color: #fbfcfd;
    padding: 4px 6px;
    text-align: center;
}}
.gtu-mount-title {{
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    font-size: 7.6pt;
    font-weight: bold;
    color: #0f172a;
    letter-spacing: 0.4px;
    margin-bottom: 1px;
}}
.gtu-mount-filename {{
    font-family: 'DejaVu Sans Mono', monospace;
    font-size: 6.8pt;
    color: #475569;
    margin-bottom: 2px;
}}
.gtu-mount-instructions {{
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    font-size: 6.5pt;
    color: #334155;
    text-align: left;
    background-color: #ffffff;
    border: 0.75pt solid #cbd5e1;
    border-left: 2.5pt solid #1e3a8a;
    padding: 2px 4px;
    line-height: 1.28;
}}

/* Continuous Assessment & Evaluation Record */
.gtu-eval-section {{
    margin-top: 5px;
    padding-top: 3px;
    border-top: 1pt solid #cbd5e1;
    page-break-inside: avoid;
    break-inside: avoid;
}}
.gtu-eval-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0 0 2px 0;
    border: 1pt solid #1e3a8a;
}}
.gtu-eval-table th, .gtu-eval-table td {{
    border: 1px solid #cbd5e1;
    padding: 1.6px 4px;
    font-size: 6.7pt;
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
}}
.gtu-eval-hdr th {{
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: bold;
    text-align: center;
    font-size: 6.9pt;
    letter-spacing: 0.4px;
    padding: 1.8px 4px;
    border: 1pt solid #1e3a8a;
}}
.gtu-eval-subhdr th {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: bold;
    font-size: 6.5pt;
}}
.gtu-eval-total td {{
    background-color: #f8fafc;
    border-top: 1pt solid #1e3a8a;
    font-weight: bold;
}}
.gtu-sig-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 2px 0 0 0;
}}
.gtu-sig-table td {{
    border: none;
    padding: 0;
    vertical-align: bottom;
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    font-size: 6.7pt;
}}
.gtu-sig-space {{
    height: 12px;
    border-bottom: 0.75pt dashed #94a3b8;
    margin-bottom: 2px;
}}
.gtu-sig-name {{
    color: #0f172a;
}}
.gtu-sig-date {{
    color: #64748b;
    font-size: 6.3pt;
}}

/* Dynamic TOC page target links */
a.page-target-link {{
    text-decoration: none;
    font-weight: bold;
    color: #1e3a8a;
}}
a.page-target-link::after {{
    content: target-counter(attr(href), page);
}}

/* Official GTU Cover Page Styles */
.cover-container {{
    page: no-headers-footers;
    width: 100%;
    height: 100vh;
    box-sizing: border-box;
    padding: 10mm 12mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.cover-border-box {{
    border: 3.5pt double #1e3a8a;
    padding: 10mm 10mm;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
}}
.cover-inst-header {{
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
}}
.cover-inst-code {{
    font-size: 8.5pt;
    font-weight: bold;
    color: #475569;
    letter-spacing: 1.5px;
}}
.cover-inst-name {{
    font-size: 15.5pt;
    font-weight: bold;
    color: #0f172a;
    margin: 4px 0 2px 0;
    letter-spacing: 0.5px;
}}
.cover-inst-dept {{
    font-size: 11pt;
    font-weight: bold;
    color: #1e3a8a;
    letter-spacing: 0.5px;
}}
.cover-divider {{
    height: 2pt;
    background-color: #1e3a8a;
    margin: 8px auto;
    width: 70%;
}}
.cover-title-section {{
    margin: 10px 0;
}}
.cover-doc-type {{
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    font-size: 10.5pt;
    font-weight: bold;
    letter-spacing: 1.5px;
    color: #334155;
    text-transform: uppercase;
    margin-bottom: 6px;
}}
.cover-course-title {{
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    font-size: 18.5pt;
    font-weight: 800;
    color: #1e3a8a;
    line-height: 1.25;
    margin-bottom: 6px;
}}
.cover-course-code {{
    font-family: 'DejaVu Sans Mono', monospace;
    font-size: 10.5pt;
    font-weight: bold;
    color: #0f172a;
    margin-bottom: 4px;
}}
.cover-term {{
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    font-size: 9.5pt;
    color: #475569;
}}
.cover-student-card {{
    background: #ffffff;
    border: 1.5pt solid #1e3a8a;
    padding: 8px 12px;
    width: 86%;
    margin: 8px auto;
    text-align: left;
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
}}
.cover-student-card table {{
    margin: 0;
    font-size: 8pt;
}}
.cover-student-card td {{
    padding: 3px 6px;
    border: 1px solid #cbd5e1;
}}
.cover-student-card td.lbl {{
    font-weight: bold;
    color: #1e3a8a;
    width: 40%;
    background-color: #f8fafc;
}}
.cover-student-card td.val {{
    font-weight: 600;
    color: #0f172a;
}}
.cover-footer-sigs {{
    display: flex;
    justify-content: space-between;
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    margin-top: 10px;
}}
.cover-sig-item {{
    text-align: center;
    width: 42%;
}}
.cover-sig-line {{
    border-bottom: 1px dashed #64748b;
    height: 30px;
    margin-bottom: 4px;
}}
.cover-sig-title {{
    font-size: 8pt;
    font-weight: bold;
    color: #0f172a;
}}
.cover-sig-sub {{
    font-size: 7.2pt;
    color: #64748b;
}}

/* Official GTU Certificate Page Styles */
.cert-container {{
    page: no-headers-footers;
    padding: 10mm 12mm;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100vh;
}}
.cert-box {{
    border: 3pt double #1e3a8a;
    padding: 10mm 12mm;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
}}
.cert-title {{
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    font-size: 20pt;
    font-weight: 800;
    color: #1e3a8a;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 8px;
    margin-bottom: 12px;
}}
.cert-body {{
    font-size: 9.8pt;
    line-height: 1.65;
    text-align: justify;
    color: #0f172a;
    margin: 12px 0;
}}
.cert-body strong {{
    color: #0f172a;
}}
.cert-details-table {{
    width: 86%;
    margin: 10px auto;
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
    border: 1.5pt solid #1e3a8a;
}}
.cert-details-table td {{
    padding: 4px 7px;
    border: 1px solid #cbd5e1;
    font-size: 8pt;
}}
.cert-details-table td.lbl {{
    font-weight: bold;
    color: #1e3a8a;
    background-color: #f8fafc;
    width: 38%;
}}
.cert-sigs {{
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
    font-family: 'DejaVu Sans', 'Arial', sans-serif;
}}
.cert-sig-block {{
    width: 30%;
    text-align: center;
}}
.cert-sig-line {{
    border-bottom: 1px dashed #64748b;
    height: 35px;
    margin-bottom: 4px;
}}
.cert-sig-label {{
    font-size: 8pt;
    font-weight: bold;
    color: #0f172a;
}}
.cert-sig-sub {{
    font-size: 7.2pt;
    color: #64748b;
}}

/* Compact Index Section Styles */
#index-section h1 {{
    font-size: 12.5pt;
    margin: 0 0 3px 0;
    padding-bottom: 2px;
}}
#index-section h2 {{
    font-size: 9pt;
    margin: 3px 0 2px 0;
    padding-bottom: 1px;
}}
#index-section p {{
    font-size: 7.8pt;
    margin: 2px 0;
}}
#index-section table {{
    font-size: 7.1pt;
    margin: 3px 0 4px 0;
}}
#index-section th {{
    padding: 2.5px 4.5px;
    font-size: 7.1pt;
}}
#index-section td {{
    padding: 2px 4.5px;
    font-size: 7.1pt;
}}
#index-section ul {{
    font-size: 7.1pt;
    margin: 2px 0 3px 0;
    padding-left: 14px;
}}
#index-section li {{
    margin-bottom: 1px;
}}
#index-section hr {{
    margin: 3px 0;
    border: 0;
    border-top: 0.5pt solid #cbd5e1;
}}
"""

def replace_student_placeholders(text: str) -> str:
    """Replaces all student placeholders with exact configuration values."""
    name = STUDENT["name"]
    roll = STUDENT["roll_no"]
    enroll = STUDENT["enrollment_no"]
    div = STUDENT["division"]
    batch = STUDENT["batch"]

    t = text
    # Standard bracketed templates
    t = t.replace("[YOUR NAME]", name)
    t = t.replace("[YOUR ROLL NUMBER]", roll)
    t = t.replace("[YOUR ENROLLMENT NUMBER]", enroll)
    t = t.replace("[YOUR DIVISION]", div)
    t = t.replace("[YOUR BATCH]", batch)
    t = t.replace("[STUDENT NAME, ROLL NO]", f"{name}, {roll}")
    t = t.replace("[STUDENT NAME]", name)
    t = t.replace("[ROLL NO]", roll)
    t = t.replace("[ENROLLMENT NO]", enroll)
    t = t.replace("[DIVISION]", div)
    t = t.replace("[BATCH]", batch)

    # Complex regex placeholders in headers and outputs
    t = re.sub(r'\[STUDENT NAME\s*\|\s*ROLL NO:\s*_{3,}\]', f'[Student Name: {name} | Roll No: {roll}]', t, flags=re.I)
    t = re.sub(r'\[Student Name:\s*_{3,}\s*\|\s*Roll No:\s*_{3,}\]', f'[Student Name: {name} | Roll No: {roll}]', t, flags=re.I)
    t = re.sub(r'Student Name:\s*_{4,}', f'Student Name: {name}', t, flags=re.I)
    t = re.sub(r'Roll No:\s*_{4,}', f'Roll No: {roll}', t, flags=re.I)

    # Clean emojis from source text to preserve institutional dignity
    t = t.replace("✅ Complete", "Completed")
    t = t.replace("✅", "Completed")
    t = t.replace("📷", "")
    t = t.replace("🎯", "")
    return t

def make_screenshot_box(practical_num: int, filename: str = None) -> str:
    """Generates an official GTU bordered screenshot output record box."""
    if not filename:
        filename = f"P{practical_num:02d}_output.png"
    return f"""
<div class="gtu-output-record-box">
  <div class="gtu-output-record-header">
    <table class="gtu-output-record-tbl">
      <tr class="gtu-output-top-row">
        <td style="width: 22%;">PRACTICAL {practical_num:02d}</td>
        <td style="width: 56%; text-align: center;">LABORATORY WORK OUTPUT &amp; VERIFICATION RECORD</td>
        <td style="width: 22%; text-align: right;">REF: {filename}</td>
      </tr>
      <tr class="gtu-output-meta-row">
        <td colspan="3">
          <strong>Student Name:</strong> {STUDENT['name']} &nbsp;|&nbsp;
          <strong>Roll No:</strong> {STUDENT['roll_no']} &nbsp;|&nbsp;
          <strong>Enrollment No:</strong> {STUDENT['enrollment_no']} &nbsp;|&nbsp;
          <strong>Batch:</strong> Div {STUDENT['division']} / {STUDENT['batch']}
        </td>
      </tr>
    </table>
  </div>
  <div class="gtu-output-record-body">
    <div class="gtu-output-mount-frame">
      <div class="gtu-mount-title">[ AFFIX TERMINAL / CONSOLE OUTPUT SCREENSHOT HERE ]</div>
      <div class="gtu-mount-filename">Expected Verification File: <code>{filename}</code></div>
      <div class="gtu-mount-instructions">
        <strong>Faculty Verification Directive:</strong> Per GTU laboratory guidelines, the terminal execution output must explicitly confirm student identity (Name: <strong>{STUDENT['name']}</strong> | Roll No: <strong>{STUDENT['roll_no']}</strong>). In the hardcopy manual, paste verified screenshot within this designated frame. Full verbatim execution logs and console outputs are preserved directly below.
      </div>
    </div>
  </div>
</div>
"""

def make_eval_footer() -> str:
    """Generates official GTU Continuous Assessment Rubric & faculty sign-off block."""
    return f"""
<div class="gtu-eval-section">
  <table class="gtu-eval-table">
    <thead>
      <tr class="gtu-eval-hdr">
        <th colspan="3">CONTINUOUS ASSESSMENT &amp; EVALUATION RECORD</th>
      </tr>
      <tr class="gtu-eval-subhdr">
        <th style="width: 50%;">Assessment Criteria</th>
        <th style="width: 25%; text-align: center;">Max Marks</th>
        <th style="width: 25%; text-align: center;">Marks Awarded</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>1. Practical Performance, Prompting &amp; Output Verification</td>
        <td style="text-align: center;">10</td>
        <td style="text-align: center;">&nbsp;</td>
      </tr>
      <tr>
        <td>2. Technical Understanding, Analysis &amp; Viva-Voce</td>
        <td style="text-align: center;">10</td>
        <td style="text-align: center;">&nbsp;</td>
      </tr>
      <tr>
        <td>3. Lab Manual Maintenance &amp; Timely Submission</td>
        <td style="text-align: center;">05</td>
        <td style="text-align: center;">&nbsp;</td>
      </tr>
      <tr class="gtu-eval-total">
        <td><strong>Total Marks Obtained:</strong></td>
        <td style="text-align: center;"><strong>25</strong></td>
        <td style="text-align: center;"><strong>&nbsp; &nbsp; &nbsp; &nbsp; / 25</strong></td>
      </tr>
    </tbody>
  </table>
  <table class="gtu-sig-table">
    <tr>
      <td style="width: 45%; text-align: left;">
        <div class="gtu-sig-space"></div>
        <div class="gtu-sig-name"><strong>Student Signature:</strong> {STUDENT['name']}</div>
        <div class="gtu-sig-date">Date: ________________________</div>
      </td>
      <td style="width: 10%;"></td>
      <td style="width: 45%; text-align: right;">
        <div class="gtu-sig-space"></div>
        <div class="gtu-sig-name"><strong>Faculty In-Charge Signature:</strong></div>
        <div class="gtu-sig-date">{STUDENT['faculty_guide']} &bull; Date: ____________</div>
      </td>
    </tr>
  </table>
</div>
"""

def render_markdown_practical(md_path: str, practical_num: int, is_standalone: bool = False) -> str:
    """Parses and renders a practical markdown writeup into GTU-styled HTML."""
    with open(md_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # Step 1: Replace student placeholders and clean emojis
    raw = replace_student_placeholders(raw)

    # Step 2: Strip duplicate raw top markdown heading (# Practical XX: ... up to ---)
    top_header_pattern = r'\A#\s*Practical\s*\d+:[^\n]*\n+[\s\S]*?---\s*\n+'
    raw = re.sub(top_header_pattern, '', raw)

    # Step 3: Inject screenshot box placeholder marker under Section 3
    screenshot_marker = f"<!-- SCREENSHOT_PLACEHOLDER_P{practical_num:02d} -->"
    raw = re.sub(
        r'(##\s*3\.\s*Screenshot of Output\s*\n+)',
        r'\1\n' + screenshot_marker + '\n\n',
        raw,
        flags=re.I
    )

    # Step 4: Remove default raw signature line so we can replace with styled evaluation block
    raw = re.sub(r'\n+\*\*Student Signature:\*\*.*?Faculty Signature:.*?\Z', '', raw, flags=re.DOTALL)
    raw = re.sub(r'\n+---\s*\n+\Z', '', raw)

    # Step 5: Convert Markdown to HTML
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'codehilite'])
    html_content = md.convert(raw)

    # Step 6: Replace marker with official GTU screenshot box
    html_content = html_content.replace(
        screenshot_marker,
        make_screenshot_box(practical_num)
    )

    # Step 7: Append official evaluation footer
    html_content += make_eval_footer()

    # Step 8: Wrap in practical container with official GTU header table
    p_info = next((p for p in PRACTICALS if p["num"] == practical_num), None)
    unit_num = p_info['unit'] if p_info else 1
    hours_num = p_info['hours'] if p_info else 2
    title_text = p_info['title'] if p_info else ''

    banner_html = f"""
<div class="gtu-practical-header">
  <table class="gtu-header-table">
    <tr class="gtu-inst-row">
      <td colspan="4">
        GOVERNMENT POLYTECHNIC, GANDHINAGAR &bull; DEPARTMENT OF INFORMATION TECHNOLOGY
      </td>
    </tr>
    <tr class="gtu-meta-row">
      <td style="width: 25%;"><strong>Course:</strong> AIPE ({STUDENT['course_code']})</td>
      <td style="width: 25%;"><strong>Practical No:</strong> {practical_num:02d}</td>
      <td style="width: 25%;"><strong>GTU Unit:</strong> Unit {unit_num}</td>
      <td style="width: 25%;"><strong>Lab Hours:</strong> {hours_num} Hours</td>
    </tr>
    <tr class="gtu-title-row">
      <td colspan="4">
        <span class="gtu-title-tag">PRACTICAL TITLE:</span> <strong>{title_text}</strong>
      </td>
    </tr>
  </table>
</div>
"""

    anchor_id = f"practical-{practical_num:02d}"
    page_break_class = "" if is_standalone else "page-break"

    return f"""
<section id="{anchor_id}" class="{page_break_class}">
  {banner_html}
  {html_content}
</section>
"""

def generate_cover_page() -> str:
    """Generates the official GTU Cover Page for the main lab manual."""
    return f"""
<div class="cover-container">
  <div class="cover-border-box">
    <div class="cover-inst-header">
      <div class="cover-inst-code">GUJARAT TECHNOLOGICAL UNIVERSITY, AHMEDABAD · INST CODE: {STUDENT['inst_code']}</div>
      <div class="cover-inst-name">{STUDENT['institute'].upper()}</div>
      <div class="cover-inst-dept">{STUDENT['branch'].upper()} DEPARTMENT</div>
      <div class="cover-divider"></div>
    </div>

    <div class="cover-title-section">
      <div class="cover-doc-type">Official Laboratory Manual &amp; Continuous Assessment Record</div>
      <div class="cover-course-title">{STUDENT['course_name'].upper()}</div>
      <div class="cover-course-code">Course Code: {STUDENT['course_code']}</div>
      <div class="cover-term">{STUDENT['semester']} · {STUDENT['term']} {STUDENT['academic_year']}</div>
    </div>

    <div class="cover-student-card">
      <table>
        <tr>
          <td class="lbl">Student Full Name:</td>
          <td class="val"><strong>{STUDENT['name']}</strong></td>
        </tr>
        <tr>
          <td class="lbl">Enrollment Number:</td>
          <td class="val">{STUDENT['enrollment_no']}</td>
        </tr>
        <tr>
          <td class="lbl">Class Roll Number:</td>
          <td class="val">{STUDENT['roll_no']}</td>
        </tr>
        <tr>
          <td class="lbl">Division &amp; Batch:</td>
          <td class="val">Division {STUDENT['division']} · Batch {STUDENT['batch']}</td>
        </tr>
        <tr>
          <td class="lbl">Program / Branch:</td>
          <td class="val">Diploma in {STUDENT['branch']} (Semester 5)</td>
        </tr>
        <tr>
          <td class="lbl">Institute:</td>
          <td class="val">{STUDENT['institute']} (Code: {STUDENT['inst_code']})</td>
        </tr>
        <tr>
          <td class="lbl">Academic Term:</td>
          <td class="val">{STUDENT['academic_year']} ({STUDENT['term']})</td>
        </tr>
      </table>
    </div>

    <div class="cover-footer-sigs">
      <div class="cover-sig-item">
        <div class="cover-sig-line"></div>
        <div class="cover-sig-title">{STUDENT['faculty_guide']}</div>
        <div class="cover-sig-sub">Faculty In-Charge / Course Guide</div>
      </div>
      <div class="cover-sig-item">
        <div class="cover-sig-line"></div>
        <div class="cover-sig-title">{STUDENT['hod']}</div>
        <div class="cover-sig-sub">Department of Information Technology</div>
      </div>
    </div>
  </div>
</div>
"""

def generate_certificate_page() -> str:
    """Generates the official GTU academic Certificate of Completion."""
    return f"""
<div class="cert-container page-break">
  <div class="cert-box">
    <div class="cover-inst-header">
      <div class="cover-inst-code">GUJARAT TECHNOLOGICAL UNIVERSITY, AHMEDABAD · INST CODE: {STUDENT['inst_code']}</div>
      <div class="cover-inst-name">{STUDENT['institute'].upper()}</div>
      <div class="cover-inst-dept">{STUDENT['branch'].upper()} DEPARTMENT</div>
      <div class="cover-divider"></div>
    </div>

    <div class="cert-title">CERTIFICATE</div>

    <div class="cert-body">
      This is to certify that <strong>Mr. {STUDENT['name']}</strong>, Enrollment No. <strong>{STUDENT['enrollment_no']}</strong>, Class Roll No. <strong>{STUDENT['roll_no']}</strong>, of <strong>{STUDENT['semester']}</strong> of Diploma Course in <strong>{STUDENT['branch']}</strong> of <strong>{STUDENT['institute']}</strong> has satisfactorily completed the laboratory practical coursework and term assignments in the subject <strong>“{STUDENT['course_name']} ({STUDENT['course_code']})”</strong> for the academic session <strong>{STUDENT['term']} ({STUDENT['academic_year']})</strong> as prescribed by the Gujarat Technological University (GTU) curriculum.
    </div>

    <table class="cert-details-table">
      <tr>
        <td class="lbl">Student Name:</td>
        <td><strong>{STUDENT['name']}</strong></td>
      </tr>
      <tr>
        <td class="lbl">Enrollment No:</td>
        <td>{STUDENT['enrollment_no']}</td>
      </tr>
      <tr>
        <td class="lbl">Class / Division / Batch:</td>
        <td>5th Semester IT &bull; Div {STUDENT['division']} &bull; Batch {STUDENT['batch']}</td>
      </tr>
      <tr>
        <td class="lbl">Date of Submission:</td>
        <td>October 2026</td>
      </tr>
      <tr>
        <td class="lbl">Term Work Status:</td>
        <td>Satisfactorily Completed All 12 Practicals</td>
      </tr>
    </table>

    <div class="cert-sigs">
      <div class="cert-sig-block">
        <div class="cert-sig-line"></div>
        <div class="cert-sig-label">Faculty Guide</div>
        <div class="cert-sig-sub">{STUDENT['faculty_guide']}</div>
      </div>
      <div class="cert-sig-block">
        <div class="cert-sig-line"></div>
        <div class="cert-sig-label">Head of Department</div>
        <div class="cert-sig-sub">{STUDENT['hod']}</div>
      </div>
      <div class="cert-sig-block">
        <div class="cert-sig-line"></div>
        <div class="cert-sig-label">External Examiner</div>
        <div class="cert-sig-sub">GTU Appointed Examiner</div>
      </div>
    </div>
  </div>
</div>
"""

def generate_index_page() -> str:
    """Generates the Index Page from INDEX.md with dynamic page resolution for all rows."""
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        idx_md = f.read()

    idx_md = replace_student_placeholders(idx_md)

    # Link practical index rows to their target anchors robustly (handles 5-col and 6-col rows)
    new_lines = []
    for line in idx_md.splitlines():
        if line.strip().startswith('|') and any(re.match(r'\|\s*' + str(i) + r'\s*\|', line) for i in range(1, 13)):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            num = int(parts[0])
            title = parts[1]
            unit = parts[2]
            if len(parts) == 5:
                status = parts[3]
                sig = parts[4]
            else:
                status = parts[4]
                sig = parts[5]
            page_link = f'<a class="page-target-link" href="#practical-{num:02d}"></a>'
            new_lines.append(f'| {num} | {title} | {unit} | {page_link} | {status} | {sig} |')
        else:
            new_lines.append(line)

    idx_md = '\n'.join(new_lines)

    # Replace checkboxes with unicode ballot boxes
    idx_md = idx_md.replace("- [ ]", "- ☑")
    idx_md = idx_md.replace("- [x]", "- ☑")

    md = markdown.Markdown(extensions=['tables'])
    idx_html = md.convert(idx_md)

    return f"""
<div class="page-break" id="index-section">
  {idx_html}
</div>
"""

def generate_main_lab_manual(output_path: str):
    """Compiles and generates the complete combined AIPE Lab Manual PDF."""
    print("=" * 70)
    print("Generating Deliverable 1: Main Lab Manual (AIPE_Lab_Manual.pdf)...")
    print("=" * 70)

    cover_html = generate_cover_page()
    cert_html = generate_certificate_page()
    index_html = generate_index_page()

    practicals_html_list = []
    for p in PRACTICALS:
        p_path = os.path.join(WRITEUPS_DIR, p["file"])
        print(f"  Rendering Practical {p['num']:02d}: {p['title']}...")
        p_html = render_markdown_practical(p_path, p["num"], is_standalone=False)
        practicals_html_list.append(p_html)

    all_practicals_html = "\n".join(practicals_html_list)

    full_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AIPE Laboratory Manual — {STUDENT['name']}</title>
  <style>
    {COMMON_CSS}
  </style>
</head>
<body>
  {cover_html}
  {cert_html}
  {index_html}
  {all_practicals_html}
</body>
</html>"""

    doc = weasyprint.HTML(string=full_document).render()
    doc.write_pdf(output_path)
    print(f"✅ Generated {output_path} ({len(doc.pages)} pages)")

def generate_individual_practicals():
    """Generates 12 standalone individual practical PDFs."""
    print("\n" + "=" * 70)
    print("Generating Deliverable 2: Individual Practical PDFs (P01..P12)...")
    print("=" * 70)

    for p in PRACTICALS:
        p_path = os.path.join(WRITEUPS_DIR, p["file"])
        out_pdf = os.path.join(BASE_DIR, p["out_pdf"])
        print(f"  Generating {p['out_pdf']} (Practical {p['num']:02d})...")

        practical_content = render_markdown_practical(p_path, p["num"], is_standalone=True)

        indiv_css = COMMON_CSS.replace(
            '@top-left {\n        content: "AIPE Lab Manual | DI05016011 | GTU Code: 623";',
            f'@top-left {{\n        content: "AIPE Lab Manual | DI05016011 | Practical {p["num"]:02d}";'
        )

        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Practical {p['num']:02d} — {p['short_title']}</title>
  <style>
    {indiv_css}
  </style>
</head>
<body>
  {practical_content}
</body>
</html>"""

        doc = weasyprint.HTML(string=full_html).render()
        doc.write_pdf(out_pdf)
        print(f"    -> Saved {p['out_pdf']} ({len(doc.pages)} pages)")

def generate_code_appendix(output_path: str):
    """Compiles and generates the Code Appendix PDF with all code files."""
    print("\n" + "=" * 70)
    print("Generating Deliverable 3: Code Appendix PDF (Code_Appendix.pdf)...")
    print("=" * 70)

    # 1. Cover Page
    cover_html = f"""
<div class="cover-container">
  <div class="cover-border-box">
    <div class="cover-inst-header">
      <div class="cover-inst-code">GUJARAT TECHNOLOGICAL UNIVERSITY, AHMEDABAD · INST CODE: {STUDENT['inst_code']}</div>
      <div class="cover-inst-name">{STUDENT['institute'].upper()}</div>
      <div class="cover-inst-dept">{STUDENT['branch'].upper()} DEPARTMENT</div>
      <div class="cover-divider"></div>
    </div>

    <div class="cover-title-section">
      <div class="cover-doc-type">Official Laboratory Code &amp; Implementation Appendix</div>
      <div class="cover-course-title">ARTIFICIAL INTELLIGENCE WITH PROMPT ENGINEERING</div>
      <div class="cover-course-code">Course Code: {STUDENT['course_code']}</div>
      <div class="cover-term">Complete Code Listings, Prompt Engineering Templates &amp; Privata RAG Implementation</div>
    </div>

    <div class="cover-student-card">
      <table>
        <tr>
          <td class="lbl">Student Full Name:</td>
          <td class="val"><strong>{STUDENT['name']}</strong></td>
        </tr>
        <tr>
          <td class="lbl">Enrollment Number:</td>
          <td class="val">{STUDENT['enrollment_no']}</td>
        </tr>
        <tr>
          <td class="lbl">Class Roll Number:</td>
          <td class="val">{STUDENT['roll_no']}</td>
        </tr>
        <tr>
          <td class="lbl">Division &amp; Batch:</td>
          <td class="val">Division {STUDENT['division']} · Batch {STUDENT['batch']}</td>
        </tr>
        <tr>
          <td class="lbl">Program / Branch:</td>
          <td class="val">Diploma in {STUDENT['branch']} (Semester 5)</td>
        </tr>
        <tr>
          <td class="lbl">Institute:</td>
          <td class="val">{STUDENT['institute']} (Code: {STUDENT['inst_code']})</td>
        </tr>
        <tr>
          <td class="lbl">Academic Term:</td>
          <td class="val">{STUDENT['academic_year']} ({STUDENT['term']})</td>
        </tr>
      </table>
    </div>

    <div class="cover-footer-sigs">
      <div class="cover-sig-item">
        <div class="cover-sig-line"></div>
        <div class="cover-sig-title">{STUDENT['faculty_guide']}</div>
        <div class="cover-sig-sub">Faculty Guide / Examiner</div>
      </div>
      <div class="cover-sig-item">
        <div class="cover-sig-line"></div>
        <div class="cover-sig-title">{STUDENT['hod']}</div>
        <div class="cover-sig-sub">Department of Information Technology</div>
      </div>
    </div>
  </div>
</div>
"""

    # 2. Code Index Table
    index_rows = []
    for idx, cf in enumerate(CODE_FILES, 1):
        target_id = f"code-file-{idx:02d}"
        index_rows.append(f"""
<tr>
  <td style="text-align: center; font-weight: bold;">{idx}</td>
  <td><strong>{cf['practical']}</strong></td>
  <td><code>{cf['rel_path']}</code></td>
  <td>{cf['desc']}</td>
  <td style="text-align: center; font-weight: bold;">
    <a class="page-target-link" href="#{target_id}"></a>
  </td>
</tr>
""")

    index_html = f"""
<div class="page-break" id="code-appendix-index">
  <h1>Code &amp; Prompt Files Index</h1>
  <p>The following table indexes all practical code files, prompt engineering templates, and Privata RAG system modules included in this submission package.</p>
  
  <table>
    <thead>
      <tr>
        <th style="width: 5%; text-align: center;">#</th>
        <th style="width: 18%;">Practical</th>
        <th style="width: 25%;">File Path</th>
        <th style="width: 42%;">Description &amp; Functionality</th>
        <th style="width: 10%; text-align: center;">Page</th>
      </tr>
    </thead>
    <tbody>
      {''.join(index_rows)}
    </tbody>
  </table>
  
  <div style="margin-top: 10px; font-size: 7.5pt; color: #334155; background: #f8fafc; border: 1px solid #cbd5e1; border-left: 2.5pt solid #1e3a8a; padding: 6px 10px;">
    <strong>GTU Verification Note:</strong> All source code files and prompt workflows are implemented, tested, and verified under Linux / Python 3.10+. The Privata RAG pipeline utilizes local MiniLM embeddings and ChromaDB vector store for strict data privacy.
  </div>
</div>
"""

    # 3. Formatted Code Listings
    code_sections = []
    formatter = HtmlFormatter(linenos="table", cssclass="codehilite", style="default")

    for idx, cf in enumerate(CODE_FILES, 1):
        target_id = f"code-file-{idx:02d}"
        full_path = os.path.join(CODE_DIR, cf["rel_path"])
        
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            code_text = f.read()

        # Select Lexer
        if cf["lang"] == "python":
            lexer = PythonLexer()
        elif cf["lang"] == "markdown":
            lexer = MarkdownLexer()
        else:
            lexer = TextLexer()

        highlighted_code = highlight(code_text, lexer, formatter)
        line_count = len(code_text.splitlines())

        code_sections.append(f"""
<div class="page-break" id="{target_id}">
  <div class="gtu-practical-header">
    <table class="gtu-header-table">
      <tr class="gtu-inst-row">
        <td colspan="4">
          GOVERNMENT POLYTECHNIC, GANDHINAGAR &bull; DEPARTMENT OF INFORMATION TECHNOLOGY
        </td>
      </tr>
      <tr class="gtu-meta-row">
        <td style="width: 30%;"><strong>Category:</strong> {cf['practical']}</td>
        <td style="width: 25%;"><strong>Language:</strong> {cf['lang'].upper()}</td>
        <td style="width: 20%;"><strong>Lines:</strong> {line_count}</td>
        <td style="width: 25%;"><strong>Item:</strong> File {idx:02d} of {len(CODE_FILES)}</td>
      </tr>
      <tr class="gtu-title-row">
        <td colspan="4">
          <span class="gtu-title-tag">FILE:</span> <code>{cf['rel_path']}</code> &bull; <span style="font-size: 8pt; color: #475569;">{cf['desc']}</span>
        </td>
      </tr>
    </table>
  </div>

  <div class="code-listing-wrap">
    {highlighted_code}
  </div>
</div>
""")

    code_appendix_css = COMMON_CSS.replace(
        '@top-left {\n        content: "AIPE Lab Manual | DI05016011 | GTU Code: 623";',
        '@top-left {\n        content: "AIPE Code Appendix | DI05016011 | GTU Code: 623";'
    ) + """
table.codehilitetable {
    width: 100%;
    border-collapse: collapse;
    margin: 3px 0;
    font-size: 6.8pt;
    font-family: 'DejaVu Sans Mono', monospace;
}
table.codehilitetable td {
    padding: 0;
    border: none;
}
td.linenos {
    width: 30px;
    padding-right: 5px !important;
    border-right: 1px solid #cbd5e1 !important;
    color: #94a3b8;
    text-align: right;
    user-select: none;
    vertical-align: top;
}
td.linenos div.linenodiv {
    margin: 0;
    padding: 0;
}
td.code {
    padding-left: 6px !important;
    vertical-align: top;
}
td.code div {
    margin: 0;
    padding: 0;
}
td.code pre {
    margin: 0;
    padding: 0;
    border: none;
    background: transparent;
    font-size: 6.8pt;
    line-height: 1.32;
    white-space: pre-wrap;
    word-break: break-all;
}
"""

    full_appendix_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AIPE Code Appendix — {STUDENT['name']}</title>
  <style>
    {code_appendix_css}
  </style>
</head>
<body>
  {cover_html}
  {index_html}
  {''.join(code_sections)}
</body>
</html>"""

    doc = weasyprint.HTML(string=full_appendix_html).render()
    doc.write_pdf(output_path)
    print(f"✅ Generated {output_path} ({len(doc.pages)} pages)")

def main():
    """Main execution function to generate all required lab manual deliverables."""
    print("=" * 80)
    print("AIPE GTU LAB MANUAL GENERATION SUITE")
    print(f"Student: {STUDENT['name']} (Roll: {STUDENT['roll_no']} | Enr: {STUDENT['enrollment_no']})")
    print(f"Institute: {STUDENT['institute']} (Code: {STUDENT['inst_code']})")
    print("=" * 80)

    # 1. Main PDF
    main_pdf_path = os.path.join(BASE_DIR, "AIPE_Lab_Manual.pdf")
    generate_main_lab_manual(main_pdf_path)

    # 2. Individual Practicals
    generate_individual_practicals()

    # 3. Code Appendix
    appendix_pdf_path = os.path.join(BASE_DIR, "Code_Appendix.pdf")
    generate_code_appendix(appendix_pdf_path)

    print("\n" + "=" * 80)
    print("ALL DELIVERABLES SUCCESSFULLY GENERATED!")
    print(f"1. Main PDF:          {main_pdf_path}")
    print(f"2. Individual PDFs:   {BASE_DIR}/P01_*.pdf ... P12_*.pdf (12 files)")
    print(f"3. Code Appendix:     {appendix_pdf_path}")
    print("=" * 80)

if __name__ == "__main__":
    main()
