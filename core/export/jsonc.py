import json
import os
from datetime import datetime
from typing import Dict, Any

def export_jsonc(data: Dict[str, Any], output_path: str) -> str:
    """
    Exports dictionary data into a JSONC file (JSON with Comments).
    """
    if not output_path.endswith('.jsonc'):
        output_path += '.jsonc'
        
    # Serialize the data
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    
    # Insert comments manually representing JSONC structure
    header_comment = f"// xwa - Web Analysis & SEO Dashboard\n// Target: {data.get('target_url')}\n// Generated at: {datetime.utcnow().isoformat()}Z\n"
    
    jsonc_content = header_comment + json_str
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(jsonc_content)
        
    return output_path
