"""
Attribution & Funnel Page
Channel attribution models and marketing funnel analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_channel_attribution, load_funnel_data, load_correlation_matrix
from utils.visualizations import (
    create_donut_chart, create_funnel_chart, create_heatmap, format_percentage
)


def show():
    """Display Attribution & Funnel page."""
    
    st.header("🎯 Attribution & Funnel Analysis")
    st.markdown("Analyze channel attribution models and marketing funnel performance")
    
    # Section 1: Attribution Model Comparison
    st.subheader("1. Channel Attribution Model Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        attribution_df = load_channel_attribution()
        
        if 'attribution_model' in attribution_df.columns:
            models = attribution_df['attribution_model'].unique()
            selected_model = st.selectbox(
                "Select Attribution Model",
                options=models,
                key='attribution_model'
            )
            
            model_data = attribution_df[attribution_df['attribution_model'] == selected_model]
        else:
            model_data = attribution_df
            selected_model = "Overall"
    
    with col2:
        st.write(f"**Selected Model:** {selected_model}")
        st.info(f"Shows how different attribution models credit channels differently for conversions")
    
    # Prepare donut chart data
    if 'channel' in model_data.columns and 'contribution_percent' in model_data.columns:
        fig = create_donut_chart(
            model_data,
            'channel',
            'contribution_percent',
            f'Channel Attribution - {selected_model} Model',
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Attribution details table
        st.dataframe(model_data[['channel', 'contribution_percent']].sort_values('contribution_percent', ascending=False),
                    use_container_width=True)
    else:
        st.warning("Required columns not found in attribution data")
    
    # Section 2: Attribution Model Comparison Table
    if 'attribution_model' in attribution_df.columns:
        st.subheader("2. Attribution Model Comparison")
        
        pivot_table = attribution_df.pivot_table(
            index='channel',
            columns='attribution_model',
            values='contribution_percent',
            aggfunc='sum'
        ).fillna(0).round(2)
        
        st.dataframe(pivot_table, use_container_width=True)
        
        # Key insights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Google Ads credit variation
            if 'Google Ads' in pivot_table.index:
                ga_credits = pivot_table.loc['Google Ads'].values
                st.metric("Google Ads Credit Range",
                         f"{ga_credits.min():.1f}% - {ga_credits.max():.1f}%")
        
        with col2:
            # Email credit variation
            if 'Email' in pivot_table.index:
                email_credits = pivot_table.loc['Email'].values
                st.metric("Email Credit Range",
                         f"{email_credits.min():.1f}% - {email_credits.max():.1f}%")
        
        with col3:
            st.metric("Number of Models", len(attribution_df['attribution_model'].unique()))
    
    # Section 3: Marketing Funnel
    st.subheader("3. Marketing Funnel Analysis")
    
    funnel_df = load_funnel_data()
    
    if 'stage' in funnel_df.columns and 'visitors' in funnel_df.columns:
        # Create funnel chart
        funnel_sorted = funnel_df.sort_values('visitors', ascending=True)
        
        fig = create_funnel_chart(
            funnel_sorted,
            'stage',
            'visitors',
            'Marketing Funnel - Visitor Flow'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate conversion rates
        funnel_df_sorted = funnel_df.sort_values('visitors', ascending=False).reset_index(drop=True)
        funnel_df_sorted['conversion_rate'] = funnel_df_sorted['visitors'].pct_change() * -100
        funnel_df_sorted['cumulative_drop'] = (1 - funnel_df_sorted['visitors'] / funnel_df_sorted['visitors'].iloc[0]) * 100
        
        st.subheader("Funnel Conversion Rates")
        
        funnel_table = pd.DataFrame({
            'Stage': funnel_df_sorted['stage'],
            'Visitors': funnel_df_sorted['visitors'],
            'Drop-off': funnel_df_sorted['conversion_rate'].apply(lambda x: f"{abs(x):.1f}%" if pd.notna(x) else "-"),
            'Cumulative Loss': funnel_df_sorted['cumulative_drop'].apply(lambda x: f"{x:.1f}%")
        })
        
        st.dataframe(funnel_table, use_container_width=True)
        
        # Key insights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            max_drop_idx = funnel_df_sorted['conversion_rate'].idxmax()
            if pd.notna(max_drop_idx):
                st.metric("Biggest Drop-off",
                         funnel_df_sorted.iloc[max_drop_idx]['stage'],
                         f"{abs(funnel_df_sorted.iloc[max_drop_idx]['conversion_rate']):.1f}%")
        
        with col2:
            overall_conversion = (funnel_df_sorted['visitors'].iloc[-1] / funnel_df_sorted['visitors'].iloc[0]) * 100
            st.metric("Overall Conversion",
                     f"{overall_conversion:.1f}%")
        
        with col3:
            st.metric("Total Visitors",
                     f"{funnel_df_sorted['visitors'].iloc[0]:,.0f}")
    else:
        st.warning("Funnel data not available")
    
    # Section 4: Correlation Heatmap
    st.subheader("4. Marketing Metrics Correlation Matrix")
    
    correlation_df = load_correlation_matrix()
    
    if correlation_df is not None and not correlation_df.empty:
        fig = create_heatmap(
            correlation_df,
            'Correlation Matrix - Marketing Metrics'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Key correlations
        st.write("**Key Correlations:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Strong Positive Correlations:**")
            correlations_flat = []
            for i in range(len(correlation_df.columns)):
                for j in range(i+1, len(correlation_df.columns)):
                    corr_value = correlation_df.iloc[i, j]
                    if corr_value > 0.7:
                        correlations_flat.append({
                            'Variable 1': correlation_df.columns[i],
                            'Variable 2': correlation_df.columns[j],
                            'Correlation': f"{corr_value:.3f}"
                        })
            
            if correlations_flat:
                st.dataframe(pd.DataFrame(correlations_flat), use_container_width=True)
            else:
                st.info("No strong positive correlations found")
        
        with col2:
            st.write("**Strong Negative Correlations:**")
            correlations_flat = []
            for i in range(len(correlation_df.columns)):
                for j in range(i+1, len(correlation_df.columns)):
                    corr_value = correlation_df.iloc[i, j]
                    if corr_value < -0.7:
                        correlations_flat.append({
                            'Variable 1': correlation_df.columns[i],
                            'Variable 2': correlation_df.columns[j],
                            'Correlation': f"{corr_value:.3f}"
                        })
            
            if correlations_flat:
                st.dataframe(pd.DataFrame(correlations_flat), use_container_width=True)
            else:
                st.info("No strong negative correlations found")
    else:
        st.warning("Correlation matrix data not available")
    
    # Raw data viewers
    st.markdown("---")
    
    with st.expander("📋 View Raw Attribution Data"):
        st.dataframe(attribution_df, use_container_width=True)
    
    with st.expander("📋 View Raw Funnel Data"):
        st.dataframe(funnel_df, use_container_width=True)
