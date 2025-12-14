"""
Executive Overview Page
Displays key KPIs and high-level marketing metrics.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_campaign_performance, load_customer_data
from utils.visualizations import (
    create_metric_cards, create_horizontal_bar_chart, 
    create_line_chart, format_number, format_percentage
)


def show():
    """Display Executive Overview page."""
    
    st.header("📊 Executive Overview")
    st.markdown("High-level marketing metrics and key performance indicators")
    
    # Load data
    campaign_df = load_campaign_performance()
    customer_df = load_customer_data()
    
    # Calculate KPIs
    total_revenue = campaign_df['revenue'].sum()
    total_conversions = campaign_df['conversions'].sum()
    avg_roas = campaign_df['roas'].mean()
    customer_count = len(customer_df)
    
    # Display metric cards
    st.subheader("Key Performance Indicators")
    metrics = {
        'Revenue': (f"₹{format_number(total_revenue)}", 'Total Revenue', '#1f77b4'),
        'Conversions': (f"{format_number(total_conversions, decimals=0)}", 'Total Conversions', '#2ca02c'),
        'ROAS': (f"{avg_roas:.2f}x", 'Avg ROAS', '#ff7f0e'),
        'Customers': (f"{format_number(customer_count)}", 'Total Customers', '#d62728')
    }
    create_metric_cards(metrics)
    
    # Two columns layout
    col1, col2 = st.columns(2)
    
    # Revenue Trend
    with col1:
        st.subheader("Revenue Trend Over Time")
        
        # Prepare time series data
        if 'date' in campaign_df.columns:
            daily_revenue = campaign_df.groupby('date')['revenue'].sum().reset_index()
            
            # Aggregation level selector
            agg_level = st.radio("Aggregation Level", 
                                options=['Daily', 'Weekly', 'Monthly'],
                                horizontal=True, 
                                key='revenue_trend_agg')
            
            if agg_level == 'Weekly':
                daily_revenue['date'] = pd.to_datetime(daily_revenue['date'])
                daily_revenue = daily_revenue.set_index('date').resample('W').sum().reset_index()
            elif agg_level == 'Monthly':
                daily_revenue['date'] = pd.to_datetime(daily_revenue['date'])
                daily_revenue = daily_revenue.set_index('date').resample('M').sum().reset_index()
            
            fig = create_line_chart(
                daily_revenue,
                'date',
                'revenue',
                f'Revenue Trend ({agg_level})',
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Date column not found in campaign data")
    
    # Channel Performance
    with col2:
        st.subheader("Channel Performance")
        
        # Select metric
        metric = st.selectbox(
            "Select Metric",
            options=['Revenue', 'Conversions', 'ROAS'],
            key='channel_metric'
        )
        
        metric_labels = {
            'revenue': 'Total Revenue (₹)',
            'conversions': 'Total Conversions',
            'roas': 'Average ROAS'
        }
        
        try:
            if metric == 'roas':
                channel_perf = campaign_df.groupby('channel')['roas'].mean().reset_index()
                channel_perf.columns = ['channel', 'roas']
            else:
                channel_perf = campaign_df.groupby('channel')[metric].sum().reset_index()
            
            if channel_perf.empty:
                st.warning("No data available for selected metric")
            else:
                fig = create_horizontal_bar_chart(
                    channel_perf,
                    metric,
                    'channel',
                    f'{metric_labels[metric]} by Channel'
                )
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")
    
    # Additional insights
    st.markdown("---")
    st.subheader("Campaign Performance Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Top performing channel
        top_channel = campaign_df.groupby('channel')['revenue'].sum().idxmax()
        top_channel_revenue = campaign_df.groupby('channel')['revenue'].sum().max()
        st.metric(
            "Top Channel",
            top_channel,
            f"₹{format_number(top_channel_revenue)}"
        )
    
    with col2:
        # Average conversion rate
        avg_ctr = campaign_df['ctr'].mean() * 100
        st.metric(
            "Avg Click-Through Rate",
            f"{avg_ctr:.2f}%"
        )
    
    with col3:
        # Average CPA
        avg_cpa = campaign_df['cpa'].mean()
        st.metric(
            "Avg Cost Per Acquisition",
            f"₹{format_number(avg_cpa)}"
        )
    
    # Detailed metrics table
    st.subheader("Channel Metrics Summary")
    
    channel_summary = campaign_df.groupby('channel').agg({
        'revenue': 'sum',
        'conversions': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'spend': 'sum',
        'ctr': 'mean',
        'roas': 'mean'
    }).round(2)
    
    channel_summary = channel_summary.sort_values('revenue', ascending=False)
    channel_summary.columns = ['Revenue (₹)', 'Conversions', 'Impressions', 'Clicks', 
                               'Spend (₹)', 'Avg CTR (%)', 'Avg ROAS']
    
    st.dataframe(channel_summary, use_container_width=True)
    
    # Customer insights
    st.markdown("---")
    st.subheader("Customer Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_age = customer_df['age'].mean()
        st.metric("Average Customer Age", f"{avg_age:.1f} years")
    
    with col2:
        avg_ltv = customer_df['lifetime_value'].mean()
        st.metric("Avg Lifetime Value", f"₹{format_number(avg_ltv)}")
    
    with col3:
        avg_satisfaction = customer_df['satisfaction_score'].mean()
        st.metric("Avg Satisfaction Score", f"{avg_satisfaction:.1f}/5.0")
    
    # Display data preview
    with st.expander("📋 View Raw Campaign Data (First 50 rows)"):
        st.dataframe(campaign_df.head(50), use_container_width=True)
