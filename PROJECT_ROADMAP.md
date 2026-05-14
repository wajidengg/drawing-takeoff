````markdown
# PROJECT_ROADMAP.md

# drawing-takeoff

Comprehensive project roadmap, architecture, technical planning, long-term vision, and development reference for the `drawing-takeoff` repository.

---

# 1. Project Overview

`drawing-takeoff` is an experimental construction drawing analysis tool focused on automating quantity takeoffs from PDF-based construction documents.

The project initially targets:
- MEP drawings
- electrical plans
- HVAC layouts
- plumbing drawings
- reflected ceiling plans
- architectural symbol counting workflows

The core concept is simple:

> Use computer vision techniques to identify construction symbols from legends and automatically count matching symbols across drawings.

The project intentionally starts with lightweight deterministic computer vision methods before introducing larger AI or machine learning systems.

---

# 2. Initial MVP Goal

The first MVP (Minimum Viable Product) is intentionally narrow and practical.

## MVP Workflow

1. Upload PDF drawing
2. Render drawing page
3. Detect or isolate legend area
4. User selects a symbol from the legend
5. Extract symbol template
6. Find matching symbols across drawing
7. Count matches
8. Export quantity takeoff to CSV

---

# 3. Why This Project Exists

Manual quantity takeoffs are repetitive and labor-intensive.

Construction drawings already contain:
- structured layouts
- repetitive symbols
- legends
- standardized drafting conventions
- embedded quantity information

This project explores whether lightweight computer vision workflows can automate portions of estimating and takeoff processes without requiring full BIM access.

The primary goal is:
- practical workflow automation
- not academic AI research

---

# 4. Core Philosophy

The project intentionally prioritizes:

- simplicity
- modularity
- explainability
- deterministic workflows
- rapid iteration
- human-assisted interaction
- lightweight tooling

Instead of:
- massive AI infrastructure
- premature scaling
- large training pipelines
- overengineered architecture

Philosophy:

> Build useful workflows first. Add AI only where it creates measurable value.

---

# 5. Long-Term Vision

Long term, `drawing-takeoff` may evolve into a broader construction drawing intelligence platform.

Potential future capabilities:

- automated quantity takeoffs
- symbol classification
- OCR extraction
- equipment schedule extraction
- multi-sheet indexing
- drawing revision comparison
- specification parsing
- BIM integration
- natural language querying
- AI-assisted estimating
- coordination analysis
- clash detection support
- multimodal drawing understanding

Potential future workflow example:

> "Find all VAV units on Level 2 and compare against equipment schedules."

---

# 6. Initial Technical Strategy

The project begins with traditional computer vision techniques before introducing machine learning.

## Initial Pipeline

```text
PDF Upload
    ↓
PDF Rendering
    ↓
Legend Isolation
    ↓
User Symbol Selection
    ↓
Template Matching
    ↓
Quantity Detection
    ↓
CSV Export
````

---

# 7. Future AI-Enhanced Architecture

Long-term architecture may evolve toward:

```text
PDF / DWG / IFC
        ↓
Document Parsing Layer
        ↓
OCR + Vision Models
        ↓
Symbol Detection Models
        ↓
Geometric Reasoning Layer
        ↓
Structured Drawing Database
        ↓
LLM / AI Reasoning Layer
        ↓
Construction Intelligence Workflows
```

---

# 8. Proposed Repository Structure

## Current Structure

```text
drawing-takeoff/
│
├── app.py
├── requirements.txt
├── README.md
├── PROJECT_ROADMAP.md
├── LICENSE
├── .gitignore
│
├── core/
│   ├── __init__.py
│   ├── pdf_loader.py
│   ├── render.py
│   ├── takeoff.py
│
├── utils/
│   ├── __init__.py
│   ├── image_utils.py
│   ├── geometry.py
│
├── assets/
│   └── samples/
│
├── tests/
│   └── test_basic.py
│
└── .streamlit/
    └── config.toml
```

---

# 9. Purpose of Each Folder

## app.py

Primary Streamlit application entry point.

Responsible for:

* UI rendering
* file uploads
* workflow coordination

---

## core/

Core application logic.

### pdf_loader.py

Handles:

* PDF loading
* page extraction
* rendering PDF pages into images

### render.py

Handles:

* visualization
* overlays
* drawing rendering utilities

### takeoff.py

Handles:

* template matching
* symbol counting
* detection logic

---

## utils/

Shared helper utilities.

### image_utils.py

Image processing helpers:

* resizing
* thresholding
* cropping
* normalization

### geometry.py

Geometry-related calculations:

* bounding boxes
* overlap detection
* coordinate transforms

---

## assets/

Stores:

* sample PDFs
* debugging images
* example legends
* temporary visual assets

---

## tests/

Basic testing framework.

Future tests may include:

* rendering validation
* matching accuracy
* OCR validation

---

## .streamlit/

UI and Streamlit configuration files.

---

# 10. Planned Development Phases

# Phase 1 — PDF Viewer MVP

## Goal

Build a functional construction drawing viewer.

## Features

* PDF upload
* render first page
* display drawing image
* multi-page support

## Technologies

* Streamlit
* PyMuPDF
* OpenCV

---

# Phase 2 — Legend Interaction

## Goal

Allow user-guided symbol extraction.

## Features

* legend isolation
* click-to-select symbol
* symbol cropping

## Challenges

* inconsistent legend locations
* low-quality scans
* mixed raster/vector PDFs

---

# Phase 3 — Symbol Counting

## Goal

Detect repeated symbols across the drawing.

## Features

* template matching
* confidence thresholds
* duplicate filtering
* multi-scale matching

## Challenges

* rotation variance
* scale variance
* overlapping annotations
* drawing noise

---

# Phase 4 — Export Workflows

## Goal

Generate usable estimating outputs.

## Features

* CSV export
* quantity tables
* summary reports
* multi-symbol sessions

---

# Phase 5 — OCR + Semantic Extraction

## Goal

Introduce semantic understanding.

## Features

* OCR integration
* symbol label extraction
* schedule parsing
* sheet indexing

## Potential Tools

* PaddleOCR
* EasyOCR
* Tesseract

---

# Phase 6 — Machine Learning Detection

## Goal

Replace template matching with learned detectors.

## Features

* YOLO-based symbol detection
* custom datasets
* rotation-invariant detection
* semantic symbol classification

## Potential Tools

* YOLO
* Detectron2
* Segment Anything

---

# Phase 7 — AI-Assisted Construction Intelligence

## Goal

Add reasoning and contextual understanding.

## Potential Features

* natural language queries
* revision comparison
* schedule validation
* quantity verification
* coordination analysis
* AI-assisted estimating

## Potential AI Models

* multimodal LLMs
* vision-language models
* retrieval systems

---

# 11. Current Tech Stack

## Current

### Backend

* Python

### UI

* Streamlit

### PDF Rendering

* PyMuPDF

### Computer Vision

* OpenCV
* NumPy

---

## Future

### OCR

* PaddleOCR
* EasyOCR

### ML / Detection

* YOLO
* Detectron2

### AI Layer

* multimodal LLMs
* retrieval systems
* vector databases

---

# 12. Known Technical Challenges

# PDF Complexity

Construction PDFs are difficult because they may contain:

* vector geometry
* raster scans
* mixed layers
* embedded text
* faded scans
* inconsistent scaling

---

# Symbol Variability

Different consultants use:

* different drafting standards
* different symbol libraries
* different notation systems

This makes generalized automation difficult.

---

# Spatial Reasoning

Construction drawings contain:

* geometry
* relationships
* layering
* contextual meaning

Spatial reasoning is significantly harder than standard OCR tasks.

---

# 13. Why Start With Template Matching

The project intentionally starts with deterministic computer vision because:

* fast to prototype
* easy to debug
* no training data required
* lower infrastructure cost
* validates workflows early

Machine learning should only be introduced when:

* deterministic methods reach limitations
* enough labeled data exists
* complexity becomes justified

---

# 14. Potential Future Integrations

## BIM / CAD

* Revit
* IFC
* DWG
* Autodesk APIs

## Construction Platforms

* Procore
* Autodesk Construction Cloud
* estimating systems

## AI Infrastructure

* vector databases
* embedding systems
* retrieval pipelines
* multimodal search

---

# 15. Development Priorities

Priority order:

1. Build usable workflows
2. Improve reliability
3. Improve accuracy
4. Improve speed
5. Add intelligence
6. Scale architecture

The project should remain:

* modular
* explainable
* construction-focused
* practical

---

# 16. Non-Goals (For Now)

The project is NOT currently attempting to:

* replace BIM workflows
* fully automate estimating
* generate engineered designs
* perform code compliance automatically
* become a full CAD platform
* eliminate human review

The focus is:

> assisted automation and workflow acceleration

---

# 17. Potential Commercial Applications

Future use cases may include:

* estimating assistance
* bid preparation
* drawing QA/QC
* VDC workflows
* subcontractor takeoffs
* revision analysis
* field verification workflows

---

# 18. Development Notes

Important engineering principle:

> Construction document problems are often geometry and workflow problems before they are AI problems.

The project should avoid:

* premature AI complexity
* overtraining
* infrastructure bloat

Until simpler workflows are proven valuable.

---

# 19. Current Status

Project stage:

> Early experimental MVP

Current development focus:

* PDF rendering
* legend workflows
* symbol extraction
* template matching
* quantity takeoff automation

Not production-ready.

```
```
