from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from sqlmodel import Session
from api.db.database import get_session
from api.db.models import ScanRecord
from core.models.scan_results import FullScanReport, SEOResults, SitemapResults, SecurityResults
from core.modules.security import run_security_analysis
from core.modules.sitemap import run_sitemap_analysis
from core.modules.seo import (
    extract_standard_meta_tags,
    extract_social_meta_tags,
    analyze_headings,
    analyze_image_alts,
    analyze_text_ratio,
    extract_canonical,
    check_robots_txt
)
from core.utils.http import fetch_url
from datetime import datetime
import asyncio
from pydantic import BaseModel

router = APIRouter()

class ScanRequest(BaseModel):
    url: str

# Simple in-memory tracker for SSE (for a real app use Redis)
scan_progress = {}

def sync_core_execution(url: str, session: Session, scan_id: int):
    """Executes the entire core analysis pipeline synchronously and saves it to DB."""
    try:
        scan_progress[scan_id] = "Connecting to target..."
        response = fetch_url(url)
        if not response:
            scan_progress[scan_id] = "Error: Connection Failed"
            return
            
        scan_progress[scan_id] = "Running SEO Analysis..."
        html_content = response.text
        
        standard_meta = extract_standard_meta_tags(html_content)
        social_meta = extract_social_meta_tags(html_content)
        headings = analyze_headings(html_content)
        alts = analyze_image_alts(html_content)
        ratio = analyze_text_ratio(html_content)
        canonical = extract_canonical(html_content)
        robots = check_robots_txt(url)
        
        scan_progress[scan_id] = "Running Sitemap & Crawler Analysis..."
        sitemap_results = run_sitemap_analysis(url)
        
        scan_progress[scan_id] = "Running Security Analysis..."
        security_results = run_security_analysis(url, response.headers, response.cookies)
        
        scan_progress[scan_id] = "Formatting Final Report..."
        
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
        
        # Save to DB
        scan_record = session.get(ScanRecord, scan_id)
        if scan_record:
            scan_record.urls_found = sitemap_results["urls_found"]
            scan_record.broken_links_count = len(sitemap_results["broken_links"])
            scan_record.missing_security_headers = len(security_results["headers"]["missing_headers"])
            scan_record.is_ssl_valid = security_results["ssl"].get("valid", False)
            scan_record.raw_results = report.serialize()
            
            session.add(scan_record)
            session.commit()
            
        scan_progress[scan_id] = "Completed"
        
    except Exception as e:
        scan_progress[scan_id] = f"Error: {str(e)}"

@router.post("/scan")
def trigger_scan(req: ScanRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_session)):
    """Receives target URLs and triggers the core engine."""
    
    nuevo_scan = ScanRecord(target_url=req.url)
    db.add(nuevo_scan)
    db.commit()
    db.refresh(nuevo_scan)
    
    scan_id = nuevo_scan.id
    scan_progress[scan_id] = "Initiating scan..."
    
    background_tasks.add_task(sync_core_execution, req.url, db, scan_id)
    
    return {"message": "Scan started.", "scan_id": scan_id}
