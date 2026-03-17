import logging
import sys

def setup_logger(name: str = "xwa_core", level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a standard logger for the application.
    Outputs to standard output with a specific format.
    """
    logger = logging.getLogger(name)
    
    # Only configure if it doesn't have handlers yet to prevent duplicate logs
    if not logger.handlers:
        logger.setLevel(level)
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        
    return logger

# Default logger instance
logger = setup_logger()
