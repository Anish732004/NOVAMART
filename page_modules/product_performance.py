"""
Product Performance Page
Product hierarchy, sales analysis, and margin analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_product_sales
from utils.visualizations import (
    create_horizontal_bar_chart, create_grouped_bar_chart,
    create_line_chart, create_scatter_plot, format_number
)


def show():
    """Display Product Performance page."""
    
    st.header("🛍️ Product Performance")
    st.markdown("Analyze product hierarchy, sales, and profitability")
    
    # Load data
    product_df = load_product_sales()
    
    # Ensure year and quarter are proper data types
    if 'year' in product_df.columns:
        product_df['year'] = pd.to_numeric(product_df['year'], errors='coerce')
    if 'quarter' in product_df.columns:
        product_df['quarter'] = product_df['quarter'].astype(str)
    
    # Section 1: Sales by Category
    st.subheader("1. Sales by Product Category")
    
    if 'category' not in product_df.columns:
        st.warning("Category column not found in product data")
        return
    
    try:
        category_sales = product_df.groupby('category').agg({
            'sales': 'sum',
            'units_sold': 'sum',
            'profit': 'sum',
            'profit_margin': 'mean'
        }).reset_index().sort_values('sales', ascending=True)
        
        fig = create_horizontal_bar_chart(
            category_sales,
            'sales',
            'category',
            'Total Sales by Category'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Category summary table
        category_sales_display = category_sales.copy()
        category_sales_display['sales'] = category_sales_display['sales'].apply(lambda x: f"₹{format_number(x)}")
        category_sales_display['profit'] = category_sales_display['profit'].apply(lambda x: f"₹{format_number(x)}")
        category_sales_display['profit_margin'] = category_sales_display['profit_margin'].apply(lambda x: f"{x:.2f}%")
        category_sales_display.columns = ['Category', 'Sales', 'Units Sold', 'Profit', 'Avg Margin']
        
        st.dataframe(category_sales_display, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating category sales chart: {str(e)}")
    
    # Section 2: Sales by Region and Quarter
    st.subheader("2. Sales by Region and Quarter")
    
    if 'region' not in product_df.columns or 'quarter' not in product_df.columns:
        st.info("Region or Quarter data not available")
    else:
        col1, col2, col3 = st.columns(3)
        
        # Year filter
        if 'year' in product_df.columns:
            with col1:
                selected_years = st.multiselect(
                    "Select Years",
                    options=sorted(product_df['year'].dropna().unique()),
                    default=sorted(product_df['year'].dropna().unique()),
                    key='product_years'
                )
                year_filtered_df = product_df[product_df['year'].isin(selected_years)]
        else:
            year_filtered_df = product_df
        
        # Region filter
        with col2 if 'year' in product_df.columns else col1:
            selected_regions = st.multiselect(
                "Select Regions",
                options=sorted(year_filtered_df['region'].unique()),
                default=sorted(year_filtered_df['region'].unique()),
                key='product_regions'
            )
        
        # Quarter filter
        with col3 if 'year' in product_df.columns else col2:
            selected_quarters = st.multiselect(
                "Select Quarters",
                options=sorted(year_filtered_df['quarter'].unique()),
                default=sorted(year_filtered_df['quarter'].unique()),
                key='product_quarters'
            )
        
        try:
            regional_data = year_filtered_df[
                (year_filtered_df['region'].isin(selected_regions)) &
                (year_filtered_df['quarter'].isin(selected_quarters))
            ]
            
            region_perf = regional_data.groupby(['region', 'quarter'])['sales'].sum().reset_index()
            
            fig = create_grouped_bar_chart(
                region_perf,
                'region',
                'sales',
                'quarter',
                'Sales by Region and Quarter'
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating regional performance chart: {str(e)}")
    
    # Section 3: Profitability Analysis
    st.subheader("3. Profitability Analysis")
    
    try:
        col1, col2 = st.columns(2)
        
        with col1:
            # Margin by category
            margin_by_category = product_df.groupby('category')['profit_margin'].mean().reset_index().sort_values('profit_margin', ascending=True)
            
            fig = create_horizontal_bar_chart(
                margin_by_category,
                'profit_margin',
                'category',
                'Average Profit Margin by Category'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Margin statistics
            margin_stats = pd.DataFrame({
                'Metric': ['Highest', 'Lowest', 'Average', 'Median'],
                'Value': [
                    f"{product_df['profit_margin'].max():.2f}%",
                    f"{product_df['profit_margin'].min():.2f}%",
                    f"{product_df['profit_margin'].mean():.2f}%",
                    f"{product_df['profit_margin'].median():.2f}%"
                ]
            })
            
            st.dataframe(margin_stats, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating profitability analysis: {str(e)}")
    
    # Section 4: Top Products by Sales
    st.subheader("4. Top Products by Sales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        n_products = st.slider("Number of Top Products", 5, 20, 10, key='top_products')
    
    try:
        top_products = product_df.groupby('product_name').agg({
            'sales': 'sum',
            'units_sold': 'sum',
            'profit': 'sum'
        }).nlargest(n_products, 'sales').reset_index()
        
        fig = create_horizontal_bar_chart(
            top_products.sort_values('sales', ascending=True),
            'sales',
            'product_name',
            f'Top {n_products} Products by Sales'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top products table
        top_display = top_products.copy()
        top_display['sales'] = top_display['sales'].apply(lambda x: f"₹{format_number(x)}")
        top_display['profit'] = top_display['profit'].apply(lambda x: f"₹{format_number(x)}")
        top_display.columns = ['Product', 'Sales', 'Units Sold', 'Profit']
        
        st.dataframe(top_display, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating top products chart: {str(e)}")
    
    # Section 5: Sales Trend Over Quarters
    st.subheader("5. Sales Trend Over Quarters")
    
    try:
        # Ensure quarter is sortable
        quarter_order = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
        product_df['quarter_sort'] = pd.Categorical(product_df['quarter'], categories=quarter_order, ordered=True)
        
        trend_data = product_df.groupby('quarter_sort')['sales'].sum().reset_index().sort_values('quarter_sort')
        trend_data['quarter'] = trend_data['quarter_sort'].astype(str)
        
        fig = create_line_chart(
            trend_data,
            'quarter',
            'sales',
            'Quarterly Sales Trend'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating sales trend chart: {str(e)}")
    
    # Section 6: Sales vs Units Scatter
    st.subheader("6. Product Sales vs Units Sold")
    
    try:
        product_agg = product_df.groupby('product_name').agg({
            'sales': 'sum',
            'units_sold': 'sum',
            'category': 'first'
        }).reset_index()
        
        fig = create_scatter_plot(
            product_agg,
            'units_sold',
            'sales',
            'Sales vs Units Sold by Product',
            color_col='category',
            trendline=True
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating scatter chart: {str(e)}")
    
    # Section 7: Subcategory Performance
    st.subheader("7. Sales by Subcategory")
    
    if 'subcategory' in product_df.columns and 'category' in product_df.columns:
        try:
            selected_category = st.selectbox(
                "Select Category",
                options=sorted(product_df['category'].unique()),
                key='subcategory_filter'
            )
            
            subcat_data = product_df[product_df['category'] == selected_category]
            subcat_perf = subcat_data.groupby('subcategory').agg({
                'sales': 'sum',
                'units_sold': 'sum',
                'profit': 'sum'
            }).reset_index().sort_values('sales', ascending=True)
            
            fig = create_horizontal_bar_chart(
                subcat_perf,
                'sales',
                'subcategory',
                f'Sales by Subcategory - {selected_category}'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Subcategory table
            subcat_display = subcat_perf.copy()
            subcat_display['sales'] = subcat_display['sales'].apply(lambda x: f"₹{format_number(x)}")
            subcat_display['profit'] = subcat_display['profit'].apply(lambda x: f"₹{format_number(x)}")
            subcat_display.columns = ['Subcategory', 'Sales', 'Units Sold', 'Profit']
            
            st.dataframe(subcat_display, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating subcategory chart: {str(e)}")
    
    # Section 8: Product Ratings and Reviews
    st.subheader("8. Product Quality Metrics")
    
    if 'avg_rating' in product_df.columns and 'review_count' in product_df.columns:
        try:
            col1, col2 = st.columns(2)
            
            with col1:
                # Average rating by category
                rating_data = product_df.groupby('category')['avg_rating'].mean().reset_index().sort_values('avg_rating', ascending=True)
                
                fig = create_horizontal_bar_chart(
                    rating_data,
                    'avg_rating',
                    'category',
                    'Average Rating by Category'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Review distribution
                review_data = product_df.groupby('category')['review_count'].sum().reset_index().sort_values('review_count', ascending=True)
                
                fig = create_horizontal_bar_chart(
                    review_data,
                    'review_count',
                    'category',
                    'Total Reviews by Category'
                )
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating quality metrics: {str(e)}")
    
    # Section 9: Overall Product Metrics
    st.subheader("9. Overall Product Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", product_df['product_name'].nunique())
    
    with col2:
        st.metric("Total Sales", f"₹{format_number(product_df['sales'].sum())}")
    
    with col3:
        st.metric("Total Profit", f"₹{format_number(product_df['profit'].sum())}")
    
    with col4:
        st.metric("Avg Profit Margin", f"{product_df['profit_margin'].mean():.2f}%")
    
    # Section 10: Return Rate Analysis
    if 'return_rate' in product_df.columns:
        st.subheader("10. Return Rate Analysis")
        
        try:
            return_by_category = product_df.groupby('category')['return_rate'].mean().reset_index().sort_values('return_rate', ascending=True)
            
            fig = create_horizontal_bar_chart(
                return_by_category,
                'return_rate',
                'category',
                'Average Return Rate by Category'
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating return rate analysis: {str(e)}")
    
    # Raw data viewer
    with st.expander("📋 View Raw Product Data"):
        rows_to_show = st.slider("Rows to display", 10, len(product_df), 50, key='product_rows')
        st.dataframe(product_df.head(rows_to_show), use_container_width=True)
