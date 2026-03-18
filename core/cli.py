import typer
from core.utils.logger import logger
from core.utils.http import fetch_url
from core.modules.seo import (
    extract_standard_meta_tags,
    extract_social_meta_tags,
    analyze_headings,
    analyze_image_alts,
    analyze_text_ratio,
    extract_canonical,
    check_robots_txt
)
from core.modules.sitemap import run_sitemap_analysis
from core.modules.security import run_security_analysis
from core.models.scan_results import FullScanReport, SEOResults, SitemapResults, SecurityResults
from core.export.jsonc import export_jsonc
from core.export.markdown import export_markdown
from datetime import datetime
from typing import Optional

app = typer.Typer(help="xwa - Web Analysis & CLI Engine", no_args_is_help=True)

@app.command()
def scan(
    url: str,
    jsonc: Optional[str] = typer.Option(None, "--jsonc", help="Path to export the JSONC report"),
    md: Optional[str] = typer.Option(None, "--md", help="Path to export the Markdown report")
):
    """
    Run a full analysis (SEO, Sitemap, Security) on a target URL.
    """
    typer.echo(f"Initializing scan for target: {url}")
    logger.info(f"Starting scan process for {url}")
    
    response = fetch_url(url)
    if not response:
        logger.error("Scan aborted due to initial connection failure.")
        raise typer.Exit(code=1)
        
    logger.info("Target is reachable. Proceeding with SEO analysis...")
    
    # 1. SEO Module
    html_content = response.text
    
    logger.info("-> Extracting Standard Meta Tags...")
    standard_meta = extract_standard_meta_tags(html_content)
    logger.info(f"Results: {standard_meta}")
    
    logger.info("-> Extracting Social Meta Tags...")
    social_meta = extract_social_meta_tags(html_content)
    logger.info(f"Results: {social_meta}")
    
    logger.info("-> Analyzing Headings (H1-H6)...")
    headings = analyze_headings(html_content)
    logger.info(f"Results: {headings}")
    
    logger.info("-> Analyzing Image Alt Attributes...")
    alts = analyze_image_alts(html_content)
    logger.info(f"Results: total={alts['total_images']}, missing={alts['missing_alt']}")
    
    logger.info("-> Analyzing Text-to-HTML Ratio...")
    ratio = analyze_text_ratio(html_content)
    logger.info(f"Results: {ratio}")
    
    logger.info("-> Checking Canonical URL...")
    canonical = extract_canonical(html_content)
    logger.info(f"Results: {canonical}")
    
    logger.info("-> Checking robots.txt presence...")
    robots = check_robots_txt(url)
    logger.info(f"Results: {robots}")
    
    # 2. Sitemap Module
    logger.info("--------------------------------------------------")
    logger.info("Starting Sitemap & Crawler Analysis...")
    logger.info("--------------------------------------------------")
    sitemap_results = run_sitemap_analysis(url)
    logger.info(f"Sitemap Results: URLs found={sitemap_results['urls_found']}, Broken Links={len(sitemap_results['broken_links'])}")
    
    # 3. Security Module
    logger.info("--------------------------------------------------")
    logger.info("Starting Security Analysis...")
    logger.info("--------------------------------------------------")
    
    # Passing the headers and cookies from the initial Requests response
    security_results = run_security_analysis(url, response.headers, response.cookies)
    
    logger.info(f"Security Headers Missing: {len(security_results['headers']['missing_headers'])}")
    logger.info(f"Leaked Server Info: {security_results['headers']['leaked_server_info']}")
    logger.info(f"SSL Valid: {security_results['ssl'].get('valid', False)}")
    
    if security_results['ssl'].get('valid'):
        logger.info(f"SSL Days Remaining: {security_results['ssl'].get('days_remaining')}")
        
    logger.info(f"Cookie Issues: {len(security_results['cookies']['issues'])}")
    logger.info(f"Sensitive Paths Found: {len(security_results['sensitive_paths_found'])}")
    if security_results['sensitive_paths_found']:
        logger.warning(f"PATHS EXPOSED: {security_results['sensitive_paths_found']}")
        
    # 4. Export & Serialization
    logger.info("--------------------------------------------------")
    logger.info("Building Full Report...")
    logger.info("--------------------------------------------------")
    
    report = FullScanReport(
        target_url=url,
        scan_timestamp=datetime.utcnow().isoformat() + "Z",
        seo=SEOResults(
            standard_meta=standard_meta,
            social_meta=social_meta,
            headings=headings,
            image_alts=alts,
            text_ratio=ratio,
            canonical=canonical,
            robots_txt=robots
        ),
        sitemap=SitemapResults(**sitemap_results),
        security=SecurityResults(**security_results)
    )
    
    serialized_data = report.serialize()
    
    if jsonc:
        out_path = export_jsonc(serialized_data, jsonc)
        logger.info(f"JSONC Report saved to: {out_path}")
        
    if md:
        out_path = export_markdown(serialized_data, md)
        logger.info(f"Markdown Report saved to: {out_path}")
        
    logger.info("Analysis Complete.")

# Add a dummy command so Typer forces 'scan' to be a subcommand instead of the main script callback
@app.command()
def version():
    """Print the tool version."""
    typer.echo("xwa v0.1.0")

if __name__ == "__main__":
    app()
