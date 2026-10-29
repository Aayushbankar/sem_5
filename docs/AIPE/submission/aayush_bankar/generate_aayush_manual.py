#!/usr/bin/env python3
"""
AIPE Institutional Lab Manual PDF Generator — Aayush Bankar
=============================================================
GTU / Government Polytechnic Academic Publication Standard:
- Strict Black & White (B/W) Print-Ready Monochrome Styling (0 Colors/Blues)
- CDCT Benchmark Cover Page Layout (Govt. Polytechnic Gandhinagar & DTE Logo)
- CDCT Benchmark Continuous Assessment Sheet Format
- Real Embedded ChatGPT / Terminal Output Verification Screenshots
- Liberation Serif & Liberation Mono Typography
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
SUBMISSION_DIR = "/mnt/work/college/sem_5/docs/AIPE/submission"
WRITEUPS_DIR = os.path.join(SUBMISSION_DIR, "writeups")
CODE_DIR = os.path.join(SUBMISSION_DIR, "code")
OUT_DIR = "/mnt/work/college/sem_5/docs/AIPE/submission/aayush_bankar"
SCREENSHOTS_DIR = os.path.join(OUT_DIR, "screenshots")
DTE_LOGO_PATH = "/mnt/work/college/sem_5/docs/FOB/figures/dte_logo.png"

# Student & Institutional Profile
STUDENT = {
    "name": "Aayush Bankar",
    "roll_no": "246230316006",
    "enrollment_no": "246230316006",
    "division": "A",
    "batch": "A1",
    "semester": "Semester-V",
    "branch": "Information Technology",
    "institute": "Govt. Polytechnic Gandhinagar",
    "inst_code": "623",
    "course_name": "Artificial Intelligence with Prompt Engineering",
    "course_code": "DI05016011",
    "academic_year": "2026-2027",
    "term": "Odd (2026-2027)",
    "faculty_guide": "Prof. A. S. Patel",
    "hod": "Head of Department (IT)",
}

# 12 Practicals Specification
PRACTICALS = [
    {
        "num": 1,
        "title": "Use Generative AI Tools for Different Task Types & Domains",
        "short_title": "GenAI Tools: Tasks & Domains",
        "file": "P01_GenAI_Tools_Tasks_Domains.md",
        "out_pdf": "P01_GenAI_Tools.pdf",
        "unit": 1,
        "hours": 2,
        "date": "09/07/2026",
    },
    {
        "num": 2,
        "title": "Sentiment Analysis & Text Classification using Python",
        "short_title": "Sentiment Analysis & NLP",
        "file": "P02_Sentiment_Analysis.md",
        "out_pdf": "P02_Sentiment_Analysis.pdf",
        "unit": 1,
        "hours": 2,
        "date": "16/07/2026",
    },
    {
        "num": 3,
        "title": "LLM Behavior Analysis: Prompt Variation, Context, Consistency",
        "short_title": "LLM Behavior Analysis",
        "file": "P03_LLM_Behavior_Analysis.md",
        "out_pdf": "P03_LLM_Behavior_Analysis.pdf",
        "unit": 2,
        "hours": 2,
        "date": "23/07/2026",
    },
    {
        "num": 4,
        "title": "LLM Capabilities & Limitations, Hallucination Detection",
        "short_title": "Capabilities & Limitations",
        "file": "P04_LLM_Capabilities_Limitations.md",
        "out_pdf": "P04_LLM_Capabilities_Limitations.pdf",
        "unit": 2,
        "hours": 2,
        "date": "30/07/2026",
    },
    {
        "num": 5,
        "title": "Design & Refine Prompts: Email Writing & Concept Explanation",
        "short_title": "Prompt Design & Refinement",
        "file": "P05_Prompt_Design_Refinement.md",
        "out_pdf": "P05_Prompt_Design_Refinement.pdf",
        "unit": 3,
        "hours": 2,
        "date": "06/08/2026",
    },
    {
        "num": 6,
        "title": "Zero-Shot, Few-Shot & Role-Based Prompting",
        "short_title": "Zero/Few-Shot & Role Prompting",
        "file": "P06_Zero_Few_Shot_Role.md",
        "out_pdf": "P06_Zero_Few_Shot_Role.pdf",
        "unit": 3,
        "hours": 2,
        "date": "13/08/2026",
    },
    {
        "num": 7,
        "title": "Chain-of-Thought & Prompt Chaining for Multi-Step Problems",
        "short_title": "CoT & Prompt Chaining",
        "file": "P07_CoT_Prompt_Chaining.md",
        "out_pdf": "P07_CoT_Prompt_Chaining.pdf",
        "unit": 4,
        "hours": 2,
        "date": "20/08/2026",
    },
    {
        "num": 8,
        "title": "Task-Based Prompt Engineering: Summarization, Blog, Code",
        "short_title": "Task-Based Prompt Engineering",
        "file": "P08_Task_Based_Prompt_Eng.md",
        "out_pdf": "P08_Task_Based_Prompt_Eng.pdf",
        "unit": 4,
        "hours": 2,
        "date": "27/08/2026",
    },
    {
        "num": 9,
        "title": "AI Tools for Software Development: Generation, Debugging, Explanation",
        "short_title": "AI for Software Development",
        "file": "P09_AI_Tools_Software_Dev.md",
        "out_pdf": "P09_AI_Tools_Software_Dev.pdf",
        "unit": 5,
        "hours": 2,
        "date": "03/09/2026",
    },
    {
        "num": 10,
        "title": "AI Chatbot via API Integration (OpenAI/Gemini) with Python",
        "short_title": "AI Chatbot API Integration",
        "file": "P10_AI_Chatbot_API.md",
        "out_pdf": "P10_AI_Chatbot_API.pdf",
        "unit": 5,
        "hours": 4,
        "date": "10/09/2026",
    },
    {
        "num": 11,
        "title": "Document-Based Question Answering (RAG) — Privata",
        "short_title": "Document QA RAG (Privata)",
        "file": "P11_Document_QA_RAG.md",
        "out_pdf": "P11_Document_QA_RAG.pdf",
        "unit": 5,
        "hours": 4,
        "date": "24/09/2026",
    },
    {
        "num": 12,
        "title": "AI Application Development: Security Vulnerability & Mitigation Assistant",
        "short_title": "Security Vulnerability Assistant",
        "file": "P12_AI_Study_Assistant.md",
        "out_pdf": "P12_Security_Research.pdf",
        "unit": 5,
        "hours": 4,
        "date": "08/10/2026",
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
        "title": "Security Vulnerability & Mitigation Assistant",
        "rel_path": "p12_security_research_assistant.py",
        "lang": "python",
        "desc": "AI application for automated vulnerability triage, CWE classification, and defensive code remediation",
    },
    {
        "practical": "Practical 12",
        "title": "AI Study Assistant Prototype",
        "rel_path": "p12_study_assistant.py",
        "lang": "python",
        "desc": "Reference study assistant implementation for academic query answering",
    },
]

PYGMENTS_BW_CSS = HtmlFormatter(style="bw").get_style_defs(".codehilite")

# Pure Black & White (B/W) Print-Ready CSS
INSTITUTIONAL_BW_CSS = f"""
@page {{
    size: A4 portrait;
    margin: 14mm 14mm 14mm 14mm;
    @top-left {{
        content: "GOVERNMENT POLYTECHNIC, GANDHINAGAR · DEPT. OF IT";
        font-family: 'Times New Roman', 'Liberation Serif', serif;
        font-size: 8pt;
        font-weight: bold;
        color: #000000;
        border-bottom: 0.75pt solid #000000;
        padding-bottom: 3px;
    }}
    @top-right {{
        content: "{STUDENT['name']} | Roll No: {STUDENT['roll_no']}";
        font-family: 'Times New Roman', 'Liberation Serif', serif;
        font-size: 8pt;
        font-weight: bold;
        color: #000000;
        border-bottom: 0.75pt solid #000000;
        padding-bottom: 3px;
    }}
    @bottom-left {{
        content: "DI05016011: ARTIFICIAL INTELLIGENCE WITH PROMPT ENGINEERING";
        font-family: 'Times New Roman', 'Liberation Serif', serif;
        font-size: 7.5pt;
        color: #222222;
        border-top: 0.75pt solid #000000;
        padding-top: 3px;
    }}
    @bottom-right {{
        content: "Page " counter(page) " of " counter(pages);
        font-family: 'Times New Roman', 'Liberation Serif', serif;
        font-size: 7.5pt;
        font-weight: bold;
        color: #000000;
        border-top: 0.75pt solid #000000;
        padding-top: 3px;
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
    font-family: 'Times New Roman', 'Liberation Serif', serif;
    font-size: 9pt;
    line-height: 1.35;
    color: #000000;
}}

.page-break {{
    page-break-before: always;
}}

/* Typography */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Times New Roman', 'Liberation Serif', serif;
    color: #000000;
    page-break-after: avoid;
    break-after: avoid;
    font-weight: bold;
}}

h1 {{
    font-size: 12.5pt;
    color: #000000;
    border-bottom: 1.5pt solid #000000;
    padding-bottom: 2px;
    margin-top: 0;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

h2 {{
    font-size: 10pt;
    color: #000000;
    border-bottom: 0.75pt solid #000000;
    padding-bottom: 2px;
    margin-top: 6px;
    margin-bottom: 4px;
}}

h3 {{
    font-size: 9pt;
    color: #000000;
    margin-top: 5px;
    margin-bottom: 2px;
}}

p {{
    margin-top: 0;
    margin-bottom: 4px;
    text-align: justify;
}}

ul, ol {{
    margin-top: 0;
    margin-bottom: 4px;
    padding-left: 18px;
}}

li {{
    margin-bottom: 1.5px;
}}

/* Practical Header Banner (Institutional B/W Boxed Format) */
.practical-banner {{
    border: 1.25pt solid #000000;
    background: #ffffff;
    padding: 6px 10px;
    margin-bottom: 8px;
}}
.practical-banner-top {{
    display: flex;
    justify-content: space-between;
    font-size: 8pt;
    font-weight: bold;
    color: #000000;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 0.5pt solid #000000;
    padding-bottom: 3px;
    margin-bottom: 4px;
}}
.practical-banner-title {{
    font-size: 12pt;
    font-weight: bold;
    color: #000000;
    margin-bottom: 4px;
}}
.practical-banner-meta {{
    font-size: 7.5pt;
    color: #222222;
    display: flex;
    gap: 16px;
}}

/* Aim Callout */
.aim-callout {{
    border: 1pt solid #000000;
    border-left: 3.5pt solid #000000;
    background-color: #f9f9f9;
    padding: 6px 10px;
    margin: 5px 0 8px 0;
}}
.aim-label {{
    font-size: 8pt;
    font-weight: bold;
    color: #000000;
    text-transform: uppercase;
    margin-bottom: 2px;
    letter-spacing: 0.5px;
}}
.aim-text {{
    font-size: 8.5pt;
    color: #000000;
    margin: 0;
}}

/* Tables (Pure B/W High Contrast Print Ready) */
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 5px 0;
    font-size: 7.5pt;
    page-break-inside: auto;
}}

tr {{
    page-break-inside: avoid;
    break-inside: avoid;
}}

th {{
    background-color: #f0f0f0;
    color: #000000;
    font-weight: bold;
    text-align: left;
    padding: 3.5px 6px;
    border: 1px solid #000000;
    font-size: 7.5pt;
}}

td {{
    padding: 3px 6px;
    border: 1px solid #000000;
    vertical-align: top;
    font-size: 7.5pt;
    color: #000000;
}}

tr:nth-child(even) td {{
    background-color: #fafafa;
}}

/* Code & Highlight (Pure B/W) */
{PYGMENTS_BW_CSS}

pre, .codehilite pre {{
    background-color: #fafafa;
    border: 1px solid #000000;
    padding: 4px 6px;
    font-family: 'Liberation Mono', 'Courier New', monospace;
    font-size: 6.8pt;
    line-height: 1.25;
    white-space: pre-wrap;
    word-break: break-word;
    margin: 3px 0 5px 0;
    page-break-inside: auto;
}}

code {{
    font-family: 'Liberation Mono', 'Courier New', monospace;
    font-size: 7.5pt;
    background-color: #f4f4f4;
    padding: 1px 3px;
    border: 0.5pt solid #999999;
}}

blockquote {{
    border-left: 3pt solid #000000;
    background-color: #f9f9f9;
    margin: 5px 0;
    padding: 4px 8px;
    font-style: italic;
    color: #111827;
}}

/* Screenshot Frame (High Quality Verification Image) */
.screenshot-frame {{
    border: 1.25pt solid #000000;
    background: #ffffff;
    padding: 4px;
    margin: 5px 0 6px 0;
    text-align: center;
    page-break-inside: avoid;
    break-inside: avoid;
}}
.screenshot-frame img {{
    width: 100%;
    max-width: 100%;
    height: auto;
    max-height: 310px;
    object-fit: contain;
    border: 0.5pt solid #000000;
    display: block;
    margin: 0 auto;
    filter: contrast(1.05) grayscale(0.2);
}}
.screenshot-caption {{
    font-size: 7.2pt;
    font-weight: bold;
    color: #000000;
    margin-top: 3px;
    border-top: 0.5pt solid #000000;
    padding-top: 2px;
}}
.screenshot-meta {{
    font-size: 6.8pt;
    color: #222222;
    margin-top: 1px;
}}

/* Practical Evaluation & Signature Block */
.practical-eval-footer {{
    margin-top: 6px;
    padding-top: 4px;
    border-top: 1pt solid #000000;
    page-break-inside: avoid;
    break-inside: avoid;
}}
.eval-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 2px;
}}
.eval-table th {{
    background-color: #f0f0f0;
    color: #000000;
    font-size: 6.8pt;
    padding: 2.5px 4px;
    text-align: center;
    border: 1px solid #000000;
}}
.eval-table td {{
    font-size: 7pt;
    padding: 2.5px 4px;
    text-align: center;
    border: 1px solid #000000;
}}
.eval-sig-block {{
    display: flex;
    justify-content: space-between;
    margin-top: 6px;
    font-size: 7.2pt;
}}
.eval-sig-item {{
    width: 45%;
    text-align: center;
}}
.eval-sig-line {{
    border-bottom: 1px dashed #000000;
    height: 18px;
    margin-bottom: 2px;
}}

/* Internal Link for Index Page Numbers */
a.page-target-link {{
    text-decoration: none;
    font-weight: bold;
    color: #000000;
}}
a.page-target-link::after {{
    content: target-counter(attr(href), page);
}}

/* CDCT Gold Standard Cover Page Layout */
.cdct-cover {{
    page: no-headers-footers;
    width: 100%;
    height: 100vh;
    box-sizing: border-box;
    padding: 26mm 16mm 18mm 16mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    font-family: 'Times New Roman', 'Liberation Serif', serif;
}}
.cdct-title {{
    font-size: 26pt;
    font-weight: bold;
    line-height: 1.25;
    color: #000000;
    margin-bottom: 12px;
}}
.cdct-course {{
    font-size: 16pt;
    font-weight: bold;
    color: #000000;
    margin-bottom: 8px;
}}
.cdct-sub {{
    font-size: 13pt;
    font-weight: bold;
    color: #000000;
    margin-bottom: 25px;
}}
.cdct-table {{
    width: 88%;
    margin: 20px auto 25px auto;
    border-collapse: collapse;
    font-size: 10.5pt;
}}
.cdct-table td {{
    padding: 7px 12px;
    border: 1px solid #000000;
    text-align: left;
}}
.cdct-table td.label {{
    font-weight: bold;
    width: 38%;
    background-color: #f7f7f7;
    color: #000000;
}}
.cdct-table td.val {{
    font-weight: bold;
    width: 62%;
    color: #000000;
}}
.cdct-logo-container {{
    margin: 15px auto 10px auto;
    text-align: center;
}}
.cdct-logo {{
    width: 140px;
    height: auto;
    filter: grayscale(1.0) contrast(1.1);
}}
.cdct-footer {{
    font-size: 14.5pt;
    font-weight: bold;
    color: #000000;
    margin-top: 15px;
    letter-spacing: 0.5px;
}}

/* Certificate Page Styles (Strict B/W) */
.cert-container {{
    page: no-headers-footers;
    padding: 12mm 14mm;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100vh;
}}
.cert-box {{
    border: 2pt solid #000000;
    padding: 10mm 12mm;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
}}
.cert-title {{
    font-size: 20pt;
    font-weight: bold;
    color: #000000;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 5px;
    margin-bottom: 10px;
}}
.cert-body {{
    font-size: 9.5pt;
    line-height: 1.6;
    text-align: justify;
    color: #000000;
    margin: 10px 0;
}}
.cert-body strong {{
    color: #000000;
}}
.cert-details-table {{
    width: 82%;
    margin: 10px auto;
}}
.cert-details-table td {{
    padding: 4px 6px;
    border: 1px solid #000000;
    font-size: 8pt;
}}
.cert-sigs {{
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
}}
.cert-sig-block {{
    width: 30%;
    text-align: center;
}}
.cert-sig-line {{
    border-bottom: 1px dashed #000000;
    height: 35px;
    margin-bottom: 4px;
}}
.cert-sig-label {{
    font-size: 8pt;
    font-weight: bold;
    color: #000000;
}}
.cert-sig-sub {{
    font-size: 7pt;
    color: #333333;
}}

/* CDCT Continuous Assessment Sheet Styles */
.cas-container {{
    page-break-before: always;
    font-family: 'Times New Roman', 'Liberation Serif', serif;
}}
.cas-title {{
    font-size: 16pt;
    font-weight: bold;
    text-align: center;
    color: #000000;
    margin-top: 0;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}}
.cas-meta-line {{
    display: flex;
    justify-content: space-between;
    font-size: 8.5pt;
    font-weight: bold;
    color: #000000;
    margin-bottom: 3px;
    padding: 0 4px;
}}
.cas-sub-div {{
    font-size: 8.5pt;
    font-weight: bold;
    text-align: center;
    color: #000000;
    margin-bottom: 6px;
}}
.cas-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 7.8pt;
    margin-top: 2px;
}}
.cas-table th {{
    background-color: #f0f0f0;
    color: #000000;
    font-weight: bold;
    border: 1px solid #000000;
    padding: 5px 4px;
    text-align: center;
    font-size: 8pt;
}}
.cas-table td {{
    border: 1px solid #000000;
    padding: 4px 5px;
    vertical-align: middle;
    font-size: 7.6pt;
    color: #000000;
}}
"""

def generate_cover_page() -> str:
    """Generates the CDCT benchmark laboratory manual cover page."""
    return f"""
<div class="cdct-cover">
  <div>
    <div class="cdct-title">Diploma Engineering Laboratory<br>Manual</div>
    <div class="cdct-course">({STUDENT['course_name']}) ({STUDENT['course_code']})</div>
    <div class="cdct-sub">[{STUDENT['branch']}, {STUDENT['semester']} (Division - {STUDENT['division']})]</div>
  </div>

  <table class="cdct-table">
    <tr>
      <td class="label">Enrolment No</td>
      <td class="val">{STUDENT['enrollment_no']}</td>
    </tr>
    <tr>
      <td class="label">Name</td>
      <td class="val">{STUDENT['name']}</td>
    </tr>
    <tr>
      <td class="label">Branch</td>
      <td class="val">{STUDENT['branch']}</td>
    </tr>
    <tr>
      <td class="label">Academic Term</td>
      <td class="val">{STUDENT['term']}</td>
    </tr>
    <tr>
      <td class="label">Institute</td>
      <td class="val">{STUDENT['institute']}</td>
    </tr>
  </table>

  <div class="cdct-logo-container">
    <img src="file://{DTE_LOGO_PATH}" class="cdct-logo" alt="Directorate of Technical Education Logo" />
  </div>

  <div class="cdct-footer">
    Directorate Of Technical Education Gandhinagar - Gujarat
  </div>
</div>
"""

def generate_certificate_page() -> str:
    """Generates the official GTU Department Certificate page in B/W."""
    return f"""
<div class="page-break cert-container">
  <div class="cert-box">
    <div>
      <div style="font-size: 8.5pt; font-weight: bold; color: #333333; letter-spacing: 1px;">GUJARAT TECHNOLOGICAL UNIVERSITY</div>
      <div style="font-size: 14pt; font-weight: bold; color: #000000; margin: 3px 0;">{STUDENT['institute']}</div>
      <div style="font-size: 10pt; font-weight: bold; color: #000000;">DEPARTMENT OF {STUDENT['branch'].upper()}</div>
      <div style="height: 1.5pt; background: #000000; margin: 8px auto; width: 50%;"></div>
    </div>

    <div class="cert-title">CERTIFICATE</div>

    <div class="cert-body">
      This is to certify that Mr./Ms. <strong>{STUDENT['name']}</strong>, 
      Enrollment No: <strong>{STUDENT['enrollment_no']}</strong> (Roll No: <strong>{STUDENT['roll_no']}</strong>), 
      is a bonafide student of <strong>5th Semester Diploma in Information Technology</strong> at 
      <strong>{STUDENT['institute']} (Code: {STUDENT['inst_code']})</strong>.
      <br><br>
      He/She has satisfactorily completed the requisite laboratory course work and continuous term work exercises in 
      <strong>{STUDENT['course_name']} ({STUDENT['course_code']})</strong> prescribed by Gujarat Technological 
      University for the <strong>{STUDENT['term']}</strong> of Academic Year <strong>{STUDENT['academic_year']}</strong>.
    </div>

    <table class="cert-details-table">
      <tr>
        <td style="font-weight: bold; width: 35%; background: #f0f0f0;">Course Title:</td>
        <td>{STUDENT['course_name']} ({STUDENT['course_code']})</td>
      </tr>
      <tr>
        <td style="font-weight: bold; background: #f0f0f0;">Total Practicals Completed:</td>
        <td>12 Practicals (P01 to P12 Prescribed GTU Curriculum)</td>
      </tr>
      <tr>
        <td style="font-weight: bold; background: #f0f0f0;">Student Identification:</td>
        <td>{STUDENT['name']} · Roll No: {STUDENT['roll_no']} · Div {STUDENT['division']}</td>
      </tr>
      <tr>
        <td style="font-weight: bold; background: #f0f0f0;">Term Work Assessment:</td>
        <td>Completed Satisfactorily & Verified for GTU Exam Submission</td>
      </tr>
    </table>

    <div class="cert-sigs">
      <div class="cert-sig-block">
        <div class="cert-sig-line"></div>
        <div class="cert-sig-label">Course Faculty</div>
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
        <div class="cert-sig-sub">GTU Commission / Seat No.</div>
      </div>
    </div>
  </div>
</div>
"""

def generate_continuous_assessment_sheet() -> str:
    """Generates the CDCT Continuous Assessment Sheet format with dynamic target links."""
    rows = []
    for p in PRACTICALS:
        page_link = f'<a class="page-target-link" href="#practical-{p["num"]:02d}"></a>'
        rows.append(f"""
        <tr>
          <td style="text-align: center; font-weight: bold;">{p['num']}</td>
          <td style="text-align: left; padding-left: 6px;">{p['title']}</td>
          <td style="text-align: center;">{page_link}</td>
          <td style="text-align: center;">{p['date']}</td>
          <td style="text-align: center;"></td>
          <td style="text-align: center;"></td>
        </tr>
        """)

    return f"""
<div class="page-break cas-container" id="index-section">
  <div class="cas-title">Continuous Assessment Sheet</div>
  <div class="cas-meta-line">
    <span>Enrolment No: <strong>{STUDENT['enrollment_no']}</strong></span>
    <span>Name: <strong>{STUDENT['name']}</strong></span>
    <span>Term: <strong>{STUDENT['term']}</strong></span>
  </div>
  <div class="cas-sub-div">(Division - {STUDENT['division']})</div>
  <table class="cas-table">
    <thead>
      <tr>
        <th style="width: 5%;">S.</th>
        <th style="width: 53%; text-align: left; padding-left: 6px;">Practical Outcome / Title of Experiment</th>
        <th style="width: 8%;">Page</th>
        <th style="width: 12%;">Date</th>
        <th style="width: 11%;">Marks (25)</th>
        <th style="width: 11%;">Sign</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</div>
"""

def make_eval_footer() -> str:
    """Generates faculty evaluation & signature block at practical conclusion."""
    return f"""
<div class="practical-eval-footer">
  <table class="eval-table">
    <thead>
      <tr>
        <th>Timely Submission (2M)</th>
        <th>Process / Code Execution (4M)</th>
        <th>Output Verification (2M)</th>
        <th>Viva-Voce & Application (2M)</th>
        <th>Total Marks (10M)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>____ / 2</td>
        <td>____ / 4</td>
        <td>____ / 2</td>
        <td>____ / 2</td>
        <td style="font-weight: bold; font-size: 8pt;">____ / 10</td>
      </tr>
    </tbody>
  </table>
  <div class="eval-sig-block">
    <div class="eval-sig-item">
      <div class="eval-sig-line"></div>
      <div>Student Signature ({STUDENT['name']}) · Date: __________</div>
    </div>
    <div class="eval-sig-item">
      <div class="eval-sig-line"></div>
      <div>Faculty Examiner Signature · Date: __________</div>
    </div>
  </div>
</div>
"""

def render_markdown_practical(md_file_path: str, practical_num: int, is_standalone: bool = False) -> str:
    """Renders a practical markdown writeup into institutional B/W academic HTML with real screenshots."""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip Files Submitted section and redundant signature lines
    content = re.sub(r'##\s*\d*\.?\s*Files Submitted.*?(?=(?:^##\s|\Z))', '', content, flags=re.DOTALL | re.MULTILINE)
    content = re.sub(r'\*\*Student Signature:\*\*.*?Faculty Signature:\*\*.*', '', content)
    content = re.sub(r'Student Signature:.*?Faculty Signature:.*', '', content)

    # Strip any redundant checklists like "Submission Checklist"
    content = re.sub(r'##\s*Submission Checklist[\s\S]*?(?=(?:^##\s|\Z))', '', content)

    # Populate all student placeholders
    content = content.replace("[STUDENT NAME]", STUDENT["name"])
    content = content.replace("[ROLL NO]", STUDENT["roll_no"])
    content = content.replace("[YOUR NAME]", STUDENT["name"])
    content = content.replace("[YOUR ROLL NUMBER]", STUDENT["roll_no"])
    content = re.sub(r'\[Student Name:\s*__+\s*\|\s*Roll No:\s*__+\]', f"[Student Name: {STUDENT['name']} | Roll No: {STUDENT['roll_no']}]", content)
    content = re.sub(r'\[STUDENT NAME\s*\|\s*ROLL NO:\s*__+\]', f"[{STUDENT['name']} | Roll No: {STUDENT['roll_no']}]", content)
    content = content.replace("[STUDENT NAME, ROLL NO]", f"[{STUDENT['name']}, {STUDENT['roll_no']}]")

    # Embed real customized screenshot
    screenshot_file = os.path.join(SCREENSHOTS_DIR, f"P{practical_num:02d}_screenshot.png")
    file_url = f"file://{screenshot_file}"
    screenshot_html_block = f"""
<div class="screenshot-frame">
  <img src="{file_url}" alt="Practical {practical_num:02d} Execution Screenshot" />
  <div class="screenshot-caption">Figure {practical_num:02d}: Verified Terminal / Application Execution Output (ChatGPT / CLI)</div>
  <div class="screenshot-meta">Student: <strong>{STUDENT['name']}</strong> | Class Roll No: <strong>{STUDENT['roll_no']}</strong> | Enrollment No: <strong>{STUDENT['enrollment_no']}</strong> | Govt. Polytechnic Gandhinagar</div>
</div>
"""
    # Insert screenshot right under the Screenshot header
    if re.search(r'##\s*\d*\.?\s*Screenshot of Output', content):
        content = re.sub(
            r'(##\s*\d*\.?\s*Screenshot of Output[^\n]*\n)',
            r'\1\n' + screenshot_html_block.replace('\\', '\\\\') + '\n',
            content,
            count=1
        )
    else:
        content += f"\n\n## Screenshot of Output\n\n{screenshot_html_block}\n"

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['fenced_code', 'codehilite', 'tables'])
    body_html = md.convert(content)

    # Append evaluation block before concluding
    body_html += make_eval_footer()

    p_info = PRACTICALS[practical_num - 1]
    banner_html = f"""
<div class="practical-banner">
  <div class="practical-banner-top">
    <span>Practical Exercise {practical_num:02d}</span>
    <span>Unit {p_info['unit']} · Allocated Lab Hours: {p_info['hours']} Hrs</span>
  </div>
  <div class="practical-banner-title">{p_info['title']}</div>
  <div class="practical-banner-meta">
    <span><strong>Course:</strong> {STUDENT['course_name']} ({STUDENT['course_code']})</span>
    <span><strong>Student:</strong> {STUDENT['name']} (Roll: {STUDENT['roll_no']})</span>
  </div>
</div>
"""

    page_break_class = "page-break" if not is_standalone else ""
    return f"""
<div class="{page_break_class}" id="practical-{practical_num:02d}">
  {banner_html}
  {body_html}
</div>
"""

def generate_main_lab_manual(output_path: str):
    """Compiles and generates the complete combined AIPE Lab Manual PDF."""
    print("=" * 70)
    print("Generating Deliverable 1: Main Lab Manual (AIPE_Lab_Manual.pdf)...")
    print("=" * 70)

    cover_html = generate_cover_page()
    cert_html = generate_certificate_page()
    cas_html = generate_continuous_assessment_sheet()

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
    {INSTITUTIONAL_BW_CSS}
  </style>
</head>
<body>
  {cover_html}
  {cert_html}
  {cas_html}
  {all_practicals_html}
</body>
</html>"""

    doc = weasyprint.HTML(string=full_document, base_url=OUT_DIR).render()
    doc.write_pdf(output_path)
    print(f"Generated {output_path} ({len(doc.pages)} pages)")
    return len(doc.pages)

def generate_individual_practicals():
    """Generates 12 standalone individual practical PDFs in B/W."""
    print("\n" + "=" * 70)
    print("Generating Deliverable 2: Individual Practical PDFs (P01..P12)...")
    print("=" * 70)

    for p in PRACTICALS:
        p_path = os.path.join(WRITEUPS_DIR, p["file"])
        out_pdf = os.path.join(OUT_DIR, p["out_pdf"])
        print(f"  Generating {p['out_pdf']} (Practical {p['num']:02d})...")

        p_html = render_markdown_practical(p_path, p["num"], is_standalone=True)

        full_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Practical {p['num']:02d}: {p['short_title']} — {STUDENT['name']}</title>
  <style>
    {INSTITUTIONAL_BW_CSS}
  </style>
</head>
<body>
  {p_html}
</body>
</html>"""

        doc = weasyprint.HTML(string=full_doc, base_url=OUT_DIR).render()
        doc.write_pdf(out_pdf)
        print(f"    -> Saved {out_pdf} ({len(doc.pages)} pages)")

def generate_code_appendix(output_path: str):
    """Compiles Deliverable 3: Code Appendix PDF containing all code files in B/W."""
    print("\n" + "=" * 70)
    print("Generating Deliverable 3: Code Appendix (Code_Appendix.pdf)...")
    print("=" * 70)

    cover_html = f"""
<div class="cdct-cover">
  <div>
    <div class="cdct-title">Technical Code & Prompt<br>Appendix</div>
    <div class="cdct-course">({STUDENT['course_name']}) ({STUDENT['course_code']})</div>
    <div class="cdct-sub">[{STUDENT['branch']}, {STUDENT['semester']} (Division - {STUDENT['division']})]</div>
  </div>

  <table class="cdct-table">
    <tr>
      <td class="label">Enrolment No</td>
      <td class="val">{STUDENT['enrollment_no']}</td>
    </tr>
    <tr>
      <td class="label">Name</td>
      <td class="val">{STUDENT['name']}</td>
    </tr>
    <tr>
      <td class="label">Branch</td>
      <td class="val">{STUDENT['branch']}</td>
    </tr>
    <tr>
      <td class="label">Repository Scope</td>
      <td class="val">23 Source Files (Standalone + Privata RAG Engine)</td>
    </tr>
    <tr>
      <td class="label">Institute</td>
      <td class="val">{STUDENT['institute']}</td>
    </tr>
  </table>

  <div class="cdct-logo-container">
    <img src="file://{DTE_LOGO_PATH}" class="cdct-logo" alt="Directorate of Technical Education Logo" />
  </div>

  <div class="cdct-footer">
    Directorate Of Technical Education Gandhinagar - Gujarat
  </div>
</div>
"""

    idx_rows = []
    for idx, c in enumerate(CODE_FILES, 1):
        idx_rows.append(f"""
        <tr>
          <td style="text-align: center; font-weight: bold;">{idx:02d}</td>
          <td><strong>{c['practical']}</strong></td>
          <td><code>{c['rel_path']}</code></td>
          <td>{c['title']}</td>
          <td style="text-align: center;"><a class="page-target-link" href="#code-file-{idx:02d}"></a></td>
        </tr>
        """)

    index_html = f"""
<div class="page-break cas-container" id="appendix-index">
  <div class="cas-title">Code & Prompt Files Index</div>
  <div class="cas-meta-line">
    <span>Enrolment No: <strong>{STUDENT['enrollment_no']}</strong></span>
    <span>Name: <strong>{STUDENT['name']}</strong></span>
    <span>Total Files: <strong>{len(CODE_FILES)}</strong></span>
  </div>
  <table class="cas-table">
    <thead>
      <tr>
        <th style="width: 6%; text-align: center;">#</th>
        <th style="width: 22%;">Associated Practical</th>
        <th style="width: 32%;">File Path in Repository</th>
        <th style="width: 32%;">Description</th>
        <th style="width: 8%; text-align: center;">Page</th>
      </tr>
    </thead>
    <tbody>
      {''.join(idx_rows)}
    </tbody>
  </table>
</div>
"""

    files_html_list = []
    formatter = HtmlFormatter(style="bw", cssclass="codehilite", linenos="inline")

    for idx, c in enumerate(CODE_FILES, 1):
        full_code_path = os.path.join(CODE_DIR, c["rel_path"])
        print(f"  Formatting file {idx:02d}/{len(CODE_FILES)}: {c['rel_path']}...")
        if not os.path.exists(full_code_path):
            print(f"    WARNING: File {full_code_path} not found!")
            continue

        with open(full_code_path, 'r', encoding='utf-8', errors='replace') as cf:
            raw_code = cf.read()

        if c["lang"] == "python":
            lexer = PythonLexer()
        elif c["lang"] == "markdown":
            lexer = MarkdownLexer()
        else:
            lexer = TextLexer()

        highlighted_code = highlight(raw_code, lexer, formatter)

        file_banner = f"""
<div class="practical-banner" style="margin-top: 5px;">
  <div class="practical-banner-top">
    <span>{c['practical']} · File {idx:02d} of {len(CODE_FILES)}</span>
    <span>Format: {c['lang'].upper()} · Length: {len(raw_code.splitlines())} Lines</span>
  </div>
  <div class="practical-banner-title" style="font-size: 11pt;">{c['title']} (<code>{c['rel_path']}</code>)</div>
  <div class="practical-banner-meta">
    <span>{c['desc']}</span>
  </div>
</div>
"""
        files_html_list.append(f"""
<div class="page-break" id="code-file-{idx:02d}">
  {file_banner}
  {highlighted_code}
</div>
""")

    all_files_html = "\n".join(files_html_list)

    full_appendix_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AIPE Code & Prompt Appendix — {STUDENT['name']}</title>
  <style>
    {INSTITUTIONAL_BW_CSS}
  </style>
</head>
<body>
  {cover_html}
  {index_html}
  {all_files_html}
</body>
</html>"""

    doc = weasyprint.HTML(string=full_appendix_doc, base_url=OUT_DIR).render()
    doc.write_pdf(output_path)
    print(f"Generated {output_path} ({len(doc.pages)} pages)")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    main_pdf_path = os.path.join(OUT_DIR, "AIPE_Lab_Manual.pdf")
    pages = generate_main_lab_manual(main_pdf_path)
    generate_individual_practicals()
    appendix_pdf_path = os.path.join(OUT_DIR, "Code_Appendix.pdf")
    generate_code_appendix(appendix_pdf_path)
    print("\nAll deliverables for Aayush Bankar successfully generated!")
