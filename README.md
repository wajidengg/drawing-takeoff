# drawing-takeoff

PDF-based construction drawing takeoff tool for detecting, identifying, and counting symbols from MEP and architectural drawings.  

## Drawing Takeoff App
🚀 Live Demo: [Open App](https://drawing-takeoff-w.streamlit.app)

---

# Overview

`drawing-takeoff` is an experimental computer vision project focused on automating quantity takeoffs from construction drawings.

The initial goal is intentionally narrow and practical:

1. Upload a construction PDF drawing
2. Detect or isolate the legend area
3. Select a symbol from the legend
4. Find matching symbols across the sheet
5. Count occurrences
6. Export quantities to CSV

The project is designed as a lightweight and modular foundation for future AI-assisted construction document analysis.

---

# Why This Project Exists

Manual quantity takeoffs are repetitive and time-consuming.

Construction drawings already contain:
- standardized symbols
- legends
- repetitive layouts
- structured visual information

This project explores whether computer vision and lightweight AI workflows can automate portions of the estimating and takeoff process without requiring full BIM access.

The focus is:
- simplicity
- usability
- rapid iteration
- practical workflows over academic AI research

---

# MVP Scope

The first MVP (Minimum Viable Product) intentionally avoids complexity.

## Included

- PDF upload
- Drawing rendering
- Legend cropping
- User-selected symbol extraction
- Template matching
- Symbol counting
- CSV export

## Excluded (for now)

- LLM integration
- BIM/Revit parsing
- Multi-user authentication
- Cloud infrastructure
- Full OCR pipelines
- Multi-sheet intelligence
- AI-generated estimates
- Code compliance analysis

The goal is to validate:
> "Can construction symbols be reliably counted from PDFs with lightweight CV methods?"

---

# Current Technical Approach

The initial implementation uses traditional computer vision techniques before introducing machine learning.

## Pipeline

```text
PDF → Image Rendering → Legend Extraction → Symbol Selection
→ Template Matching → Count Detection → CSV Export
