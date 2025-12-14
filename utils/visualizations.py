"""
Visualization Helper Module
Contains helper functions for creating various chart types.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
from typing import Tuple, List, Optional, Dict, Any


def create_metric_cards(metrics: Dict[str, Any]):
    """
    Create metric cards for KPIs.
    
    Parameters:
    -----------
    metrics : dict
        Dictionary with metric names as keys and (value, label, color) tuples as values
    """
    cols = st.columns(len(metrics))
    
    for col, (metric_name, (value, label, color)) in zip(cols, metrics.items()):
        with col:
            st.markdown(f"""
                <div style='background-color: white; border-left: 4px solid {color}; 
                          padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <h4 style='margin: 0; color: #666;'>{label}</h4>
                    <h2 style='margin: 10px 0 0 0; color: {color};'>{value}</h2>
                </div>
                """, unsafe_allow_html=True)


def create_horizontal_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, 
                               title: str, color_col: Optional[str] = None) -> go.Figure:
    """
    Create a horizontal bar chart.
    """
    try:
        sorted_data = data.sort_values(x_col, ascending=True)
    except:
        sorted_data = data
    
    if color_col and color_col in data.columns:
        fig = px.bar(
            sorted_data,
            x=x_col,
            y=y_col,
            color=color_col,
            orientation='h',
            title=title,
            labels={x_col: x_col.replace('_', ' ').title(), 
                    y_col: y_col.replace('_', ' ').title()}
        )
    else:
        fig = px.bar(
            sorted_data,
            x=x_col,
            y=y_col,
            orientation='h',
            title=title,
            labels={x_col: x_col.replace('_', ' ').title(), 
                    y_col: y_col.replace('_', ' ').title()}
        )
    
    fig.update_layout(
        height=400,
        showlegend=True,
        hovermode='closest',
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig


def create_grouped_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, 
                            group_col: str, title: str) -> go.Figure:
    """
    Create a grouped bar chart.
    """
    fig = px.bar(
        data,
        x=x_col,
        y=y_col,
        color=group_col,
        barmode='group',
        title=title,
        labels={x_col: x_col.replace('_', ' ').title(),
                y_col: y_col.replace('_', ' ').title()}
    )
    fig.update_layout(
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig


def create_stacked_bar_chart(data: pd.DataFrame, x_col: str, y_col: str,
                            stack_col: str, title: str, mode: str = 'absolute') -> go.Figure:
    """
    Create a stacked bar chart.
    
    Parameters:
    -----------
    mode : str
        'absolute' for stacked values or 'relative' for 100% stacked
    """
    fig = px.bar(
        data,
        x=x_col,
        y=y_col,
        color=stack_col,
        title=title,
        barnorm='percent' if mode == 'relative' else None
    )
    fig.update_layout(
        height=400,
        barmode='stack',
        hovermode='x unified',
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig


def create_line_chart(data: pd.DataFrame, x_col: str, y_col: str, 
                     title: str, color_col: Optional[str] = None,
                     markers: bool = True) -> go.Figure:
    """
    Create a line chart.
    """
    fig = px.line(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        markers=markers,
        labels={x_col: x_col.replace('_', ' ').title(),
                y_col: y_col.replace('_', ' ').title()}
    )
    fig.update_layout(
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig


def create_area_chart(data: pd.DataFrame, x_col: str, y_col: str,
                     title: str, group_col: Optional[str] = None) -> go.Figure:
    """
    Create a stacked area chart.
    """
    fig = px.area(
        data,
        x=x_col,
        y=y_col,
        color=group_col,
        title=title,
        labels={x_col: x_col.replace('_', ' ').title(),
                y_col: y_col.replace('_', ' ').title()}
    )
    fig.update_layout(
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig


def create_histogram(data: pd.DataFrame, col: str, title: str, 
                    nbins: int = 30, color_col: Optional[str] = None) -> go.Figure:
    """
    Create a histogram.
    """
    fig = px.histogram(
        data,
        x=col,
        nbins=nbins,
        color=color_col,
        title=title,
        labels={col: col.replace('_', ' ').title()}
    )
    fig.update_layout(
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig


def create_box_plot(data: pd.DataFrame, x_col: str, y_col: str,
                   title: str, points: str = 'outliers') -> go.Figure:
    """
    Create a box plot.
    
    Parameters:
    -----------
    points : str
        'outliers', 'all', 'suspectedoutliers', or False
    """
    fig = px.box(
        data,
        x=x_col,
        y=y_col,
        points=points,
        title=title,
        labels={y_col: y_col.replace('_', ' ').title()}
    )
    fig.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig


def create_violin_plot(data: pd.DataFrame, x_col: str, y_col: str,
                      title: str, split_col: Optional[str] = None,
                      points: bool = True) -> go.Figure:
    """
    Create a violin plot.
    """
    fig = px.violin(
        data,
        x=x_col,
        y=y_col,
        color=split_col,
        points='all' if points else False,
        title=title,
        labels={y_col: y_col.replace('_', ' ').title()}
    )
    fig.update_layout(
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig


def create_scatter_plot(data: pd.DataFrame, x_col: str, y_col: str,
                       title: str, color_col: Optional[str] = None,
                       size_col: Optional[str] = None,
                       trendline: bool = False) -> go.Figure:
    """
    Create a scatter plot with optional trend line.
    """
    trendline_opt = 'ols' if trendline else None
    
    fig = px.scatter(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        trendline=trendline_opt,
        title=title,
        labels={x_col: x_col.replace('_', ' ').title(),
                y_col: y_col.replace('_', ' ').title()}
    )
    fig.update_layout(
        height=400,
        hovermode='closest',
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig


def create_bubble_chart(data: pd.DataFrame, x_col: str, y_col: str,
                       size_col: str, color_col: Optional[str] = None,
                       title: str = '') -> go.Figure:
    """
    Create a bubble chart.
    """
    fig = px.scatter(
        data,
        x=x_col,
        y=y_col,
        size=size_col,
        color=color_col,
        hover_data=data.columns,
        title=title,
        labels={x_col: x_col.replace('_', ' ').title(),
                y_col: y_col.replace('_', ' ').title(),
                size_col: size_col.replace('_', ' ').title()}
    )
    fig.update_layout(
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig


def create_heatmap(data: pd.DataFrame, title: str, colorscale: str = 'RdBu') -> go.Figure:
    """
    Create a correlation heatmap.
    """
    fig = px.imshow(
        data,
        color_continuous_scale=colorscale,
        title=title,
        aspect='auto',
        text_auto='.2f',
        origin='lower'
    )
    fig.update_layout(
        height=500,
        width=600,
        plot_bgcolor='white'
    )
    return fig


def create_donut_chart(data: pd.DataFrame, names_col: str, values_col: str,
                      title: str, hole: float = 0.4) -> go.Figure:
    """
    Create a donut chart.
    """
    fig = px.pie(
        data,
        names=names_col,
        values=values_col,
        title=title,
        hole=hole
    )
    fig.update_layout(
        height=400,
        showlegend=True
    )
    return fig


def create_pie_chart(data: pd.DataFrame, names_col: str, values_col: str,
                    title: str) -> go.Figure:
    """
    Create a pie chart.
    """
    fig = px.pie(
        data,
        names=names_col,
        values=values_col,
        title=title
    )
    fig.update_layout(
        height=400,
        showlegend=True
    )
    return fig


def create_sunburst_chart(data: pd.DataFrame, labels: List[str], parents: List[str],
                         values: List[float], colors: Optional[List[float]] = None,
                         title: str = '') -> go.Figure:
    """
    Create a sunburst chart.
    """
    if colors:
        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(colorscale='Viridis', cmid=2),
            text=labels,
            textposition='inside'
        ))
    else:
        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            text=labels,
            textposition='inside'
        ))
    
    fig.update_layout(
        title=title,
        height=500,
        margin=dict(t=100, l=0, r=0, b=0)
    )
    return fig


def create_treemap(data: pd.DataFrame, labels: List[str], parents: List[str],
                   values: List[float], colors: Optional[List[float]] = None,
                   title: str = '') -> go.Figure:
    """
    Create a treemap chart.
    """
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(colors=colors, colorscale='Viridis'),
        text=labels,
        textposition='middle center'
    ))
    
    fig.update_layout(
        title=title,
        height=500,
        margin=dict(t=100, l=0, r=0, b=0)
    )
    return fig


def create_funnel_chart(data: pd.DataFrame, stage_col: str, count_col: str,
                       title: str = '') -> go.Figure:
    """
    Create a funnel chart.
    """
    fig = go.Figure(go.Funnel(
        y=data[stage_col],
        x=data[count_col],
        textposition='inside',
        textinfo='value+percent total',
        marker=dict(colorscale='Blues')
    ))
    
    fig.update_layout(
        title=title,
        height=400,
        showlegend=False
    )
    return fig


def create_confusion_matrix_plot(y_true: np.ndarray, y_pred: np.ndarray) -> go.Figure:
    """
    Create a confusion matrix heatmap.
    """
    cm = confusion_matrix(y_true, y_pred)
    
    fig = px.imshow(
        cm,
        labels=dict(x='Predicted', y='Actual', color='Count'),
        x=['Negative', 'Positive'],
        y=['Negative', 'Positive'],
        color_continuous_scale='Blues',
        text_auto=True,
        title='Confusion Matrix - Lead Scoring Model'
    )
    fig.update_layout(
        height=400,
        plot_bgcolor='white'
    )
    return fig, cm


def create_roc_curve_plot(y_true: np.ndarray, y_pred_proba: np.ndarray) -> go.Figure:
    """
    Create an ROC curve plot.
    """
    fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    fig = go.Figure()
    
    # ROC curve
    fig.add_trace(go.Scatter(
        x=fpr,
        y=tpr,
        mode='lines',
        name=f'ROC Curve (AUC = {roc_auc:.3f})',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # Diagonal (random classifier)
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        name='Random Classifier',
        line=dict(color='gray', width=1, dash='dash')
    ))
    
    fig.update_layout(
        title='ROC Curve - Lead Scoring Model',
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        height=400,
        hovermode='closest',
        plot_bgcolor='rgba(240,240,240,0.5)'
    )
    
    return fig, roc_auc


def create_learning_curve_plot(data: pd.DataFrame) -> go.Figure:
    """
    Create a learning curve visualization.
    """
    # Handle flexible column names
    x_col = None
    train_col = None
    val_col = None
    
    # Find the correct column names
    for col in data.columns:
        col_lower = col.lower()
        if 'training_set' in col_lower or 'train_size' in col_lower or 'set_size' in col_lower:
            x_col = col
        elif 'train' in col_lower and 'score' in col_lower:
            train_col = col
        elif 'val' in col_lower and 'score' in col_lower:
            val_col = col
    
    # Fallback to first few columns if not found
    if not x_col:
        x_col = data.columns[0]
    if not train_col:
        train_col = data.columns[1] if len(data.columns) > 1 else None
    if not val_col:
        val_col = data.columns[2] if len(data.columns) > 2 else None
    
    if not train_col or not val_col:
        # Return a simple message if we can't find the right columns
        fig = go.Figure()
        fig.add_annotation(text="Insufficient data for learning curve visualization")
        return fig
    
    fig = go.Figure()
    
    # Training scores
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[train_col],
        name='Training Score',
        mode='lines+markers',
        line=dict(color='#1f77b4')
    ))
    
    # Validation scores
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[val_col],
        name='Validation Score',
        mode='lines+markers',
        line=dict(color='#ff7f0e')
    ))
    
    fig.update_layout(
        title='Learning Curve - Model Diagnostics',
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title='Score',
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(240,240,240,0.5)'
    )
    
    return fig


def create_feature_importance_plot(data: pd.DataFrame, name_col: str = 'feature',
                                   importance_col: str = 'importance',
                                   std_col: Optional[str] = 'std') -> go.Figure:
    """
    Create a feature importance bar chart with error bars.
    """
    try:
        data_sorted = data.sort_values(importance_col)
    except KeyError:
        # Try to find the right column
        numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            importance_col = numeric_cols[0]
            data_sorted = data.sort_values(importance_col)
        else:
            fig = go.Figure()
            fig.add_annotation(text="No numeric columns found for importance")
            return fig
    
    # Handle feature name column
    if name_col not in data.columns:
        # Try to find a suitable name column
        for col in data.columns:
            if col != importance_col and col != std_col:
                name_col = col
                break
    
    fig = go.Figure()
    
    error_info = None
    if std_col and std_col in data_sorted.columns:
        error_info = dict(
            type='data',
            array=data_sorted[std_col],
            visible=True
        )
    
    fig.add_trace(go.Bar(
        y=data_sorted[name_col],
        x=data_sorted[importance_col],
        error_x=error_info,
        orientation='h',
        marker=dict(color='#1f77b4'),
        text=data_sorted[importance_col].round(3),
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Feature Importance - Lead Scoring Model',
        xaxis_title='Importance Score',
        yaxis_title='Feature',
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(240,240,240,0.5)'
    )
    
    return fig


def create_calendar_heatmap(dates: pd.Series, values: pd.Series, title: str = '') -> alt.Chart:
    """
    Create a calendar heatmap using altair.
    """
    # Prepare data for calendar view
    df = pd.DataFrame({
        'date': dates,
        'value': values
    })
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day_of_week
    df['week'] = df['date'].dt.isocalendar().week
    
    # Create calendar heatmap
    heatmap = alt.Chart(df).mark_rect().encode(
        x=alt.X('week:O', title='Week'),
        y=alt.Y('day:O', title='Day of Week'),
        color='value:Q',
        tooltip=['date:T', 'value:Q']
    ).properties(
        width=800,
        height=200,
        title=title
    )
    
    return heatmap


def format_number(num: float, prefix: str = '', decimals: int = 0) -> str:
    """
    Format number with K, M, B suffixes.
    """
    abs_num = abs(num)
    
    if abs_num >= 1e9:
        return f"{prefix}{num/1e9:.{decimals}f}B"
    elif abs_num >= 1e6:
        return f"{prefix}{num/1e6:.{decimals}f}M"
    elif abs_num >= 1e3:
        return f"{prefix}{num/1e3:.{decimals}f}K"
    else:
        return f"{prefix}{num:.{decimals}f}"


def format_percentage(num: float, decimals: int = 1) -> str:
    """
    Format number as percentage.
    """
    return f"{num*100:.{decimals}f}%"
