import ssl
import socket
import asyncio
import aiohttp
from urllib.parse import urlparse
from typing import Dict, Any, List, Optional
from datetime import datetime
from core.utils.logger import logger

def analyze_security_headers(headers: Dict[str, str]) -> Dict[str, Any]:
    """Analyzes response headers for security best practices and leaked info."""
    # Convert headers to lowercase keys for easy lookup
    h = {k.lower(): v for k, v in headers.items()}
    
    security_headers = {
        'strict-transport-security': h.get('strict-transport-security'),
        'content-security-policy': h.get('content-security-policy'),
        'x-frame-options': h.get('x-frame-options'),
        'x-content-type-options': h.get('x-content-type-options'),
        'referrer-policy': h.get('referrer-policy'),
        'permissions-policy': h.get('permissions-policy')
    }
    
    leaked_info = {
        'server': h.get('server'),
        'x-powered-by': h.get('x-powered-by'),
        'x-aspnet-version': h.get('x-aspnet-version')
    }
    
    # Filter out None values for leaked info
    leaked_info = {k: v for k, v in leaked_info.items() if v is not None}
    
    missing_headers = [k for k, v in security_headers.items() if v is None]
    
    return {
        'headers_present': {k: v for k, v in security_headers.items() if v is not None},
        'missing_headers': missing_headers,
        'leaked_server_info': leaked_info,
        'score_penalty': len(missing_headers) * 10
    }

def analyze_ssl_certificate(url: str) -> Dict[str, Any]:
    """Connects to the host using sockets to extract and verify the SSL cert."""
    parsed = urlparse(url)
    hostname = parsed.hostname
    port = parsed.port or 443
    
    if not hostname or parsed.scheme != 'https':
        return {"valid": False, "error": "Not an HTTPS URL or invalid hostname."}
        
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # 'notAfter' format format: 'Oct 14 23:59:59 2024 GMT'
                expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_remaining = (expire_date - datetime.utcnow()).days
                
                issuer = dict(x[0] for x in cert['issuer'])
                subject = dict(x[0] for x in cert['subject'])
                
                return {
                    "valid": True,
                    "issuer": issuer.get('organizationName', issuer.get('commonName', 'Unknown')),
                    "subject": subject.get('commonName', hostname),
                    "days_remaining": days_remaining,
                    "expires_on": str(expire_date),
                    "is_expired": days_remaining < 0
                }
    except ssl.SSLCertVerificationError as e:
        return {"valid": False, "error": f"Certificate verification failed: {str(e)}"}
    except Exception as e:
        return {"valid": False, "error": f"SSL connection error: {str(e)}"}

def analyze_cookies(cookies: Dict[str, Any]) -> Dict[str, Any]:
    """Analyzes cookies for Secure, HttpOnly, and SameSite flags."""
    issues = []
    analyzed_cookies = []
    
    # Requests cookie jar translation
    for cookie in cookies:
        c_info = {
            "name": cookie.name,
            "secure": cookie.secure,
            "httponly": cookie.has_nonstandard_attr('HttpOnly') or 'HttpOnly' in cookie._rest,
            "samesite": cookie._rest.get('SameSite', 'Not Set') if hasattr(cookie, '_rest') else 'Not Set'
        }
        analyzed_cookies.append(c_info)
        
        if not c_info["secure"]:
            issues.append(f"Cookie '{cookie.name}' is missing 'Secure' flag.")
        if not c_info["httponly"]:
            issues.append(f"Cookie '{cookie.name}' is missing 'HttpOnly' flag.")
            
    return {
        "total": len(analyzed_cookies),
        "cookies": analyzed_cookies,
        "issues": issues
    }

SENSITIVE_PATHS = [
    '/.git/', '/.env', '/wp-admin/', '/phpinfo.php', 
    '/backup.zip', '/config.php.bak', '/.DS_Store'
]

async def check_sensitive_path(session: aiohttp.ClientSession, base_url: str, path: str) -> Optional[str]:
    """Checks a single sensitive path."""
    url = f"{base_url.rstrip('/')}{path}"
    try:
        async with session.head(url, allow_redirects=False, timeout=5) as response:
            if response.status in [200, 401, 403]:
                # 401/403 means it exists but is forbidden (which still confirms its presence)
                return f"{path} (HTTP {response.status})"
    except Exception:
        pass
    return None

async def brute_force_sensitive_paths(base_url: str) -> List[str]:
    """Concurrently scans for common sensitive directories and files."""
    found_paths = []
    
    async with aiohttp.ClientSession() as session:
        tasks = [check_sensitive_path(session, base_url, path) for path in SENSITIVE_PATHS]
        results = await asyncio.gather(*tasks)
        
        for res in results:
            if res:
                found_paths.append(res)
                
    return found_paths

def run_security_analysis(base_url: str, headers: Dict[str, str], cookies: Any) -> Dict[str, Any]:
    """Main execution entry point for Security module."""
    logger.info("Executing Security Analysis modules...")
    
    sec_headers = analyze_security_headers(headers)
    ssl_info = analyze_ssl_certificate(base_url)
    cookie_info = analyze_cookies(cookies)
    
    logger.info("Brute forcing sensitive paths in background (async)...")
    sensitive_paths = asyncio.run(brute_force_sensitive_paths(base_url))
    
    return {
        "headers": sec_headers,
        "ssl": ssl_info,
        "cookies": cookie_info,
        "sensitive_paths_found": sensitive_paths
    }
