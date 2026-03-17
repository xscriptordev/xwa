# xwa - Ideal Project Structure

This document outlines the ideal, decoupled architecture for the `xwa` (Web Analysis) project, separating the core analysis engine, the backend API, and the web frontend.

## Directory Tree

```text
xwa/
├── core/                   # The Python Core Analysis Engine (CLI)
│   ├── modules/            # Analysis modules
│   │   ├── seo.py          # Meta tags, headings, alt attributes
│   │   ├── sitemap.py      # Sitemap parsing and concurrent crawler
│   │   └── security.py     # Headers, SSL, sensitive directories
│   ├── export/             # Data serialization
│   │   ├── jsonc.py        # JSONC exporter
│   │   └── markdown.py     # Markdown report generator
│   ├── models/             # Shared data schemas (e.g., Pydantic)
│   ├── utils/              # Helper functions (http client, logging)
│   ├── cli.py              # Command-line interface entry point (Typer/Argparse)
│   └── main.py             # Internal API for the engine
│
├── api/                    # The FastAPI Backend
│   ├── routers/            # API Endpoints
│   │   ├── scan.py         # POST /api/scan triggering the core
│   │   ├── reports.py      # GET /api/reports/...
│   │   └── sse.py          # Real-time scan progress stream
│   ├── db/                 # Database configuration (SQLite + SQLAlchemy)
│   │   ├── models.py       # ORM Models
│   │   └── migrations/     # Alembic migrations
│   ├── tasks/              # Background tasks (Celery/RQ/FastAPI BackgroundTasks)
│   └── main.py             # FastAPI application instance
│
├── web/                    # The Next.js Frontend (React)
│   ├── src/
│   │   ├── app/            # Next.js App Router pages
│   │   │   ├── page.tsx    # Home (Search input)
│   │   │   ├── dashboard/  # Dashboard views
│   │   │   └── history/    # Scan history
│   │   ├── components/     # Reusable UI components (Shadcn/UI)
│   │   │   ├── ui/         # Base components (buttons, cards, inputs)
│   │   │   ├── dashboard/  # Specific charts and tables
│   │   │   └── layout/     # Sidebar, Header
│   │   ├── lib/            # Utilities (API client, formatting)
│   │   └── styles/         # Global CSS and Tailwind configuration
│   ├── package.json
│   └── tailwind.config.ts
│
├── docs/                   # Documentation
│   ├── structure.md        # This file
│   └── api.md              # API endpoint documentation
│
├── ROADMAP.md              # Project roadmap and checklist
├── ROADMAP_SYNC.md         # GitHub Actions sync instructions
├── requirements.txt        # Python dependencies (for core and api)
└── README.md               # Main project overview
```

## Explanation of Layers

1. **`core/`**: This is a standalone Python package. It should not know anything about the database or the web server. It takes a URL as input and returns structured data (Python dictionaries or Pydantic models). It can be run purely from the terminal via `cli.py`.
2. **`api/`**: The FastAPI server. It imports the `core` package to perform scans, saves the results to an SQLite database, and serves HTTP endpoints for the web frontend to consume.
3. **`web/`**: The Next.js dashboard. It is completely isolated from the Python code. It communicates entirely by fetching data from the FastAPI endpoints (`GET`, `POST` to `api/`).
