# Docling Markdown Studio 🚀

A premium, modern desktop-like web application to convert any type of document (PDF, Word, PowerPoint, Excel, HTML, or Images) to clean, highly structured Markdown using the state-of-the-art **IBM Docling** engine.

Developed with a high-performance **FastAPI backend** and a premium **glassmorphic dark cyber UI**.

---

## Key Features 🌟

- **Comprehensive Formats**: Converts PDF, DOCX, PPTX, XLSX, HTML, and raster images.
- **State-of-the-Art Parser**: Retains table gridlines, structure, reading order, and document sections.
- **Deep-Learning OCR**: Optional Optical Character Recognition (OCR) pipeline for scanned documents and image files.
- **Dual Visual Workspace**: Side-by-side split screen showing a fully rendered HTML visual preview and a raw Markdown monospaced code panel.
- **One-Click Actions**: Single-tap download as `.md`, copy-to-clipboard, or extract images.
- **URL Fetching**: Feed direct remote document or web links to convert them immediately.
- **Performance Metrics**: View detailed statistics including conversion time, pages processed, and document title.

---

## Installation & Setup 🛠️

Ensure you have [Anaconda or Miniconda](https://www.anaconda.com/) installed on your Windows system.

### Quick Start
Double-click the **`start_app.bat`** file in the root folder. It will:
1. Active the dedicated conda environment (`docling-env`).
2. Run the FastAPI development server on `http://127.0.0.1:8000`.
3. Automatically open your default web browser to the dashboard interface!

### Manual Setup & Execution
If you prefer running manual commands:

1. **Activate the environment**:
   ```bash
   conda activate docling-env
   ```
2. **Start the FastAPI backend server**:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
3. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

---

## Project Structure 📁

```
convert_to_markdown/
├── start_app.bat           # Quick launcher double-click script
├── requirements.txt         # Primary Python dependencies (docling, fastapi, etc.)
├── app/
│   ├── __init__.py          # Python package marker
│   ├── main.py              # FastAPI server & endpoints
│   ├── converter.py         # IBM Docling wrapper & extraction pipeline logic
│   └── static/              # Glassmorphic single page dashboard frontend
│       ├── index.html       # HTML layout & panel boundaries
│       ├── app.css          # Cyberpunk glass styling & responsive grids
│       └── app.js           # AJAX fetch requests & UI interaction handlers
└── README.md                # Project documentation
```

---

## Technical Details 🔬

- **Backend**: FastAPI (Python 3.11), Uvicorn, Python-Multipart.
- **Parser Engine**: IBM Docling, using layout classification models, table structure extractors, and OCR integrations.
- **Frontend**: Vanilla CSS grid & flex layouts, backdrop glass filtering, standard HTML5 semantic elements, Marked.js (GFM Markdown parser).
