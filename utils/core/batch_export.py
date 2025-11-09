"""
Batch Export Helper Functions

This module provides functions to handle batch exporting of large datasets
by splitting date ranges and properly re-aggregating metrics to avoid duplicates.
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


def merge_batches(dfs: List[pd.DataFrame], product = 'keyword_lab') -> pd.DataFrame:
    """
    Merge KWL (Keyword Lab) batches and re-aggregate metrics.
    Logic mirrors the notebook's merge keys and aggregation map.
    """
    if not dfs:
        return pd.DataFrame()
    if len(dfs) == 1:
        return dfs[0]
    if product == 'keyword_lab':
        df = pd.concat(dfs, ignore_index=True)

        merge_keys = ['keyword_id', 'storefront_sid', 'month']

        agg_dict: Dict[str, Any] = {
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
    elif product == 'keyword_performance':
        df = pd.concat(dfs, ignore_index=True)
        merge_keys = ['keyword_id', 'storefront_sid', 'month']
        agg_dict: Dict[str, Any] = {
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
    elif product == 'product_tracking':
        df = pd.concat(dfs, ignore_index=True)
        merge_keys = ['product_id', 'storefront_sid', 'month']
        agg_dict: Dict[str, Any] = {
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
    elif product == 'competition_landscape':
        df = pd.concat(dfs, ignore_index=True)
        merge_keys = ['keyword_id', 'storefront_sid', 'month']
        agg_dict: Dict[str, Any] = {
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
    elif product == 'storefront_optimization':
        df = pd.concat(dfs, ignore_index=True)
        merge_keys = ['storefront_sid', 'month']
        agg_dict: Dict[str, Any] = {
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
    elif product == 'campaign_optimization':
        df = pd.concat(dfs, ignore_index=True)
        merge_keys = ['campaign_id', 'month']
        agg_dict: Dict[str, Any] = {
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
    elif product == 'ads_object_optimization':
        df = pd.concat(dfs, ignore_index=True)
        merge_keys = ['ads_object_id', 'month']
        agg_dict: Dict[str, Any] = {
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
    elif product == 'ads_placement_optimization':
        df = pd.concat(dfs, ignore_index=True)
        merge_keys = ['ads_placement_id', 'month']
        agg_dict: Dict[str, Any] = {
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
    else:
        raise ValueError(f"Invalid product: {product}")

    # Add 'first' for other columns
    other_cols = [c for c in df.columns if c not in merge_keys + list(agg_dict.keys())]
    for c in other_cols:
        agg_dict[c] = 'first'

    # Keep only merge keys that exist to avoid KeyError
    group_keys = [k for k in merge_keys if k in df.columns]
    if not group_keys:
        # If keys are missing, return concatenated df as last resort
        return df

    df_merged = df.groupby(group_keys, as_index=False).agg(agg_dict)
    return df_merged


# === Notebook-inspired helpers (generic, no UI/DB coupling) ===

def split_month_range(start_date: str, end_date: str) -> List[Tuple[str, str]]:
    """
    Split an overall date range into calendar-month subranges.
    Returns list of (month_start, month_end) as 'YYYY-MM-DD' strings.
    """
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Normalize to the first day of the month
    current = start.replace(day=1)
    months: List[Tuple[str, str]] = []

    while current <= end:
        # Compute last day of current month
        if current.month == 12:
            next_month_first = current.replace(year=current.year + 1, month=1, day=1)
        else:
            next_month_first = current.replace(month=current.month + 1, day=1)
        month_last = next_month_first - timedelta(days=1)

        month_start = max(current, start)
        month_end = min(month_last, end)

        months.append((month_start.strftime('%Y-%m-%d'), month_end.strftime('%Y-%m-%d')))
        current = next_month_first

    return months


def load_batches_via_function(
    fetch_func,
    start_date: str,
    end_date: str,
    batch_days: int = 7,
    **kwargs: Any,
) -> List[pd.DataFrame]:
    """
    Generic batch loader inspired by notebook logic.

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


def merge_and_reaggregate_by_config(dfs: List[pd.DataFrame], data_source: str) -> pd.DataFrame:
    """
    KWL-only entry point preserved for compatibility with existing calls.
    """
    if data_source != 'keyword_lab':
        raise ValueError("Only 'keyword_lab' is supported in batch_export module at this time.")
    return merge_keyword_lab_batches(dfs)


"""
test code cho kwl: done
test code cho keyword performance: not done
test code cho product tracking: not done
test code cho competition landscape: not done
test code cho storefront optimization: not done
test code cho storefront in workspace: not done
"""