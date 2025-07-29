import streamlit as st
import pandas as pd
from io import StringIO
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError
from utils.core.database import get_connection
from utils.core.helpers import trace_function_call
import importlib
from utils.ui.input_config import DATA_SOURCE_CONFIGS
from utils.config import PROJECT_ROOT



def get_query_by_source(data_source: str):
    """
    Dynamically import and return the get_query function based on the data source config.
    
    NEW: Falls back to convention-based SQL file reading if module doesn't exist.
    """
    config = DATA_SOURCE_CONFIGS.get(data_source)
    if not config or 'data_logic_module' not in config:
        raise ValueError(f"Unknown or misconfigured data source: {data_source}")

    module_name = config['data_logic_module']
    
    try:
        # 🔄 Try to import existing module first (backward compatibility)
        data_logic_module = importlib.import_module(f"data_logic.{module_name}")
        get_query_func = getattr(data_logic_module, 'get_query')
        
        # 📝 Log that we're using existing module
        if hasattr(st, 'session_state') and 'debug_mode' in st.session_state:
            st.info(f"✅ Using existing module: data_logic.{module_name}")
        
        return get_query_func
        
    except (ImportError, AttributeError) as e:
        # 🚀 NEW: If module doesn't exist, create convention-based query function
        if hasattr(st, 'session_state') and 'debug_mode' in st.session_state:
            st.info(f"⚡ Auto-generating query function for: {data_source}")
            st.info(f"   Module not found: data_logic.{module_name}")
            st.info(f"   Using convention-based SQL file reading")
        
        return create_convention_based_query_func(data_source)


def create_convention_based_query_func(data_source: str):
    """
    🚀 NEW: Create a query function based on SQL file naming convention.
    
    Convention:
    - data_logic/sql/{data_source}_data.sql -> get_query("data")
    - data_logic/sql/{data_source}_count.sql -> get_query("count")
    
    Args:
        data_source: The data source key (e.g., "sales_analytics")
    
    Returns:
        A get_query function that reads SQL files directly
    """
    def get_query(query_name: str) -> str:
        """
        Get SQL query content based on naming convention.
        
        Args:
            query_name: Either "data" or "count"
        
        Returns:
            SQL query string
        """
        # 📁 Map query names to SQL file names
        sql_file_map = {
            "data": f"{data_source}_data.sql",
            "count": f"{data_source}_count.sql"
        }
        
        file_name = sql_file_map.get(query_name)
        if not file_name:
            st.error(f"❌ Unknown query type: {query_name}. Expected 'data' or 'count'")
            return ""
        
        # 📂 Construct file path
        sql_file_path = PROJECT_ROOT / "data_logic" / "sql" / file_name
        
        try:
            # 📖 Read SQL file content
            with open(sql_file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # 📝 Debug logging
            if hasattr(st, 'session_state') and 'debug_mode' in st.session_state:
                st.success(f"✅ Read SQL file: {file_name}")
                st.code(f"File path: {sql_file_path}", language="text")
                if len(sql_content) > 200:
                    st.code(f"SQL preview: {sql_content[:200]}...", language="sql")
                else:
                    st.code(f"SQL content: {sql_content}", language="sql")
            
            return sql_content
            
        except FileNotFoundError as e:
            error_msg = f"❌ SQL file not found: {file_name}"
            st.error(error_msg)
            st.error(f"Expected path: {sql_file_path}")
            st.info("💡 **Convention-based file naming:**")
            st.info(f"   • {data_source}_data.sql - Main query")
            st.info(f"   • {data_source}_count.sql - Count query")
            
            # 📋 Show available SQL files for debugging
            sql_dir = PROJECT_ROOT / "data_logic" / "sql"
            if sql_dir.exists():
                available_files = [f.name for f in sql_dir.glob("*.sql")]
                if available_files:
                    st.info(f"📁 Available SQL files: {', '.join(available_files[:10])}")
                    if len(available_files) > 10:
                        st.info(f"   ... and {len(available_files) - 10} more")
            
            return ""
            
        except Exception as e:
            st.error(f"❌ Error reading SQL file {file_name}: {str(e)}")
            return ""
    
    return get_query


def validate_convention_based_setup(data_source: str) -> bool:
    """
    🔍 Validate that convention-based setup is correct for a data source.
    
    Args:
        data_source: The data source key
    
    Returns:
        True if setup is valid, False otherwise
    """
    sql_dir = PROJECT_ROOT / "data_logic" / "sql"
    required_files = [
        f"{data_source}_data.sql",
        f"{data_source}_count.sql"
    ]
    
    missing_files = []
    for file_name in required_files:
        file_path = sql_dir / file_name
        if not file_path.exists():
            missing_files.append(file_name)
    
    if missing_files:
        st.error(f"❌ Missing SQL files for '{data_source}':")
        for file_name in missing_files:
            st.error(f"   • {file_name}")
        st.info("💡 Create these files in: data_logic/sql/")
        return False
    
    st.success(f"✅ Convention-based setup valid for '{data_source}'")
    return True


def list_available_data_sources():
    """
    📋 Debug helper: List all available data sources and their status.
    """
    st.subheader("🔍 Available Data Sources")
    
    for data_source, config in DATA_SOURCE_CONFIGS.items():
        with st.expander(f"📊 {config.get('name', data_source)}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Configuration:**")
                st.json({
                    "data_source_key": data_source,
                    "module": config.get('data_logic_module'),
                    "inputs": config.get('inputs', [])
                })
            
            with col2:
                st.write("**Status:**")
                
                # Check if existing module exists
                module_name = config.get('data_logic_module')
                try:
                    importlib.import_module(f"data_logic.{module_name}")
                    st.success("✅ Existing module found")
                    module_status = "existing"
                except ImportError:
                    st.info("⚡ Will use convention-based")
                    module_status = "convention"
                
                # Check SQL files for convention-based
                if module_status == "convention":
                    validate_convention_based_setup(data_source)


# 🚀 NEW: Debug mode toggle
def enable_debug_mode():
    """Enable debug mode to see convention-based loading in action."""
    st.session_state.debug_mode = True
    st.success("🔧 Debug mode enabled! You'll see detailed logs for convention-based loading.")


def disable_debug_mode():
    """Disable debug mode."""
    if 'debug_mode' in st.session_state:
        del st.session_state.debug_mode
    st.info("🔇 Debug mode disabled.")


# === REST OF THE FILE UNCHANGED ===

@st.cache_data(show_spinner=False, ttl=3600, persist=True)
def _execute_query(query: str, params_to_bind: dict) -> pd.DataFrame:
    print("--- DEBUG: EXECUTING QUERY ---")
    print(f"Query: {query}")
    print(f"Params: {params_to_bind}")
    print("-----------------------------")
    with get_connection() as db:
        return pd.read_sql(text(query), db.connection(), params=params_to_bind)


@trace_function_call
@st.cache_data(show_spinner=False, ttl=3600, persist=True)
def get_data(query_type: str, data_source: str, limit: int = None, **kwargs):
    """
    Fetches data from the DB.
    
    Now supports both existing modules and convention-based SQL file reading.
    """
    get_query_func = get_query_by_source(data_source)
    base_query_str = get_query_func(query_type)
    
    params_to_bind = kwargs.copy()

    # SQLAlchemy's text() construct doesn't natively support expanding a list for an IN clause when used with pandas.read_sql.
    # To work around this, we safely format the list of integer IDs directly into the SQL string.
    # This is safe from SQL injection because we explicitly cast all IDs to integers first.
    if 'storefront_ids' in params_to_bind and isinstance(params_to_bind['storefront_ids'], (list, tuple)) and ':storefront_ids' in base_query_str:
        storefront_ids = params_to_bind['storefront_ids']
        
        safe_ids = [int(sid) for sid in storefront_ids]
        
        if len(safe_ids) == 1:
            ids_string = f"({safe_ids[0]})"
        else:
            ids_string = str(tuple(safe_ids))

        base_query_str = base_query_str.replace(':storefront_ids', ids_string)
        
        del params_to_bind['storefront_ids']    
    elif 'storefront_ids' in params_to_bind:
        # Clean up storefront_ids if they are not needed in the query to avoid sending them to the DB driver
        del params_to_bind['storefront_ids']

    if limit is not None and query_type == 'data':
        final_query_str = f"{base_query_str} LIMIT {limit}"
    else:
        final_query_str = base_query_str
    
    query = text(final_query_str)
    
    with get_connection() as db:
        return pd.read_sql(query, db.connection(), params=params_to_bind)


@trace_function_call
def load_data(data_source: str, limit: int = None):
    """Load data based on parameters in the session state."""
    try:
        params = st.session_state.get('params', {}).copy()
        if not params:
            return None

        # Parameters are already built, just remove non-SQL keys
        params.pop('data_source', None)
        params.pop('current_page', None)  # Remove page info but keep data_source in session
        params.pop('num_row', None)  # Remove row count info
        sql_params = params

        df = get_data("data", data_source, limit=limit, **sql_params)
        st.session_state.df = df
        return df
    except Exception as e:
        st.error(f"An error occurred while loading data: {str(e)}")
        return None


@trace_function_call
def get_row_count(data_source: str, **kwargs) -> int:
    """Get the total row count."""
    try:
        params = kwargs.copy()
        if not params:
            return None

        # Parameters are already built, just remove non-SQL keys
        params.pop('data_source', None)
        params.pop('current_page', None)  # Remove page info but keep data_source in session
        params.pop('num_row', None)  # Remove row count info
        sql_params = params

        # Get total row count
        num_row_df = get_data('count', data_source, **sql_params)
        num_row = num_row_df.iloc[0, 0] if not num_row_df.empty else 0
        return num_row
    except Exception as e:
        st.error(f"An error occurred while getting row count: {str(e)}")
        return None


@trace_function_call
def handle_export_process(data_source: str):
    """Handle the entire process: row counting, and status updates."""
    # `st.session_state.params` is now set by the caller (`create_action_buttons`)
    params = st.session_state.get('params', {}).copy()

    # Keep the data_source in params for tab state management
    # but remove other non-SQL keys for the database query
    current_page = params.pop('current_page', None)
    params.pop('data_source', None)
    sql_params = params

    try:
        with st.spinner("Checking data size..."):
            # Get total row count
            num_row = get_row_count(data_source, **sql_params)
            if num_row is None: # Handle case where get_row_count fails
                st.session_state.user_message = {
                    "type": "error",
                    "text": "Failed to check data size. Please try again."
                }
                st.session_state.stage = 'initial'
                return
            
            # Re-add the data_source to params so it's preserved for tab state
            st.session_state.params['num_row'] = num_row
            # Keep data_source in params for tab state management
            st.session_state.params['data_source'] = data_source
            if current_page:
                st.session_state.params['current_page'] = current_page

        # --- Handle user messages and warnings ---
        if num_row == 0:
            st.session_state.user_message = {
                "type": "warning",
                "text": "No data found for the selected criteria."
            }
            st.session_state.stage = 'initial'
            return
            
        elif int(num_row) > 50000:
            st.session_state.user_message = {
                "type": "error",
                "text": f"Data is too large to export ({num_row:,} rows). Please narrow your selection to under 50,000 rows."
            }
            st.session_state.stage = 'blocked'  # Set to blocked state instead of initial
            return
        else:
            # Data size is acceptable, proceed with loading preview
            st.session_state.stage = 'loading_preview'

    except OperationalError as e:
        st.session_state.user_message = {
            "type": "error",
            "text": "❌ Database Connection Error. Please try again later."
        }
        st.session_state.stage = 'initial'
    except ProgrammingError as e:
        st.session_state.user_message = {
            "type": "error", 
            "text": "❌ An error occurred with the data query. Please check your inputs."
        }
        st.session_state.stage = 'initial'
    except Exception as e:
        st.session_state.user_message = {
            "type": "error",
            "text": f"❌ An unexpected error occurred: {str(e)}"
        }
        st.session_state.stage = 'initial'


def convert_df_to_csv(df: pd.DataFrame):
    output = StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    return output.getvalue()