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
    st.markdown("Analyze marketing performance across India's states and regions")
    
    # Load data
    geo_df = load_geographic_data()
    
    # Section 1: State-wise Revenue (Choropleth alternative)
    st.subheader("1. State Revenue Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metric = st.selectbox(
            "Select Metric",
            options=['revenue', 'customers', 'market_penetration', 'yoy_growth']
                   if 'yoy_growth' in geo_df.columns
                   else ['revenue', 'customers', 'market_penetration'],
            key='geo_metric'
        )
    
    geo_sorted = geo_df.sort_values(metric, ascending=True)
    
    fig = create_horizontal_bar_chart(
        geo_sorted,
        metric,
        'state' if 'state' in geo_df.columns else 'region',
        f'{metric.replace("_", " ").title()} by State'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Section 2: Top Performing States
    st.subheader("2. Top Performing States")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🥇 Top Revenue State", geo_df.loc[geo_df['revenue'].idxmax(), 
                                                      'state' if 'state' in geo_df.columns else 'region'],
                 f"₹{format_number(geo_df['revenue'].max())}")
    
    with col2:
        st.metric("👥 Most Customers", geo_df.loc[geo_df['customers'].idxmax(),
                                                   'state' if 'state' in geo_df.columns else 'region'],
                 f"{format_number(geo_df['customers'].max(), decimals=0)} customers")
    
    with col3:
        if 'market_penetration' in geo_df.columns:
            st.metric("📊 Highest Penetration", geo_df.loc[geo_df['market_penetration'].idxmax(),
                                                           'state' if 'state' in geo_df.columns else 'region'],
                     f"{geo_df['market_penetration'].max():.2f}%")
    
    # Section 3: Regional Summary Table
    st.subheader("3. Regional Performance Summary")
    
    summary_cols = ['revenue', 'customers', 'market_penetration']
    if 'satisfaction' in geo_df.columns:
        summary_cols.append('satisfaction')
    if 'yoy_growth' in geo_df.columns:
        summary_cols.append('yoy_growth')
    
    available_cols = [col for col in summary_cols if col in geo_df.columns]
    
    summary_table = geo_df[['state' if 'state' in geo_df.columns else 'region'] + available_cols].copy()
    summary_table = summary_table.sort_values('revenue', ascending=False)
    
    column_names = ['State/Region'] + [col.replace('_', ' ').title() for col in available_cols]
    summary_table.columns = column_names
    
    st.dataframe(summary_table, use_container_width=True)
    
    # Section 4: Growth Analysis
    if 'yoy_growth' in geo_df.columns:
        st.subheader("4. Year-over-Year Growth Analysis")
        
        growth_sorted = geo_df.sort_values('yoy_growth', ascending=True)
        
        fig = create_horizontal_bar_chart(
            growth_sorted,
            'yoy_growth',
            'state' if 'state' in geo_df.columns else 'region',
            'YoY Growth Rate by State'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Highest Growth", 
                     geo_df.loc[geo_df['yoy_growth'].idxmax(), 
                               'state' if 'state' in geo_df.columns else 'region'],
                     f"{geo_df['yoy_growth'].max():.2f}%")
        
        with col2:
            st.metric("Lowest Growth",
                     geo_df.loc[geo_df['yoy_growth'].idxmin(),
                               'state' if 'state' in geo_df.columns else 'region'],
                     f"{geo_df['yoy_growth'].min():.2f}%")
    
    # Section 5: Customer Satisfaction by Region
    if 'satisfaction' in geo_df.columns:
        st.subheader("5. Customer Satisfaction by Region")
        
        satisfaction_sorted = geo_df.sort_values('satisfaction', ascending=True)
        
        fig = create_horizontal_bar_chart(
            satisfaction_sorted,
            'satisfaction',
            'state' if 'state' in geo_df.columns else 'region',
            'Average Satisfaction Score by State'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Section 6: Market Penetration Analysis
    if 'market_penetration' in geo_df.columns:
        st.subheader("6. Market Penetration Analysis")
        
        penetration_sorted = geo_df.sort_values('market_penetration', ascending=True)
        
        fig = create_horizontal_bar_chart(
            penetration_sorted,
            'market_penetration',
            'state' if 'state' in geo_df.columns else 'region',
            'Market Penetration by State (%)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"Average Market Penetration: {geo_df['market_penetration'].mean():.2f}% | "
               f"Highest: {geo_df['market_penetration'].max():.2f}% | "
               f"Lowest: {geo_df['market_penetration'].min():.2f}%")
    
    # Section 7: Geographic Metrics Overview
    st.subheader("7. Geographic Overview Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total States", len(geo_df))
    
    with col2:
        st.metric("Total Revenue", f"₹{format_number(geo_df['revenue'].sum())}")
    
    with col3:
        st.metric("Total Customers", f"{format_number(geo_df['customers'].sum(), decimals=0)}")
    
    with col4:
        if 'satisfaction' in geo_df.columns:
            st.metric("Avg Satisfaction", f"{geo_df['satisfaction'].mean():.2f}/5")
    
    # Section 8: Regional Classification
    st.subheader("8. States Classification")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**High Revenue, High Growth States**")
        if 'yoy_growth' in geo_df.columns:
            high_performers = geo_df[
                (geo_df['revenue'] > geo_df['revenue'].median()) &
                (geo_df['yoy_growth'] > geo_df['yoy_growth'].median())
            ][['state' if 'state' in geo_df.columns else 'region', 'revenue', 'yoy_growth']]
            
            if len(high_performers) > 0:
                st.dataframe(high_performers, use_container_width=True)
            else:
                st.info("No high-performing states found")
    
    with col2:
        st.write("**Growth Opportunity States**")
        if 'yoy_growth' in geo_df.columns:
            growth_potential = geo_df[
                (geo_df['revenue'] < geo_df['revenue'].median()) &
                (geo_df['yoy_growth'] > geo_df['yoy_growth'].median())
            ][['state' if 'state' in geo_df.columns else 'region', 'revenue', 'yoy_growth']]
            
            if len(growth_potential) > 0:
                st.dataframe(growth_potential, use_container_width=True)
            else:
                st.info("No growth opportunity states found")
    
    # Raw data viewer
    with st.expander("📋 View Raw Geographic Data"):
        st.dataframe(geo_df, use_container_width=True)
