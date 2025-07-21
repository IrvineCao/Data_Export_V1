from pathlib import Path
from utils.helpers import trace_function_call

def _get_query_from_file(file_path: str) -> str:
    """Helper function to read SQL file safely."""
    path = Path(__file__).parent / "sql" / file_path
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "" 

query_params = {
    "count": _get_query_from_file("keyword_lab_count.sql"),
    "data": _get_query_from_file("keyword_lab_data.sql"),
}

@trace_function_call
def get_query(query_name: str) -> str:
    """Gets a query by name from the pre-loaded dictionary."""
    return query_params.get(query_name, "")