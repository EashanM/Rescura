import logging
from pathlib import Path
from datetime import datetime

def setup_logging() -> None:
    """Configure application-wide logging"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    log_file = logs_dir / f"rescura_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logging.captureWarnings(True)
