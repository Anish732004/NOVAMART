"""
Product Performance Page
Product hierarchy, sales analysis, and margin analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_product_sales, load_campaign_performance
from utils.visualizations import (
    create_horizontal_bar_chart, create_grouped_bar_chart,
    create_treemap, format_number
)


def show():
    """Display Product Performance page."""
    
    st.header("🛍️ Product Performance")
    st.markdown("Analyze product hierarchy, sales, and profitability")
    
    # Load data
    product_df = load_product_sales()
    
    # Section 1: Product Category Performance
    st.subheader("1. Sales by Product Category")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metric_type = st.selectbox(
            "Select Metric",
            options=['sales', 'units', 'profit_margin'] 
                   if 'profit_margin' in product_df.columns 
                   else ['sales', 'units'],
            key='product_metric'
        )
    
    if 'category' in product_df.columns:
        category_perf = product_df.groupby('category').agg({
            'sales': 'sum',
            'units': 'sum'
        }).reset_index()
        
        if 'profit_margin' in product_df.columns:
            category_perf['profit_margin'] = product_df.groupby('category')['profit_margin'].mean().values
        
        category_perf = category_perf.sort_values('sales', ascending=True)
        
        fig = create_horizontal_bar_chart(
            category_perf,
            metric_type,
            'category',
            f'{metric_type.title()} by Product Category'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Category summary table
        summary = product_df.groupby('category').agg({
            'sales': 'sum',
            'units': 'sum',
            'product_id': 'count'
        }).round(2)
        summary.columns = ['Total Sales (₹)', 'Total Units', 'Products']
        summary['Avg Sale'] = (summary['Total Sales (₹)'] / summary['Total Units']).round(2)
        
        st.dataframe(summary, use_container_width=True)
    
    # Section 2: Regional Product Performance
    st.subheader("2. Product Sales by Region and Quarter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'region' in product_df.columns:
            selected_regions = st.multiselect(
                "Select Regions",
                options=product_df['region'].unique(),
                default=product_df['region'].unique(),
                key='product_regions'
            )
    
    with col2:
        if 'quarter' in product_df.columns:
            selected_quarters = st.multiselect(
                "Select Quarters",
                options=sorted(product_df['quarter'].unique()),
                default=sorted(product_df['quarter'].unique()),
                key='product_quarters'
            )
    
    if 'region' in product_df.columns and 'quarter' in product_df.columns:
        regional_data = product_df[
            (product_df['region'].isin(selected_regions)) &
            (product_df['quarter'].isin(selected_quarters))
        ]
        
        region_perf = regional_data.groupby(['region', 'quarter'])['sales'].sum().reset_index()
        region_perf['Quarter'] = 'Q' + region_perf['quarter'].astype(str)
        
        fig = create_grouped_bar_chart(
            region_perf,
            'region',
            'sales',
            'Quarter',
            'Sales by Region and Quarter'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Section 3: Profit Margin Analysis
    if 'profit_margin' in product_df.columns:
        st.subheader("3. Profitability Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Margin by category
            margin_data = product_df.groupby('category').agg({
                'profit_margin': 'mean',
                'sales': 'sum'
            }).reset_index().sort_values('profit_margin', ascending=True)
            
            fig = create_horizontal_bar_chart(
                margin_data,
                'profit_margin',
                'category',
                'Average Profit Margin by Category'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Margin statistics
            margin_stats = pd.DataFrame({
                'Metric': ['Highest Margin', 'Lowest Margin', 'Avg Margin', 'Median Margin'],
                'Value': [
                    f"{product_df['profit_margin'].max():.2f}%",
                    f"{product_df['profit_margin'].min():.2f}%",
                    f"{product_df['profit_margin'].mean():.2f}%",
                    f"{product_df['profit_margin'].median():.2f}%"
                ]
            })
            
            st.dataframe(margin_stats, use_container_width=True)
    
    # Section 4: Top Products Analysis
    st.subheader("4. Top Products by Sales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        n_products = st.slider("Number of Top Products", 5, 20, 10, key='top_products')
    
    if 'product_name' in product_df.columns or 'product_id' in product_df.columns:
        product_col = 'product_name' if 'product_name' in product_df.columns else 'product_id'
        
        top_products = product_df.groupby(product_col).agg({
            'sales': 'sum',
            'units': 'sum'
        }).nlargest(n_products, 'sales').reset_index()
        
        fig = create_horizontal_bar_chart(
            top_products,
            'sales',
            product_col,
            f'Top {n_products} Products by Sales'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Section 5: Product Performance Metrics
    st.subheader("5. Overall Product Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", len(product_df))
    
    with col2:
        st.metric("Total Sales", f"₹{format_number(product_df['sales'].sum())}")
    
    with col3:
        st.metric("Total Units Sold", f"{format_number(product_df['units'].sum(), decimals=0)}")
    
    with col4:
        if 'profit_margin' in product_df.columns:
            st.metric("Avg Margin", f"{product_df['profit_margin'].mean():.2f}%")
    
    # Section 6: Subcategory Breakdown
    if 'subcategory' in product_df.columns:
        st.subheader("6. Sales by Subcategory")
        
        selected_category = st.selectbox(
            "Select Category",
            options=product_df['category'].unique() if 'category' in product_df.columns else [],
            key='subcategory_filter'
        )
        
        if 'category' in product_df.columns:
            subcat_data = product_df[product_df['category'] == selected_category]
            subcat_perf = subcat_data.groupby('subcategory')['sales'].sum().reset_index()
            subcat_perf = subcat_perf.sort_values('sales', ascending=True)
            
            fig = create_horizontal_bar_chart(
                subcat_perf,
                'sales',
                'subcategory',
                f'Sales by Subcategory - {selected_category}'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Raw data viewer
    with st.expander("📋 View Raw Product Data"):
        rows_to_show = st.slider("Rows to display", 10, len(product_df), 50, key='product_rows')
        st.dataframe(product_df.head(rows_to_show), use_container_width=True)
