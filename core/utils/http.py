import requests
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError
from core.utils.logger import logger
from typing import Optional

def fetch_url(url: str, timeout: int = 10, headers: Optional[dict] = None) -> Optional[requests.Response]:
    """
    Fetches a URL with robust error handling and logging.
    Returns the requests.Response object if successful, or None if it fails.
    """
    default_headers = {
        'User-Agent': 'xwa-bot/1.0 (+https://github.com/your-repo/xwa)'
    }
    
    if headers:
        default_headers.update(headers)
        
    logger.debug(f"Fetching URL: {url}")
    
    try:
        response = requests.get(url, timeout=timeout, headers=default_headers)
        response.raise_for_status()  # Check for 4xx and 5xx errors
        logger.info(f"Successfully fetched {url} [Status: {response.status_code}]")
        return response
        
    except HTTPError as e:
        logger.error(f"HTTP Error for {url}: {e}")
    except ConnectionError as e:
        logger.error(f"Connection Error for {url}: {e}")
    except Timeout as e:
        logger.error(f"Timeout Error for {url} ({timeout}s): {e}")
    except RequestException as e:
        logger.error(f"Request Error fetching {url}: {e}")
    except Exception as e:
        logger.critical(f"Unexpected error fetching {url}: {e}")
        
    return None
