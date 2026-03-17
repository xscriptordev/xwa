# Web Analysis & SEO Dashboard - Roadmap

This document outlines the step-by-step development plan for the project, separated into detailed phases. Progress marked in this file will automatically sync with GitHub Issues.

## Phase 1: Project Setup & Core CLI <!-- phase:project-setup -->

- [ ] Initialize the project repository and set up version control conventions.
- [ ] Define the base directory structure (separating core engine, api, and web frontend).
- [ ] Set up Python virtual environment and basic dependencies (e.g., `requests`, `beautifulsoup4`).
- [ ] Create a basic Command Line Interface (CLI) entry point using `argparse` or `Typer`.
- [ ] Implement robust error handling for HTTP requests and invalid URLs in the core engine.
- [ ] Set up standard logging configuration for the core engine execution.

## Phase 2: SEO Analysis Engine <!-- phase:seo-engine -->

- [ ] Implement extractor for standard meta tags (Title, Description, Keywords).
- [ ] Implement extractor for Open Graph (OG) and Twitter Card meta tags.
- [ ] Create a module to analyze header tag hierarchy (H1, H2, H3) and detect missing H1s.
- [ ] Implement a checker for missing `alt` attributes on image tags.
- [ ] Analyze text-to-HTML ratio and calculate basic word count statistics.
- [ ] Create a module to check for robots.txt presence and basic allow/disallow rules.
- [ ] Implement canonical URL verification.

## Phase 3: Sitemap & Crawler Module <!-- phase:sitemap-crawler -->

- [ ] Implement function to automatically locate and download `sitemap.xml` (or `sitemap_index.xml`).
- [ ] Parse XML content to extract all listed URLs efficiently.
- [ ] Implement a concurrent HTTP crawler (e.g., using `asyncio` and `aiohttp`) to validate URL status codes.
- [ ] Detect and report broken links (404s) and redirect chains (301/302).
- [ ] Develop an algorithm to transform a flat list of URL paths into a hierarchical tree structure.
- [ ] Implement rate limiting and sensible timeouts to avoid overloading target servers.

## Phase 4: Security Analysis Module <!-- phase:security-engine -->

- [ ] Scanner for missing or misconfigured security headers (CORS, HSTS, X-Frame-Options, CSP).
- [ ] Implement basic SSL/TLS certificate analysis (expiration date, issuer, validation status).
- [ ] Create a passive directory brute-forcer to detect common sensitive paths (`/.git/`, `/.env`, `/wp-admin/`, etc.).
- [ ] Detect leaked server information headers (e.g., `X-Powered-By`, `Server`).
- [ ] Check for basic cookie security flags (`HttpOnly`, `Secure`, `SameSite`).

## Phase 5: Export & Serialization Engine <!-- phase:export-engine -->

- [ ] Define standardized internal data classes (e.g., Pydantic models) to hold all analysis results.
- [ ] Create a unified serializer that converts internal data models to primitive Python dictionaries.
- [ ] Implement JSONC (JSON with Comments) formatting and file generation.
- [ ] Develop a Markdown (MD) report generator using Jinja2 templates or string formatting.
- [ ] Add CLI flags to specify output formats and export destination paths.

## Phase 6: Backend API Configuration (FastAPI) <!-- phase:api-setup -->

- [ ] Initialize the FastAPI application structure within the project.
- [ ] Configure standard middlewares (CORS for Next.js frontend frontend, GZip).
- [ ] Set up SQLite database connection using SQLAlchemy or SQLModel.
- [ ] Define database schema and ORM models (Analyses, URLs, SEO Results, Security Results).
- [ ] Implement Alembic for database migrations.

## Phase 7: API Endpoints & Background Tasks <!-- phase:api-endpoints -->

- [ ] Create `POST /api/scan` endpoint to receive target URLs and trigger the core engine.
- [ ] Implement background task processing (e.g., Celery, RQ, or FastAPI `BackgroundTasks`) for long-running scans.
- [ ] Create endpoints for WebSocket or Server-Sent Events (SSE) to stream live scan progress to the frontend.
- [ ] Create `GET /api/reports/{id}` endpoint to fetch the complete JSON results of a specific scan.
- [ ] Create `GET /api/reports` endpoint with pagination to list scan history.
- [ ] Implement direct download endpoints for generated MD and JSONC files (e.g., `/api/export/md/{id}`).

## Phase 8: Web Frontend Setup (Next.js) <!-- phase:frontend-setup -->

- [ ] Initialize Next.js (App Router) project with TypeScript and TailwindCSS.
- [ ] Install and configure Shadcn/UI (or similar Radix-based component library).
- [ ] Define the global design system, color tokens, and dark/light mode functionality.
- [ ] Design and implement the primary application Shell (sidebar navigation, header, layout).
- [ ] Configure API client (e.g., Axios or native fetch) for communicating with the FastAPI backend.

## Phase 9: Web Frontend Features & Views <!-- phase:frontend-features -->

- [ ] Implement the Home Dashboard view with a main input field for initiating new site scans.
- [ ] Develop interactive loading states and progress bars using real-time data from the API.
- [ ] Build the "Scan Summary" component showing overall scores and high-level metrics.
- [ ] Create the "SEO Dashboard" tab with specific cards for missing tags, headings structure, and warnings.
- [ ] Implement the "Sitemap Visualizer" tab using a library like D3.js or react-flow to render the route tree.
- [ ] Build the "Vulnerabilities" tab with data tables detailing security headers and sensitive path findings.
- [ ] Add download buttons securely linked to the API export endpoints (JSONC & Markdown).
- [ ] Build the "Scan History" page to list and filter previous analyses.

## Phase 10: Local Multiplatform Tooling <!-- phase:local-tooling -->

- [ ] Research and initialize a Terminal UI (TUI) library for Python (e.g., `Textual` or `Rich`).
- [ ] Port the core CLI functionality to the TUI, creating visually distinct panes for SEO, Security, and Sitemaps natively in the terminal.
- [ ] Configure PyInstaller, Nuitka, or PyOxidizer to package the Python engine into a single executable binary.
- [ ] Automate build processes for cross-compiling the binary for Linux, Windows, and macOS.
- [ ] Write comprehensive installation and usage documentation for running the tool locally without the web dashboard.
- [ ] Explore native GUI alternatives (e.g., PyQt/PySide6) for a standalone desktop application experience.
