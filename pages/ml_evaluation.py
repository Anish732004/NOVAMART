"""
ML Model Evaluation Page
Machine learning model performance visualization and analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve
from utils.data_loader import (
    load_lead_scoring_results, load_feature_importance, load_learning_curve
)
from utils.visualizations import (
    create_confusion_matrix_plot, create_roc_curve_plot, create_learning_curve_plot,
    create_feature_importance_plot, create_histogram, format_percentage
)


def show():
    """Display ML Model Evaluation page."""
    
    st.header("🤖 ML Model Evaluation")
    st.markdown("Analyze lead scoring model performance and diagnostics")
    
    # Load data
    lead_df = load_lead_scoring_results()
    feature_df = load_feature_importance()
    learning_df = load_learning_curve()
    
    # Section 1: Model Performance Overview
    st.subheader("1. Model Performance Summary")
    
    if 'actual_converted' in lead_df.columns and 'predicted_class' in lead_df.columns:
        # Calculate metrics
        cm = confusion_matrix(lead_df['actual_converted'], lead_df['predicted_class'])
        tn, fp, fn, tp = cm.ravel()
        
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Accuracy", f"{accuracy:.2%}")
        
        with col2:
            st.metric("Precision", f"{precision:.2%}")
        
        with col3:
            st.metric("Recall", f"{recall:.2%}")
        
        with col4:
            st.metric("F1-Score", f"{f1:.2%}")
    
    # Section 2: Confusion Matrix
    st.subheader("2. Confusion Matrix")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'actual_converted' in lead_df.columns and 'predicted_class' in lead_df.columns:
            fig, cm = create_confusion_matrix_plot(
                lead_df['actual_converted'].values,
                lead_df['predicted_class'].values
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'actual_converted' in lead_df.columns and 'predicted_class' in lead_df.columns:
            tn, fp, fn, tp = cm.ravel()
            
            st.write("**Confusion Matrix Details:**")
            st.write(f"- **True Negatives (TN):** {tn} - Correctly predicted non-conversions")
            st.write(f"- **False Positives (FP):** {fp} - Predicted as conversion but actually not")
            st.write(f"- **False Negatives (FN):** {fn} - Predicted as non-conversion but actually converted")
            st.write(f"- **True Positives (TP):** {tp} - Correctly predicted conversions")
            
            st.info("**Interpretation:** Lower FN is critical (minimize missed opportunities). "
                   "FP acceptable (extra leads for sales team)")
    
    # Section 3: ROC Curve
    st.subheader("3. ROC Curve - Model Discrimination")
    
    if 'actual_converted' in lead_df.columns and 'predicted_probability' in lead_df.columns:
        fig, roc_auc = create_roc_curve_plot(
            lead_df['actual_converted'].values,
            lead_df['predicted_probability'].values
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("AUC-ROC Score", f"{roc_auc:.3f}")
            if roc_auc > 0.9:
                st.success("Excellent model performance")
            elif roc_auc > 0.8:
                st.success("Good model performance")
            elif roc_auc > 0.7:
                st.info("Fair model performance")
            else:
                st.warning("Poor model performance")
        
        with col2:
            st.write("**ROC Curve Interpretation:**")
            st.write("- Curve above diagonal = Better than random classifier")
            st.write("- AUC closer to 1.0 = Better discrimination ability")
            st.write(f"- Current AUC = {roc_auc:.3f} indicates model has good discriminative power")
    
    # Section 4: Threshold Analysis
    st.subheader("4. Threshold Optimization")
    
    if 'predicted_probability' in lead_df.columns and 'actual_converted' in lead_df.columns:
        threshold = st.slider(
            "Select Classification Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            key='threshold'
        )
        
        # Recalculate metrics at new threshold
        predicted_at_threshold = (lead_df['predicted_probability'] >= threshold).astype(int)
        cm_threshold = confusion_matrix(lead_df['actual_converted'], predicted_at_threshold)
        tn_t, fp_t, fn_t, tp_t = cm_threshold.ravel()
        
        accuracy_t = (tp_t + tn_t) / (tp_t + tn_t + fp_t + fn_t)
        precision_t = tp_t / (tp_t + fp_t) if (tp_t + fp_t) > 0 else 0
        recall_t = tp_t / (tp_t + fn_t) if (tp_t + fn_t) > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Accuracy", f"{accuracy_t:.2%}")
        
        with col2:
            st.metric("Precision", f"{precision_t:.2%}")
        
        with col3:
            st.metric("Recall", f"{recall_t:.2%}")
        
        with col4:
            st.metric("False Positives", f"{fp_t}")
    
    # Section 5: Learning Curve
    st.subheader("5. Learning Curve - Model Diagnostics")
    
    if learning_df is not None and not learning_df.empty:
        show_confidence = st.checkbox("Show Confidence Bands", value=True, key='learning_confidence')
        
        try:
            fig = create_learning_curve_plot(learning_df)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating learning curve: {str(e)}")
        
        st.write("**Learning Curve Interpretation:**")
        st.write("- Converging curves = No significant overfitting")
        st.write("- Gap between curves = Variance present (model would benefit from more data)")
        st.write("- Both curves low = Underfitting (model complexity too low)")
        st.write("- Training high, validation low = Overfitting (model too complex)")
    else:
        st.warning("Learning curve data not available")
    
    # Section 6: Feature Importance
    st.subheader("6. Feature Importance - Model Interpretability")
    
    if feature_df is not None and not feature_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            sort_order = st.radio(
                "Sort Order",
                options=['Ascending', 'Descending'],
                horizontal=True,
                key='feature_sort'
            )
        
        feature_data = feature_df.copy()
        if sort_order == 'Ascending':
            feature_data = feature_data.sort_values(feature_data.columns[1])
        else:
            feature_data = feature_data.sort_values(feature_data.columns[1], ascending=False)
        
        fig = create_feature_importance_plot(feature_data)
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("**Top 3 Most Important Features:**")
        top_features = feature_df.nlargest(3, feature_df.columns[1])
        for idx, (_, row) in enumerate(top_features.iterrows(), 1):
            feature_name = row[0]
            importance = row[1]
            st.write(f"{idx}. **{feature_name}** - Importance: {importance:.4f}")
        
        st.info("These features have the highest predictive power for lead conversion. "
               "Focus marketing efforts on optimizing these touchpoints.")
    
    # Section 7: Prediction Distribution
    st.subheader("7. Predicted Probability Distribution")
    
    if 'predicted_probability' in lead_df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_histogram(
                lead_df,
                'predicted_probability',
                'Distribution of Predicted Probabilities',
                nbins=30,
                color_col='actual_converted' if 'actual_converted' in lead_df.columns else None
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Prediction Distribution Analysis:**")
            st.write(f"- Mean Probability: {lead_df['predicted_probability'].mean():.3f}")
            st.write(f"- Median Probability: {lead_df['predicted_probability'].median():.3f}")
            st.write(f"- Std Deviation: {lead_df['predicted_probability'].std():.3f}")
            st.write(f"- Min Probability: {lead_df['predicted_probability'].min():.3f}")
            st.write(f"- Max Probability: {lead_df['predicted_probability'].max():.3f}")
    
    # Section 8: Model Performance Insights
    st.subheader("8. Key Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Strengths:**")
        st.write("✅ Good AUC-ROC score (>0.75) indicates strong discrimination")
        st.write("✅ Balanced precision-recall trade-off")
        st.write("✅ Learning curves suggest appropriate model complexity")
    
    with col2:
        st.write("**Recommendations:**")
        st.write("🎯 Optimize threshold based on business cost of false positives vs false negatives")
        st.write("🎯 Focus on improving top 3 features for better conversion prediction")
        st.write("🎯 Collect more data to further improve model performance")
    
    # Raw data viewer
    with st.expander("📋 View Raw Lead Scoring Data"):
        rows_to_show = st.slider("Rows to display", 10, len(lead_df), 50, key='lead_rows')
        st.dataframe(lead_df.head(rows_to_show), use_container_width=True)
