"""
Data Loading Module
Handles loading and caching of all CSV files used in the dashboard.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Dict

# Get the data directory path
DATA_DIR = Path(__file__).parent.parent / "marketing_dataset"


@st.cache_data
def load_campaign_performance() -> pd.DataFrame:
    """Load campaign performance data."""
    df = pd.read_csv(DATA_DIR / "campaign_performance.csv")
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df


@st.cache_data
def load_customer_data() -> pd.DataFrame:
    """Load customer data."""
    return pd.read_csv(DATA_DIR / "customer_data.csv")


@st.cache_data
def load_product_sales() -> pd.DataFrame:
    """Load product sales data."""
    return pd.read_csv(DATA_DIR / "product_sales.csv")


@st.cache_data
def load_lead_scoring_results() -> pd.DataFrame:
    """Load lead scoring model results."""
    return pd.read_csv(DATA_DIR / "lead_scoring_results.csv")


@st.cache_data
def load_feature_importance() -> pd.DataFrame:
    """Load feature importance data."""
    return pd.read_csv(DATA_DIR / "feature_importance.csv")


@st.cache_data
def load_learning_curve() -> pd.DataFrame:
    """Load learning curve data."""
    return pd.read_csv(DATA_DIR / "learning_curve.csv")


@st.cache_data
def load_geographic_data() -> pd.DataFrame:
    """Load geographic data."""
    return pd.read_csv(DATA_DIR / "geographic_data.csv")


@st.cache_data
def load_channel_attribution() -> pd.DataFrame:
    """Load channel attribution data."""
    return pd.read_csv(DATA_DIR / "channel_attribution.csv")


@st.cache_data
def load_funnel_data() -> pd.DataFrame:
    """Load funnel data."""
    return pd.read_csv(DATA_DIR / "funnel_data.csv")


@st.cache_data
def load_customer_journey() -> pd.DataFrame:
    """Load customer journey data."""
    return pd.read_csv(DATA_DIR / "customer_journey.csv")


@st.cache_data
def load_correlation_matrix() -> pd.DataFrame:
    """Load correlation matrix data."""
    return pd.read_csv(DATA_DIR / "correlation_matrix.csv", index_col=0)


def load_all_data() -> Dict[str, pd.DataFrame]:
    """Load all datasets."""
    return {
        'campaign_performance': load_campaign_performance(),
        'customer_data': load_customer_data(),
        'product_sales': load_product_sales(),
        'lead_scoring_results': load_lead_scoring_results(),
        'feature_importance': load_feature_importance(),
        'learning_curve': load_learning_curve(),
        'geographic_data': load_geographic_data(),
        'channel_attribution': load_channel_attribution(),
        'funnel_data': load_funnel_data(),
        'customer_journey': load_customer_journey(),
        'correlation_matrix': load_correlation_matrix(),
    }
