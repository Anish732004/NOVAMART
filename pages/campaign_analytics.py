"""
Campaign Analytics Page
Detailed temporal and comparative analysis of marketing campaigns.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.data_loader import load_campaign_performance
from utils.visualizations import (
    create_line_chart, create_area_chart, create_grouped_bar_chart,
    create_stacked_bar_chart, create_calendar_heatmap
)


def show():
    """Display Campaign Analytics page."""
    
    st.header("📈 Campaign Analytics")
    st.markdown("Detailed analysis of campaign performance across time and dimensions")
    
    # Load data
    campaign_df = load_campaign_performance()
    
    # Ensure date is datetime
    if 'date' in campaign_df.columns:
        campaign_df['date'] = pd.to_datetime(campaign_df['date'])
        campaign_df['year'] = campaign_df['date'].dt.year
        campaign_df['quarter'] = campaign_df['date'].dt.quarter
        campaign_df['month'] = campaign_df['date'].dt.month
        campaign_df['week'] = campaign_df['date'].dt.isocalendar().week
    
    # Section 1: Revenue Trend with Interactions
    st.subheader("1. Revenue Trend Over Time")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        agg_level = st.selectbox(
            "Aggregation Level",
            options=['Daily', 'Weekly', 'Monthly'],
            key='campaign_agg_level'
        )
    
    with col2:
        show_channels = st.multiselect(
            "Filter by Channels",
            options=campaign_df['channel'].unique(),
            default=campaign_df['channel'].unique(),
            key='campaign_channels'
        )
    
    with col3:
        date_range = st.date_input(
            "Date Range",
            value=(campaign_df['date'].min(), campaign_df['date'].max()),
            key='campaign_date_range'
        )
    
    # Filter data
    filtered_df = campaign_df[
        (campaign_df['channel'].isin(show_channels)) &
        (campaign_df['date'] >= pd.Timestamp(date_range[0])) &
        (campaign_df['date'] <= pd.Timestamp(date_range[1]))
    ]
    
    # Aggregate based on selection
    if agg_level == 'Weekly':
        trend_data = filtered_df.groupby([pd.Grouper(key='date', freq='W'), 'channel'])['revenue'].sum().reset_index()
    elif agg_level == 'Monthly':
        trend_data = filtered_df.groupby([pd.Grouper(key='date', freq='M'), 'channel'])['revenue'].sum().reset_index()
    else:
        trend_data = filtered_df.groupby(['date', 'channel'])['revenue'].sum().reset_index()
    
    fig = create_line_chart(
        trend_data,
        'date',
        'revenue',
        f'{agg_level} Revenue Trend by Channel',
        color_col='channel'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Section 2: Cumulative Conversions
    st.subheader("2. Cumulative Conversions by Channel")
    
    region_filter = st.multiselect(
        "Filter by Regions",
        options=campaign_df['region'].unique() if 'region' in campaign_df.columns else ['All'],
        default=campaign_df['region'].unique() if 'region' in campaign_df.columns else ['All'],
        key='cumulative_regions'
    )
    
    if 'region' in campaign_df.columns:
        cumulative_df = campaign_df[campaign_df['region'].isin(region_filter)].copy()
    else:
        cumulative_df = campaign_df.copy()
    
    # Sort by date and calculate cumulative conversions per channel
    cumulative_df = cumulative_df.sort_values('date')
    cumulative_df['cumulative_conversions'] = cumulative_df.groupby('channel')['conversions'].cumsum()
    
    # Aggregate by date and channel
    cumulative_agg = cumulative_df.groupby(['date', 'channel'])['cumulative_conversions'].sum().reset_index()
    
    fig = create_area_chart(
        cumulative_agg,
        'date',
        'cumulative_conversions',
        'Cumulative Conversions Over Time',
        group_col='channel'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Section 3: Regional Performance by Quarter
    st.subheader("3. Regional Performance by Quarter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        year_filter = st.selectbox(
            "Select Year",
            options=sorted(campaign_df['year'].unique()),
            key='regional_year'
        )
    
    with col2:
        show_all_quarters = st.checkbox("Show All Quarters", value=True, key='all_quarters')
        if not show_all_quarters:
            quarters = st.multiselect(
                "Select Quarters",
                options=sorted(campaign_df[campaign_df['year']==year_filter]['quarter'].unique()),
                default=sorted(campaign_df[campaign_df['year']==year_filter]['quarter'].unique()),
                key='selected_quarters'
            )
    
    regional_df = campaign_df[campaign_df['year'] == year_filter].copy()
    if not show_all_quarters:
        regional_df = regional_df[regional_df['quarter'].isin(quarters)]
    
    if 'region' in regional_df.columns:
        regional_perf = regional_df.groupby(['region', 'quarter'])['revenue'].sum().reset_index()
        regional_perf['Quarter'] = 'Q' + regional_perf['quarter'].astype(str)
        
        fig = create_grouped_bar_chart(
            regional_perf,
            'region',
            'revenue',
            'Quarter',
            f'Revenue by Region - {year_filter}'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Region data not available in dataset")
    
    # Section 4: Campaign Type Contribution
    st.subheader("4. Campaign Type Contribution to Spend")
    
    col1, col2 = st.columns(2)
    
    with col1:
        stacked_mode = st.radio(
            "View Mode",
            options=['Absolute', '100% Stacked'],
            horizontal=True,
            key='stacked_mode'
        )
    
    if 'campaign_type' in campaign_df.columns:
        monthly_campaigns = campaign_df.groupby([pd.Grouper(key='date', freq='M'), 'campaign_type'])['spend'].sum().reset_index()
        
        mode_name = 'relative' if stacked_mode == '100% Stacked' else 'absolute'
        fig = create_stacked_bar_chart(
            monthly_campaigns,
            'date',
            'spend',
            'campaign_type',
            f'Monthly Campaign Spend Contribution',
            mode=mode_name
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Campaign type data not available in dataset")
    
    # Section 5: Detailed Campaign Metrics Table
    st.subheader("5. Detailed Campaign Metrics")
    
    # Aggregate by channel
    detailed_metrics = campaign_df.groupby('channel').agg({
        'revenue': 'sum',
        'conversions': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'spend': 'sum',
        'ctr': 'mean',
        'cpa': 'mean',
        'roas': 'mean'
    }).round(2)
    
    detailed_metrics = detailed_metrics.sort_values('revenue', ascending=False)
    detailed_metrics.columns = ['Revenue (₹)', 'Conversions', 'Impressions', 'Clicks',
                                'Spend (₹)', 'Avg CTR', 'Avg CPA (₹)', 'Avg ROAS']
    
    st.dataframe(detailed_metrics, use_container_width=True)
    
    # Section 6: Performance Distribution
    st.subheader("6. Performance Metrics Distribution")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Revenue", f"₹{campaign_df['revenue'].sum():,.0f}")
        st.metric("Total Conversions", f"{campaign_df['conversions'].sum():,.0f}")
    
    with col2:
        st.metric("Avg ROAS", f"{campaign_df['roas'].mean():.2f}x")
        st.metric("Avg CTR", f"{campaign_df['ctr'].mean()*100:.2f}%")
    
    with col3:
        st.metric("Total Impressions", f"{campaign_df['impressions'].sum():,.0f}")
        st.metric("Total Spend", f"₹{campaign_df['spend'].sum():,.0f}")
    
    # Raw data viewer
    with st.expander("📋 View Raw Campaign Data"):
        col1, col2 = st.columns(2)
        with col1:
            rows_to_show = st.slider("Rows to display", 10, len(campaign_df), 50)
        
        st.dataframe(campaign_df.head(rows_to_show), use_container_width=True)
