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
    
    # Display available columns for debugging
    st.write(f"Available columns: {list(product_df.columns)}")
    
    # Identify available numeric columns
    numeric_cols = product_df.select_dtypes(include=['number']).columns.tolist()
    
    # Section 1: Product Category Performance
    st.subheader("1. Sales by Product Category")
    
    if 'category' not in product_df.columns:
        st.warning("Category column not found in product data")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Filter to numeric columns that might represent sales/units
        metric_options = [col for col in numeric_cols if col not in ['id', 'product_id']]
        if not metric_options:
            st.warning("No numeric metrics available")
            return
            
        metric_type = st.selectbox(
            "Select Metric",
            options=metric_options,
            key='product_metric'
        )
    
    try:
        # Build aggregation dictionary based on available columns
        agg_dict = {metric_type: 'sum'}
        
        # Add other numeric columns if they exist
        for col in numeric_cols:
            if col != metric_type and col not in ['id', 'product_id']:
                agg_dict[col] = 'sum'
        
        category_perf = product_df.groupby('category').agg(agg_dict).reset_index()
        category_perf = category_perf.sort_values(metric_type, ascending=True)
        
        fig = create_horizontal_bar_chart(
            category_perf,
            metric_type,
            'category',
            f'{metric_type.title()} by Product Category'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Category summary table
        st.dataframe(category_perf, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating category performance chart: {str(e)}")
    
    # Section 2: Regional Product Performance
    st.subheader("2. Product Sales by Region and Quarter")
    
    if 'region' not in product_df.columns or 'quarter' not in product_df.columns:
        st.info("Region or Quarter data not available")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            selected_regions = st.multiselect(
                "Select Regions",
                options=product_df['region'].unique(),
                default=product_df['region'].unique(),
                key='product_regions'
            )
        
        with col2:
            selected_quarters = st.multiselect(
                "Select Quarters",
                options=sorted(product_df['quarter'].unique()),
                default=sorted(product_df['quarter'].unique()),
                key='product_quarters'
            )
        
        try:
            regional_data = product_df[
                (product_df['region'].isin(selected_regions)) &
                (product_df['quarter'].isin(selected_quarters))
            ]
            
            # Use first available numeric column for aggregation
            sales_col = [col for col in numeric_cols if col not in ['id', 'product_id']][0]
            region_perf = regional_data.groupby(['region', 'quarter'])[sales_col].sum().reset_index()
            region_perf['Quarter'] = 'Q' + region_perf['quarter'].astype(str)
            
            fig = create_grouped_bar_chart(
                region_perf,
                'region',
                sales_col,
                'Quarter',
                f'Sales by Region and Quarter'
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating regional performance chart: {str(e)}")
    
    # Section 3: Profit Margin Analysis
    margin_cols = [col for col in product_df.columns if 'margin' in col.lower() or 'profit' in col.lower()]
    
    if margin_cols:
        st.subheader("3. Profitability Analysis")
        
        margin_col = margin_cols[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                # Margin by category
                margin_data = product_df.groupby('category').agg({
                    margin_col: 'mean'
                }).reset_index().sort_values(margin_col, ascending=True)
                
                fig = create_horizontal_bar_chart(
                    margin_data,
                    margin_col,
                    'category',
                    f'Average {margin_col.title()} by Category'
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating margin chart: {str(e)}")
        
        with col2:
            try:
                # Margin statistics
                margin_stats = pd.DataFrame({
                    'Metric': ['Highest', 'Lowest', 'Average', 'Median'],
                    'Value': [
                        f"{product_df[margin_col].max():.2f}%",
                        f"{product_df[margin_col].min():.2f}%",
                        f"{product_df[margin_col].mean():.2f}%",
                        f"{product_df[margin_col].median():.2f}%"
                    ]
                })
                
                st.dataframe(margin_stats, use_container_width=True)
            except Exception as e:
                st.error(f"Error calculating margin stats: {str(e)}")
    
    # Section 4: Top Products Analysis
    st.subheader("4. Top Products by Sales")
    
    product_col = None
    if 'product_name' in product_df.columns:
        product_col = 'product_name'
    elif 'product_id' in product_df.columns:
        product_col = 'product_id'
    else:
        # Try to find any text column
        text_cols = product_df.select_dtypes(include=['object']).columns.tolist()
        if text_cols:
            product_col = text_cols[0]
    
    if product_col:
        col1, col2 = st.columns(2)
        
        with col1:
            n_products = st.slider("Number of Top Products", 5, 20, 10, key='top_products')
        
        try:
            sales_col = [col for col in numeric_cols if col not in ['id', 'product_id']][0]
            top_products = product_df.groupby(product_col).agg({
                sales_col: 'sum'
            }).nlargest(n_products, sales_col).reset_index()
            
            fig = create_horizontal_bar_chart(
                top_products,
                sales_col,
                product_col,
                f'Top {n_products} Products by {sales_col.title()}'
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating top products chart: {str(e)}")
    
    # Section 5: Product Performance Metrics
    st.subheader("5. Overall Product Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", len(product_df))
    
    with col2:
        if numeric_cols:
            sales_col = numeric_cols[0]
            st.metric(f"Total {sales_col.title()}", f"₹{format_number(product_df[sales_col].sum())}")
    
    with col3:
        st.metric("Rows", len(product_df))
    
    with col4:
        if margin_cols:
            st.metric(f"Avg {margin_cols[0].title()}", f"{product_df[margin_cols[0]].mean():.2f}%")
    
    # Section 6: Subcategory Breakdown
    if 'subcategory' in product_df.columns and 'category' in product_df.columns:
        st.subheader("6. Sales by Subcategory")
        
        selected_category = st.selectbox(
            "Select Category",
            options=product_df['category'].unique(),
            key='subcategory_filter'
        )
        
        try:
            subcat_data = product_df[product_df['category'] == selected_category]
            sales_col = [col for col in numeric_cols if col not in ['id', 'product_id']][0]
            subcat_perf = subcat_data.groupby('subcategory')[sales_col].sum().reset_index()
            subcat_perf = subcat_perf.sort_values(sales_col, ascending=True)
            
            fig = create_horizontal_bar_chart(
                subcat_perf,
                sales_col,
                'subcategory',
                f'{sales_col.title()} by Subcategory - {selected_category}'
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating subcategory chart: {str(e)}")
    
    # Raw data viewer
    with st.expander("📋 View Raw Product Data"):
        rows_to_show = st.slider("Rows to display", 10, len(product_df), 50, key='product_rows')
        st.dataframe(product_df.head(rows_to_show), use_container_width=True)
