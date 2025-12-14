"""
Customer Insights Page
Customer demographics, behavior, and segmentation analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_customer_data, load_campaign_performance
from utils.visualizations import (
    create_histogram, create_box_plot, create_violin_plot,
    create_scatter_plot, create_bubble_chart, format_number
)


def show():
    """Display Customer Insights page."""
    
    st.header("👥 Customer Insights")
    st.markdown("Analyze customer demographics, behavior, and segmentation")
    
    # Load data
    customer_df = load_customer_data()
    campaign_df = load_campaign_performance()
    
    # Section 1: Age Distribution
    st.subheader("1. Customer Age Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        bin_size = st.slider(
            "Bin Size",
            min_value=1,
            max_value=20,
            value=5,
            key='age_bins'
        )
    
    with col2:
        if 'customer_segment' in customer_df.columns:
            show_segments = st.multiselect(
                "Filter by Segment",
                options=customer_df['customer_segment'].unique(),
                default=customer_df['customer_segment'].unique(),
                key='age_segments'
            )
            age_data = customer_df[customer_df['customer_segment'].isin(show_segments)]
        else:
            age_data = customer_df
    
    fig = create_histogram(
        age_data,
        'age',
        f'Customer Age Distribution (Bin size: {bin_size})',
        nbins=int(age_data['age'].max() / bin_size),
        color_col='customer_segment' if 'customer_segment' in customer_df.columns else None
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.info(f"Age range: {customer_df['age'].min():.0f} - {customer_df['age'].max():.0f} years | "
            f"Mean age: {customer_df['age'].mean():.1f} years | "
            f"Median age: {customer_df['age'].median():.1f} years")
    
    # Section 2: Lifetime Value Distribution by Segment
    st.subheader("2. Lifetime Value by Customer Segment")
    
    if 'customer_segment' in customer_df.columns:
        show_points = st.checkbox(
            "Show Individual Points",
            value=False,
            key='ltv_points'
        )
        
        fig = create_box_plot(
            customer_df,
            'customer_segment',
            'lifetime_value',
            'Lifetime Value Distribution by Segment',
            points='all' if show_points else 'outliers'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Segment statistics
        segment_stats = customer_df.groupby('customer_segment')['lifetime_value'].agg([
            'count', 'mean', 'median', 'min', 'max', 'std'
        ]).round(2)
        segment_stats.columns = ['Count', 'Mean LTV (₹)', 'Median LTV (₹)', 
                                 'Min LTV (₹)', 'Max LTV (₹)', 'Std Dev']
        
        st.dataframe(segment_stats, use_container_width=True)
    else:
        st.warning("Segment data not available")
    
    # Section 3: Satisfaction Distribution by NPS
    st.subheader("3. Satisfaction Score Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'nps_category' in customer_df.columns:
            split_by_channel = st.checkbox(
                "Split by Acquisition Channel",
                value=True,
                key='satisfaction_split'
            )
            
            split_col = 'acquisition_channel' if split_by_channel and 'acquisition_channel' in customer_df.columns else None
        else:
            split_col = None
    
    if 'nps_category' in customer_df.columns:
        fig = create_violin_plot(
            customer_df,
            'nps_category',
            'satisfaction_score',
            'Satisfaction Score Distribution by NPS Category',
            split_col=split_col,
            points=True
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("NPS category data not available, showing overall satisfaction distribution")
        fig = create_histogram(
            customer_df,
            'satisfaction_score',
            'Satisfaction Score Distribution',
            nbins=10
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Section 4: Income vs Lifetime Value
    st.subheader("4. Income vs Lifetime Value Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        show_trendline = st.checkbox(
            "Show Trend Line",
            value=True,
            key='income_trendline'
        )
    
    if 'income' in customer_df.columns:
        color_col = 'segment' if 'segment' in customer_df.columns else None
        
        fig = create_scatter_plot(
            customer_df,
            'income',
            'lifetime_value',
            'Income vs Lifetime Value',
            color_col=color_col,
            trendline=show_trendline
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation analysis
        if 'segment' not in customer_df.columns:
            corr = customer_df[['income', 'lifetime_value']].corr().iloc[0, 1]
            st.info(f"Correlation between Income and LTV: {corr:.3f} "
                   f"({'Strong' if abs(corr) > 0.7 else 'Moderate' if abs(corr) > 0.4 else 'Weak'} positive)")
    else:
        st.warning("Income data not available")
    
    # Section 5: Customer Engagement Metrics
    st.subheader("5. Customer Engagement Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", f"{len(customer_df):,}")
    
    with col2:
        if 'churn' in customer_df.columns:
            churn_rate = (customer_df['churn'].sum() / len(customer_df) * 100)
            st.metric("Churn Rate", f"{churn_rate:.1f}%")
    
    with col3:
        if 'number_of_purchases' in customer_df.columns:
            avg_purchases = customer_df['number_of_purchases'].mean()
            st.metric("Avg Purchases", f"{avg_purchases:.1f}")
    
    with col4:
        avg_satisfaction = customer_df['satisfaction_score'].mean()
        st.metric("Avg Satisfaction", f"{avg_satisfaction:.2f}/5.0")
    
    # Section 6: Customer Segmentation Summary
    if 'customer_segment' in customer_df.columns:
        st.subheader("6. Customer Segment Summary")
        
        segment_summary = customer_df.groupby('customer_segment').agg({
            'customer_id': 'count',
            'age': 'mean',
            'income': 'mean',
            'lifetime_value': 'mean',
            'satisfaction_score': 'mean'
        }).round(2)
        
        segment_summary.columns = ['Count', 'Avg Age', 'Avg Income (₹)', 
                                  'Avg LTV (₹)', 'Avg Satisfaction']
        segment_summary['% of Total'] = (segment_summary['Count'] / len(customer_df) * 100).round(1)
        
        st.dataframe(segment_summary, use_container_width=True)
    
    # Section 7: Behavioral Insights
    st.subheader("7. Customer Behavior Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'number_of_purchases' in customer_df.columns:
            st.metric(
                "Avg Purchases per Customer",
                f"{customer_df['number_of_purchases'].mean():.1f}"
            )
    
    with col2:
        if 'engagement_score' in customer_df.columns:
            st.metric(
                "Avg Engagement Score",
                f"{customer_df['engagement_score'].mean():.2f}"
            )
    
    with col3:
        avg_ltv = customer_df['lifetime_value'].mean()
        st.metric(
            "Average LTV",
            f"₹{format_number(avg_ltv)}"
        )
    
    # Raw data viewer
    with st.expander("📋 View Raw Customer Data"):
        rows_to_show = st.slider("Rows to display", 10, len(customer_df), 50, key='customer_rows')
        st.dataframe(customer_df.head(rows_to_show), use_container_width=True)
