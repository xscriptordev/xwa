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

app = typer.Typer(help="xwa - Web Analysis & CLI Engine", no_args_is_help=True)

@app.command()
def scan(url: str):
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
    
    # TODO: Invoke other core analysis execution here

# Add a dummy command so Typer forces 'scan' to be a subcommand instead of the main script callback
@app.command()
def version():
    """Print the tool version."""
    typer.echo("xwa v0.1.0")

if __name__ == "__main__":
    app()
