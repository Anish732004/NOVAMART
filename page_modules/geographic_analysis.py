"""
Geographic Analysis Page
State-level performance and geographic distribution analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_geographic_data
from utils.visualizations import (
    create_horizontal_bar_chart, create_bubble_chart, format_number
)


def show():
    """Display Geographic Analysis page."""
    
    st.header("🗺️ Geographic Analysis")
    st.markdown("Analyze marketing performance across regions")
    
    # Load data
    geo_df = load_geographic_data()
    
    # Display available columns
    st.write(f"Available columns: {list(geo_df.columns)}")
    
    # Identify available columns
    numeric_cols = geo_df.select_dtypes(include=['number']).columns.tolist()
    text_cols = geo_df.select_dtypes(include=['object']).columns.tolist()
    
    if not numeric_cols:
        st.error("No numeric columns found in geographic data")
        return
    
    # Identify the location column (state/region)
    location_col = None
    if 'state' in geo_df.columns:
        location_col = 'state'
    elif 'region' in geo_df.columns:
        location_col = 'region'
    elif text_cols:
        location_col = text_cols[0]
    else:
        st.error("No location column found")
        return
    
    # Section 1: State-wise Revenue (Choropleth alternative)
    st.subheader("1. Regional Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metric = st.selectbox(
            "Select Metric",
            options=numeric_cols,
            key='geo_metric'
        )
    
    try:
        geo_sorted = geo_df.sort_values(metric, ascending=True)
        
        fig = create_horizontal_bar_chart(
            geo_sorted,
            metric,
            location_col,
            f'{metric.replace("_", " ").title()} by {location_col.title()}'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
    
    # Section 2: Top Performing States
    st.subheader("2. Top Performing Regions")
    
    try:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if numeric_cols:
                top_col = numeric_cols[0]
                top_val = geo_df[top_col].max()
                top_loc = geo_df.loc[geo_df[top_col].idxmax(), location_col]
                st.metric(f"Top {top_col.title()}", top_loc, f"{format_number(top_val)}")
        
        with col2:
            if len(numeric_cols) > 1:
                second_col = numeric_cols[1]
                second_val = geo_df[second_col].max()
                second_loc = geo_df.loc[geo_df[second_col].idxmax(), location_col]
                st.metric(f"Top {second_col.title()}", second_loc, f"{format_number(second_val, decimals=0)}")
        
        with col3:
            if len(numeric_cols) > 2:
                third_col = numeric_cols[2]
                third_val = geo_df[third_col].max()
                third_loc = geo_df.loc[geo_df[third_col].idxmax(), location_col]
                st.metric(f"Top {third_col.title()}", third_loc, f"{third_val:.2f}")
    except Exception as e:
        st.error(f"Error displaying metrics: {str(e)}")
    
    # Section 3: Regional Summary Table
    st.subheader("3. Regional Performance Summary")
    
    try:
        # Use available numeric columns
        cols_to_show = [location_col] + numeric_cols[:5]  # Show first 5 numeric columns
        summary_table = geo_df[cols_to_show].copy()
        
        # Sort by first numeric column
        if numeric_cols:
            summary_table = summary_table.sort_values(numeric_cols[0], ascending=False)
        
        st.dataframe(summary_table, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating summary table: {str(e)}")
    
    # Section 4: Geographic Metrics Overview
    st.subheader("4. Geographic Overview Metrics")
    
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Regions", len(geo_df))
        
        with col4:
            if len(numeric_cols) > 2:
                st.metric(f"Avg {numeric_cols[2].title()}", 
                         f"{geo_df[numeric_cols[2]].mean():.2f}")
    except Exception as e:
        st.error(f"Error displaying metrics: {str(e)}")
    
    # Raw data viewer
    with st.expander("📋 View Raw Geographic Data"):
        st.dataframe(geo_df, use_container_width=True)
