import os
from pathlib import Path
from .sqlite_data_layer import SQLiteFriendlyDataLayer

DB_PATH = os.getenv("CHAINLIT_DB_PATH", "./chatbot.db")

_data_layer_instance = None

def get_data_layer() -> SQLiteFriendlyDataLayer:
    global _data_layer_instance
    
    if _data_layer_instance is None:
        db_file = Path(DB_PATH)
        conninfo = f"sqlite+aiosqlite:///{db_file.absolute()}"
        
        _data_layer_instance = SQLiteFriendlyDataLayer(
            conninfo=conninfo,
            ssl_require=False,
            show_logger=False
        )
    
    return _data_layer_instance
