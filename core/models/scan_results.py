from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class SEOResults(BaseModel):
    standard_meta: Dict[str, Optional[str]] = Field(default_factory=dict)
    social_meta: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    headings: Dict[str, Any] = Field(default_factory=dict)
    image_alts: Dict[str, Any] = Field(default_factory=dict)
    text_ratio: Dict[str, Any] = Field(default_factory=dict)
    canonical: Optional[str] = None
    robots_txt: Dict[str, Any] = Field(default_factory=dict)

class SitemapResults(BaseModel):
    urls_found: int = 0
    scanned_count: int = 0
    broken_links: List[Dict[str, Any]] = Field(default_factory=list)

class SecurityResults(BaseModel):
    headers: Dict[str, Any] = Field(default_factory=dict)
    ssl: Dict[str, Any] = Field(default_factory=dict)
    cookies: Dict[str, Any] = Field(default_factory=dict)
    sensitive_paths_found: List[str] = Field(default_factory=list)

class FullScanReport(BaseModel):
    target_url: str
    scan_timestamp: str
    seo: SEOResults
    sitemap: SitemapResults
    security: SecurityResults
    
    def serialize(self) -> Dict[str, Any]:
        """Unified serialization down to primitive dictionaries."""
        return self.model_dump()
