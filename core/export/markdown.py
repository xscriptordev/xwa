import os
from typing import Dict, Any

def export_markdown(data: Dict[str, Any], output_path: str) -> str:
    """
    Exports dictionary data (from FullScanReport) into a styled Markdown report.
    """
    if not output_path.endswith('.md'):
        output_path += '.md'
        
    url = data.get('target_url', 'Unknown')
    time = data.get('scan_timestamp', 'Unknown')
    
    seo = data.get('seo', {})
    sitemap = data.get('sitemap', {})
    security = data.get('security', {})
    
    md = f"""# 📊 xwa - Web Analysis Report

**Target URL:** `{url}`
**Scan Timestamp:** `{time}`

---

## 🔍 1. SEO Analysis

### Standard Meta Tags
- **Title:** {seo.get('standard_meta', {}).get('title', 'N/A')}
- **Description:** {seo.get('standard_meta', {}).get('description', 'N/A')}

### Content & Structure
- **Word Count:** {seo.get('text_ratio', {}).get('word_count', 0)}
- **Text-to-HTML Ratio:** {seo.get('text_ratio', {}).get('text_to_html_ratio', 0)}%
- **Missing Image Alts:** {seo.get('image_alts', {}).get('missing_alt', 0)} / {seo.get('image_alts', {}).get('total_images', 0)}
- **H1 Tags:** {seo.get('headings', {}).get('counts', {}).get('h1', 0)}

---

## 🗺️ 2. Sitemap & Crawler

- **URLs Found in Sitemap:** {sitemap.get('urls_found', 0)}
- **URLs Scanned:** {sitemap.get('scanned_count', 0)}
- **Broken Links (404/5xx):** {len(sitemap.get('broken_links', []))}

"""
    if sitemap.get('broken_links'):
        md += "### Broken Links List\n"
        for link in sitemap['broken_links']:
            md += f"- `{link['url']}` (Status: {link.get('status')})\n"

    md += f"""
---

## 🛡️ 3. Security Analysis

### SSL / TLS
- **Valid:** {security.get('ssl', {}).get('valid', False)}
- **Issuer:** {security.get('ssl', {}).get('issuer', 'Unknown')}
- **Days Remaining:** {security.get('ssl', {}).get('days_remaining', 'Unknown')}

### Security Headers
- **Missing Important Headers:** {len(security.get('headers', {}).get('missing_headers', []))}
"""
    if security.get('headers', {}).get('missing_headers'):
        md += "  - " + ", ".join(security['headers']['missing_headers']) + "\n"

    md += f"""
### Sensitive Paths Exposed
{len(security.get('sensitive_paths_found', []))} paths exposed.
"""
    for path in security.get('sensitive_paths_found', []):
        md += f"- ⚠️ `{path}`\n"
        
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)
        
    return output_path
