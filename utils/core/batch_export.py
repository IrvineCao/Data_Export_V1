"""
Batch Export Helper Functions

Key insight: SQL queries already GROUP BY correctly, so we should NOT re-group
during merge unless absolutely necessary. Just concatenate and drop exact duplicates.
"""

from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any, Optional
import pandas as pd


def split_date_range_by_days(start_date: str, end_date: str, batch_days: int = 7) -> List[Tuple[str, str]]:
    """
    Chia date range thành các batch theo số ngày.
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        batch_days: Number of days per batch (default: 7)
    
    Returns:
        List of tuples: [(start, end), (start, end), ...]
    """
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    batches = []
    current_start = start
    
    while current_start <= end:
        current_end = min(current_start + timedelta(days=batch_days - 1), end)
        batches.append((
            current_start.strftime('%Y-%m-%d'),
            current_end.strftime('%Y-%m-%d')
        ))
        current_start = current_end + timedelta(days=1)
    
    return batches


def get_merge_config(product: str) -> Tuple[List[str], Dict[str, Any]]:
    """
    Get merge keys and aggregation dictionary for each product type.
    
    CRITICAL: These keys MUST match the GROUP BY clause in SQL queries exactly!
    
    Args:
        product: Product type identifier
    
    Returns:
        Tuple of (merge_keys, agg_dict)
    """
    
    configs = {
        'keyword_lab': {
            'merge_keys': ['keyword_id', 'storefront_sid', 'month'],
            'agg_dict': {
                'search_volume': 'sum',
                'ads_gmv': 'sum',
                'cost': 'sum',
                'click': 'sum',
                'impression': 'sum',
                'ads_item_sold': 'sum',
                'bidding_price': 'mean',
                'suggested_bidding_price': 'mean',
                'roas': 'mean',
                'cr': 'mean',
                'ctr': 'mean',
                'cpc': 'mean',
                'peak_day_ads_gmv': 'max',
                'peak_day_bau_ads_gmv': 'max',
                'company_competitor': 'max',
                'product_competitor': 'max',
                'storefront_competitor': 'max'
            }
        },
        
        'keyword_performance': {
            'merge_keys': [
                'keyword',
                'storefront_name',
                'marketplace_code',
                'created_datetime',
                'display_type',
                'device_type',
                'product_position'
            ],
            'agg_dict': {
                'search_volume': 'mean',
                'atc': 'max',
                'cost': 'max',
                'click': 'max',
                'ads_order': 'max',
                'conversion': 'max',
                'direct_atc': 'max',
                'direct_gmv': 'max',
                'impression': 'max',
                'active_skus': 'max',
                'active_shops': 'max',
                'direct_order': 'max',
                'ads_item_sold': 'max',
                'direct_item_sold': 'max',
                'direct_conversion': 'max',
                'escore': 'mean',
                'ads_gmv': 'max',
                'benchmark_CPC': 'mean',
                'cpc': 'max'
            }
        },
        
        'product_tracking': {
            'merge_keys': [
                'keyword',
                'keyword_id',
                'product_name',
                'marketplace_name',
                'global_company_name',
                'storefront_name',
                'created_datetime'
            ],
            'agg_dict': {
                'item_sold_LT': 'mean',
                'selling_price': 'mean',
                'item_sold_l30d': 'sum',
                'product_slot': 'mean'
            }
        },
        
        'competition_landscape': {
            'merge_keys': [
                'global_company_name',
                'storefront_name',
                'created_datetime',
                'marketplace_name',
                'keyword',
                'display_type',
                'product_position',
                'device_type'
            ],
            'agg_dict': {
                'search_volume': 'mean',
                'share_of_search': 'mean'
            }
        },
        
        'storefront_optimization': {
            'merge_keys': [
                'storefront_id',
                'storefront_name',
                'country_code',
                'marketplace_code'
            ],
            'agg_dict': {
                'gmv': 'sum',
                'cost': 'sum',
                'roas': 'mean',
                'cpc': 'mean',
                'click': 'sum',
                'impression': 'sum',
                'ads_order': 'sum',
                'direct_gmv': 'sum',
                'direct_ads_order': 'sum',
                'direct_item_sold': 'sum',
                'item_sold': 'sum'
            }
        },
        
        'campaign_optimization': {
            'merge_keys': [
                'campaign_name',
                'storefront_name',
                'country_code',
                'marketplace_code',
                'month'
            ],
            'agg_dict': {
                'campaign_clicks': 'sum',
                'campaign_impressions': 'sum',
                'campaign_roas': 'mean',
                'cpc': 'mean',
                'campaign_gmv': 'sum',
                'campaign_cost': 'sum'
            }
        },
        
        'ads_object_optimization': {
            'merge_keys': [
                'object_name',
                'campaign_name',
                'storefront_name',
                'country_code',
                'marketplace_code',
                'month'
            ],
            'agg_dict': {
                'object_clicks': 'sum',
                'object_impressions': 'sum',
                'object_roas': 'mean',
                'object_cpc': 'mean',
                'object_gmv': 'sum',
                'object_cost': 'sum'
            }
        }
    }
    
    if product not in configs:
        raise ValueError(f"Invalid product: {product}. Available: {list(configs.keys())}")
    
    return configs[product]['merge_keys'], configs[product]['agg_dict']


# def merge_batches(dfs: List[pd.DataFrame], product: str = 'keyword_lab') -> pd.DataFrame:
#     """
#     Merge batches using simple concatenation strategy.
    
#     IMPORTANT: SQL queries already do GROUP BY correctly, so we should NOT
#     re-group here unless dealing with overlapping date ranges.
    
#     Strategy:
#     1. Concatenate all DataFrames
#     2. Drop exact duplicates (handles overlapping date ranges)
#     3. Return merged result
    
#     Args:
#         dfs: List of DataFrames to merge
#         product: Product type identifier (used only for validation)
    
#     Returns:
#         Merged DataFrame
#     """
#     if not dfs:
#         return pd.DataFrame()
#     if len(dfs) == 1:
#         return dfs[0]    
#     df = pd.concat(dfs, ignore_index=True)
#     df_merged = df.drop_duplicates()
    
#     return df_merged


def merge_batches(dfs: List[pd.DataFrame], product: str = 'keyword_lab') -> pd.DataFrame:
    """
    Alternative: Merge batches with explicit groupby (use only if needed).
    
    This should only be used if you have overlapping date ranges that create
    partial duplicates (same keys but different metric values).
    
    Args:
        dfs: List of DataFrames to merge
        product: Product type identifier
    
    Returns:
        Merged and re-aggregated DataFrame
    """
    if not dfs:
        return pd.DataFrame()
    if len(dfs) == 1:
        return dfs[0]
    
    df = pd.concat(dfs, ignore_index=True)
    
    merge_keys, agg_dict = get_merge_config(product)
    
    missing_keys = [k for k in merge_keys if k not in df.columns]
    if missing_keys:
        raise ValueError(
            f"Merge keys not found in DataFrame: {missing_keys}\n"
            f"Available columns: {df.columns.tolist()}"
        )
    
    other_cols = [c for c in df.columns if c not in merge_keys and c not in agg_dict.keys()]
    agg_dict_full = agg_dict.copy()
    for c in other_cols:
        agg_dict_full[c] = 'first'
    
    df_merged = df.groupby(merge_keys, as_index=False).agg(agg_dict_full)
    return df_merged


def load_batches_via_function(
    fetch_func,
    start_date: str,
    end_date: str,
    batch_days: int = 7,
    **kwargs: Any,
) -> List[pd.DataFrame]:
    """
    Generic batch loader.

    Args:
        fetch_func: Callable accepting start_date, end_date (YYYY-MM-DD) and **kwargs, returns DataFrame
        start_date: Overall start date (YYYY-MM-DD)
        end_date: Overall end date (YYYY-MM-DD)
        batch_days: Number of days per batch
        **kwargs: Extra parameters forwarded to fetch_func

    Returns:
        List of DataFrames for each batch
    """
    batches = split_date_range_by_days(start_date, end_date, batch_days)
    results: List[pd.DataFrame] = []
    
    for batch_start, batch_end in batches:
        df = fetch_func(start_date=batch_start, end_date=batch_end, **kwargs)
        if df is not None and isinstance(df, pd.DataFrame) and not df.empty:
            results.append(df)
    
    return results


def get_recommended_batch_size(num_storefronts: int, date_range_days: int) -> int:
    """
    Get recommended batch size based on number of storefronts and date range.
    
    Args:
        num_storefronts: Number of storefronts
        date_range_days: Total days in date range
    
    Returns:
        Recommended batch size in days
    """
    if num_storefronts <= 2:
        return 14  # 2 weeks
    elif num_storefronts <= 5:
        return 7   # 1 week
    else:
        return 7   # 1 week for 5+ storefronts