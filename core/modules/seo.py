from bs4 import BeautifulSoup
from typing import Dict, Optional

def extract_standard_meta_tags(html_content: str) -> Dict[str, Optional[str]]:
    """
    Parses HTML content and extracts standard SEO meta tags.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    results = {
        'title': None,
        'description': None,
        'keywords': None,
        'author': None,
        'robots': None
    }
    
    # Extract Title
    title_tag = soup.find('title')
    if title_tag and title_tag.string:
        results['title'] = title_tag.string.strip()
        
    # Extract Meta Tags
    for meta in soup.find_all('meta'):
        name = meta.get('name', '').lower()
        content = meta.get('content', '')
        
        if name in ['description', 'keywords', 'author', 'robots'] and content:
            results[name] = content.strip()
            
    return results

def extract_social_meta_tags(html_content: str) -> Dict[str, Dict[str, str]]:
    """
    Parses HTML content and extracts Open Graph (OG) and Twitter Card meta tags.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    results = {'og': {}, 'twitter': {}}
    
    for meta in soup.find_all('meta'):
        property_attr = meta.get('property', '')
        name_attr = meta.get('name', '')
        content = meta.get('content', '')
        
        if content:
            if property_attr.startswith('og:'):
                key = property_attr.replace('og:', '')
                results['og'][key] = content.strip()
            elif name_attr.startswith('twitter:'):
                key = name_attr.replace('twitter:', '')
                results['twitter'][key] = content.strip()
                
    return results

def analyze_headings(html_content: str) -> Dict[str, any]:
    """
    Calculates heading metrics (H1, H2, H3 counts) and checks for missing H1.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    headings = {'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0}
    
    for h in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        headings[h] = len(soup.find_all(h))
        
    return {
        'counts': headings,
        'missing_h1': headings['h1'] == 0,
        'multiple_h1': headings['h1'] > 1
    }

def analyze_image_alts(html_content: str) -> Dict[str, any]:
    """
    Scans for <img> tags missing 'alt' attributes or with empty 'alt' values.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')
    
    total_images = len(images)
    missing_alt = 0
    missing_alt_urls = []
    
    for img in images:
        alt = img.get('alt')
        if alt is None or alt.strip() == '':
            missing_alt += 1
            src = img.get('src', 'unknown-source')
            missing_alt_urls.append(src)
            
    return {
        'total_images': total_images,
        'missing_alt': missing_alt,
        'missing_alt_urls': missing_alt_urls
    }

def analyze_text_ratio(html_content: str) -> Dict[str, any]:
    """
    Calculates the Text-to-HTML ratio and basic word count.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()
        
    text = soup.get_text()
    
    # Compress whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text_content = ' '.join(chunk for chunk in chunks if chunk)
    
    html_size = len(html_content)
    text_size = len(text_content)
    
    ratio = (text_size / html_size) * 100 if html_size > 0 else 0
    words = len(text_content.split())
    
    return {
        'html_size_bytes': html_size,
        'text_size_bytes': text_size,
        'text_to_html_ratio': round(ratio, 2),
        'word_count': words
    }

def extract_canonical(html_content: str) -> Optional[str]:
    """
    Extracts the canonical URL if present.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    canonical_tag = soup.find('link', rel='canonical')
    
    if canonical_tag and canonical_tag.get('href'):
        return canonical_tag.get('href').strip()
        
    return None

def check_robots_txt(base_url: str) -> Dict[str, any]:
    """
    Checks for the presence of a robots.txt file at the root.
    Note: Requires a network request. It's placed here for SEO context.
    """
    from urllib.parse import urlparse
    import requests
    
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    
    try:
        response = requests.get(robots_url, timeout=5)
        exists = response.status_code == 200
        
        return {
            'presence': exists,
            'url': robots_url,
            'status_code': response.status_code
        }
    except Exception:
        return {
            'presence': False,
            'url': robots_url,
            'status_code': 0
        }


