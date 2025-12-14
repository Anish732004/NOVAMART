import streamlit as st
import pandas as pd
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="NovaMart Marketing Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🎯 NovaMart Marketing Analytics Dashboard")
st.markdown("""
    **Interactive marketing analytics platform for NovaMart - A rapidly growing omnichannel retail company**
    
    Explore marketing performance, customer behavior, product sales, and AI model insights across multiple dimensions.
""")

# Sidebar navigation
st.sidebar.title("📍 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select a page:",
    options=[
        "📊 Executive Overview",
        "📈 Campaign Analytics",
        "👥 Customer Insights",
        "🛍️ Product Performance",
        "🗺️ Geographic Analysis",
        "🎯 Attribution & Funnel",
        "🤖 ML Model Evaluation"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info(
    """
    **About this Dashboard**
    
    This dashboard analyzes NovaMart's marketing operations across:
    - 11 CSV data files
    - 20+ interactive visualizations
    - Real-time performance metrics
    - Customer segmentation analysis
    - Geographic insights across India
    - ML model evaluation
    """
)

# Route to selected page
if page == "📊 Executive Overview":
    from pages import executive_overview
    executive_overview.show()

elif page == "📈 Campaign Analytics":
    from pages import campaign_analytics
    campaign_analytics.show()

elif page == "👥 Customer Insights":
    from pages import customer_insights
    customer_insights.show()

elif page == "🛍️ Product Performance":
    from pages import product_performance
    product_performance.show()

elif page == "🗺️ Geographic Analysis":
    from pages import geographic_analysis
    geographic_analysis.show()

elif page == "🎯 Attribution & Funnel":
    from pages import attribution_funnel
    attribution_funnel.show()

elif page == "🤖 ML Model Evaluation":
    from pages import ml_evaluation
    ml_evaluation.show()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; margin-top: 20px;'>
        <p>NovaMart Marketing Analytics Dashboard | Built with Streamlit</p>
        <p>Data source: NovaMart Marketing Dataset (2023-2024)</p>
    </div>
    """,
    unsafe_allow_html=True
)
