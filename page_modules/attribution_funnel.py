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
    
    attribution_df = load_channel_attribution()
    
    col1, col2 = st.columns(2)
    
    # The attribution data has columns: channel, first_touch, last_touch, linear, time_decay, position_based
    # These represent attribution models
    attribution_models = [col for col in attribution_df.columns if col != 'channel']
    
    with col1:
        if attribution_models:
            selected_model = st.selectbox(
                "Select Attribution Model",
                options=attribution_models,
                key='attribution_model'
            )
        else:
            st.warning("No attribution models found")
            selected_model = None
    
    with col2:
        if selected_model:
            st.write(f"**Selected Model:** {selected_model.replace('_', ' ').title()}")
            st.info(f"Shows how different attribution models credit channels for conversions")
    
    # Prepare donut chart data
    if selected_model and 'channel' in attribution_df.columns:
        try:
            chart_data = attribution_df[['channel', selected_model]].copy()
            chart_data.columns = ['channel', 'contribution']
            
            fig = create_donut_chart(
                chart_data,
                'channel',
                'contribution',
                f'Channel Attribution - {selected_model.replace("_", " ").title()} Model',
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Attribution details table
            display_df = attribution_df[['channel', selected_model]].sort_values(selected_model, ascending=False)
            display_df.columns = ['Channel', selected_model.replace('_', ' ').title()]
            st.dataframe(display_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating attribution chart: {str(e)}")
    else:
        st.warning("Required columns not found in attribution data")
    
    # Section 2: Attribution Model Comparison Table
    try:
        # Create comparison table across all models
        comparison_table = attribution_df.set_index('channel')[attribution_models].round(2)
        
        st.subheader("2. Attribution Model Comparison")
        st.dataframe(comparison_table, use_container_width=True)
        
        # Key insights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Find channel with highest variation across models
            if len(attribution_models) > 0 and 'channel' in attribution_df.columns:
                channel_variation = attribution_df.set_index('channel')[attribution_models].std(axis=1)
                max_var_channel = channel_variation.idxmax()
                st.metric("Most Inconsistent Channel", max_var_channel, f"{channel_variation.max():.2f}")
        
        with col2:
            st.metric("Number of Channels", len(attribution_df))
        
        with col3:
            st.metric("Number of Models", len(attribution_models))
    except Exception as e:
        st.error(f"Error creating attribution comparison table: {str(e)}")
    
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
