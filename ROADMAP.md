# Web Analysis & SEO Dashboard - Roadmap

This document outlines the step-by-step development plan for the project, separated into detailed phases. Progress marked in this file will automatically sync with GitHub Issues.

## Phase 1: Project Setup & Core CLI <!-- phase:project-setup -->

- [ ] Initialize the project repository and set up version control conventions. (#1)
- [ ] Define the base directory structure (separating core engine, api, and web frontend). (#2)
- [ ] Set up Python virtual environment and basic dependencies (e.g., `requests`, `beautifulsoup4`). (#3)
- [ ] Create a basic Command Line Interface (CLI) entry point using `argparse` or `Typer`. (#4)
- [ ] Implement robust error handling for HTTP requests and invalid URLs in the core engine. (#5)
- [ ] Set up standard logging configuration for the core engine execution. (#6)

## Phase 2: SEO Analysis Engine <!-- phase:seo-engine -->

- [ ] Implement extractor for standard meta tags (Title, Description, Keywords). (#7)
- [ ] Implement extractor for Open Graph (OG) and Twitter Card meta tags. (#8)
- [ ] Create a module to analyze header tag hierarchy (H1, H2, H3) and detect missing H1s. (#9)
- [ ] Implement a checker for missing `alt` attributes on image tags. (#10)
- [ ] Analyze text-to-HTML ratio and calculate basic word count statistics. (#11)
- [ ] Create a module to check for robots.txt presence and basic allow/disallow rules. (#12)
- [ ] Implement canonical URL verification. (#13)

## Phase 3: Sitemap & Crawler Module <!-- phase:sitemap-crawler -->

- [ ] Implement function to automatically locate and download `sitemap.xml` (or `sitemap_index.xml`). (#14)
- [ ] Parse XML content to extract all listed URLs efficiently. (#15)
- [ ] Implement a concurrent HTTP crawler (e.g., using `asyncio` and `aiohttp`) to validate URL status codes. (#16)
- [ ] Detect and report broken links (404s) and redirect chains (301/302). (#17)
- [ ] Develop an algorithm to transform a flat list of URL paths into a hierarchical tree structure. (#18)
- [ ] Implement rate limiting and sensible timeouts to avoid overloading target servers. (#19)

## Phase 4: Security Analysis Module <!-- phase:security-engine -->

- [ ] Scanner for missing or misconfigured security headers (CORS, HSTS, X-Frame-Options, CSP). (#20)
- [ ] Implement basic SSL/TLS certificate analysis (expiration date, issuer, validation status). (#21)
- [ ] Create a passive directory brute-forcer to detect common sensitive paths (`/.git/`, `/.env`, `/wp-admin/`, etc.). (#22)
- [ ] Detect leaked server information headers (e.g., `X-Powered-By`, `Server`). (#23)
- [ ] Check for basic cookie security flags (`HttpOnly`, `Secure`, `SameSite`). (#24)

## Phase 5: Export & Serialization Engine <!-- phase:export-engine -->

- [ ] Define standardized internal data classes (e.g., Pydantic models) to hold all analysis results. (#25)
- [ ] Create a unified serializer that converts internal data models to primitive Python dictionaries. (#26)
- [ ] Implement JSONC (JSON with Comments) formatting and file generation. (#27)
- [ ] Develop a Markdown (MD) report generator using Jinja2 templates or string formatting. (#28)
- [ ] Add CLI flags to specify output formats and export destination paths. (#29)

## Phase 6: Backend API Configuration (FastAPI) <!-- phase:api-setup -->

- [ ] Initialize the FastAPI application structure within the project. (#30)
- [ ] Configure standard middlewares (CORS for Next.js frontend frontend, GZip). (#31)
- [ ] Set up SQLite database connection using SQLAlchemy or SQLModel. (#32)
- [ ] Define database schema and ORM models (Analyses, URLs, SEO Results, Security Results). (#33)
- [ ] Implement Alembic for database migrations. (#34)

## Phase 7: API Endpoints & Background Tasks <!-- phase:api-endpoints -->

- [ ] Create `POST /api/scan` endpoint to receive target URLs and trigger the core engine. (#35)
- [ ] Implement background task processing (e.g., Celery, RQ, or FastAPI `BackgroundTasks`) for long-running scans. (#36)
- [ ] Create endpoints for WebSocket or Server-Sent Events (SSE) to stream live scan progress to the frontend. (#37)
- [ ] Create `GET /api/reports/{id}` endpoint to fetch the complete JSON results of a specific scan. (#38)
- [ ] Create `GET /api/reports` endpoint with pagination to list scan history. (#39)
- [ ] Implement direct download endpoints for generated MD and JSONC files (e.g., `/api/export/md/{id}`). (#40)

## Phase 8: Web Frontend Setup (Next.js) <!-- phase:frontend-setup -->

- [ ] Initialize Next.js (App Router) project with TypeScript and TailwindCSS. (#41)
- [ ] Install and configure Shadcn/UI (or similar Radix-based component library). (#42)
- [ ] Define the global design system, color tokens, and dark/light mode functionality. (#43)
- [ ] Design and implement the primary application Shell (sidebar navigation, header, layout). (#44)
- [ ] Configure API client (e.g., Axios or native fetch) for communicating with the FastAPI backend. (#45)

## Phase 9: Web Frontend Features & Views <!-- phase:frontend-features -->

- [ ] Implement the Home Dashboard view with a main input field for initiating new site scans. (#46)
- [ ] Develop interactive loading states and progress bars using real-time data from the API. (#47)
- [ ] Build the "Scan Summary" component showing overall scores and high-level metrics. (#48)
- [ ] Create the "SEO Dashboard" tab with specific cards for missing tags, headings structure, and warnings. (#49)
- [ ] Implement the "Sitemap Visualizer" tab using a library like D3.js or react-flow to render the route tree. (#50)
- [ ] Build the "Vulnerabilities" tab with data tables detailing security headers and sensitive path findings. (#51)
- [ ] Add download buttons securely linked to the API export endpoints (JSONC & Markdown). (#52)
- [ ] Build the "Scan History" page to list and filter previous analyses. (#53)

## Phase 10: Local Multiplatform Tooling <!-- phase:local-tooling -->

- [ ] Research and initialize a Terminal UI (TUI) library for Python (e.g., `Textual` or `Rich`). (#54)
- [ ] Port the core CLI functionality to the TUI, creating visually distinct panes for SEO, Security, and Sitemaps natively in the terminal. (#55)
- [ ] Configure PyInstaller, Nuitka, or PyOxidizer to package the Python engine into a single executable binary. (#56)
- [ ] Automate build processes for cross-compiling the binary for Linux, Windows, and macOS. (#57)
- [ ] Write comprehensive installation and usage documentation for running the tool locally without the web dashboard. (#58)
- [ ] Explore native GUI alternatives (e.g., PyQt/PySide6) for a standalone desktop application experience. (#59)
