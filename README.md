# NovaMart Marketing Analytics Dashboard

A comprehensive, interactive marketing analytics dashboard built with Streamlit for NovaMart, a rapidly growing omnichannel retail company operating across India.

## 📊 Dashboard Overview

This dashboard provides marketing teams with tools to:
- Monitor campaign performance across channels and regions
- Analyze customer behavior and segmentation
- Track product sales and profitability
- Evaluate geographic market penetration
- Assess marketing funnel effectiveness
- Analyze channel attribution models
- Evaluate AI-powered lead scoring model performance

## 🎯 Features

### 7 Interactive Dashboard Pages

#### 1. **Executive Overview** 📊
- **Key KPI Cards**: Total Revenue, Conversions, ROAS, Customer Count
- **Revenue Trend Chart**: Track revenue over time with aggregation controls (daily/weekly/monthly)
- **Channel Performance**: Compare channels by revenue, conversions, or ROAS
- **Channel Metrics Summary**: Detailed metrics table with impressions, clicks, spend, CTR, and ROAS

#### 2. **Campaign Analytics** 📈
- **Revenue Trend Analysis**: Multi-channel temporal analysis with date range selector
- **Cumulative Conversions**: Area chart showing cumulative growth by channel
- **Regional Performance by Quarter**: Grouped bar chart comparing regions across quarters
- **Campaign Type Contribution**: Stacked bar chart with absolute/100% stacked modes
- **Detailed Campaign Metrics**: Comprehensive metrics table by channel

#### 3. **Customer Insights** 👥
- **Age Distribution Histogram**: Analyze customer age demographics with adjustable bin sizes
- **Lifetime Value by Segment**: Box plot showing LTV distribution across customer segments
- **Satisfaction Score Distribution**: Violin plot by NPS category with optional channel split
- **Income vs Lifetime Value**: Scatter plot with optional trend line showing correlation
- **Customer Engagement Metrics**: Churn rate, average purchases, satisfaction scores
- **Segment Summary**: Breakdown of customer segments with key metrics

#### 4. **Product Performance** 🛍️
- **Product Category Sales**: Horizontal bar chart with metric selection (sales/units/margins)
- **Regional Product Performance**: Grouped bar chart with region and quarter filters
- **Profitability Analysis**: Margin analysis by category with statistics
- **Top Products Analysis**: Top N products by sales with adjustable count
- **Subcategory Breakdown**: Drill-down analysis within product categories

#### 5. **Geographic Analysis** 🗺️
- **State Revenue Performance**: Comprehensive state-level analysis with metric selection
- **Top Performing States**: Identify high-revenue, high-customer, highest-penetration states
- **Market Penetration Analysis**: Track market presence across regions
- **YoY Growth Analysis**: Identify fastest-growing markets
- **Customer Satisfaction by Region**: Regional service quality metrics
- **State Classification**: High performers vs growth opportunity states

#### 6. **Attribution & Funnel** 🎯
- **Channel Attribution Models**: Compare first-touch, last-touch, linear, and other models
- **Donut Chart Visualization**: Visual channel credit distribution
- **Marketing Funnel**: Track visitor flow from awareness to purchase
- **Conversion Rates**: Stage-by-stage drop-off analysis
- **Correlation Heatmap**: Identify strong relationships between marketing metrics

#### 7. **ML Model Evaluation** 🤖
- **Confusion Matrix**: Heatmap visualization of model predictions
- **ROC Curve**: AUC-ROC analysis with optimal threshold identification
- **Learning Curve**: Model diagnostics showing training vs validation performance
- **Feature Importance**: Horizontal bar chart with error bars showing predictive power
- **Threshold Optimization**: Interactive slider to adjust classification threshold
- **Prediction Distribution**: Histogram of predicted probabilities

## 🗂️ Project Structure

```
NovaMart/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── marketing_dataset/              # Data files
│   ├── campaign_performance.csv
│   ├── customer_data.csv
│   ├── product_sales.csv
│   ├── lead_scoring_results.csv
│   ├── feature_importance.csv
│   ├── learning_curve.csv
│   ├── geographic_data.csv
│   ├── channel_attribution.csv
│   ├── funnel_data.csv
│   ├── customer_journey.csv
│   ├── correlation_matrix.csv
│   └── Assignment.txt
├── pages/                          # Dashboard pages
│   ├── __init__.py
│   ├── executive_overview.py
│   ├── campaign_analytics.py
│   ├── customer_insights.py
│   ├── product_performance.py
│   ├── geographic_analysis.py
│   ├── attribution_funnel.py
│   └── ml_evaluation.py
└── utils/                          # Utility modules
    ├── __init__.py
    ├── data_loader.py              # Data loading and caching
    └── visualizations.py           # Chart creation functions
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Installation

1. **Clone or download the repository**
   ```bash
   cd /path/to/NovaMart
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

5. **Access the dashboard**
   - Open your browser and go to `http://localhost:8501`

## 🚀 Deployment on Streamlit Cloud

### Step-by-Step Guide

1. **Prepare your GitHub repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Marketing Analytics Dashboard"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select:
     - Repository: Your GitHub repo
     - Branch: `main`
     - Main file path: `app.py`
   - Click "Deploy"

3. **Live URL**
   - Your dashboard will be available at `https://share.streamlit.io/your-username/repo-name`

## 📊 Dataset Overview

The dashboard uses 11 interconnected CSV files:

| File | Records | Key Purpose |
|------|---------|-------------|
| campaign_performance.csv | 5,858 | Daily marketing metrics (impressions, clicks, conversions, spend, revenue) |
| customer_data.csv | 5,000 | Customer demographics and behavior (age, income, LTV, satisfaction) |
| product_sales.csv | 1,440 | Hierarchical product sales (category, subcategory, product, region, quarter) |
| lead_scoring_results.csv | 2,000 | ML model predictions and probabilities |
| feature_importance.csv | N/A | Feature importance scores with error bars |
| learning_curve.csv | N/A | Training/validation scores at different set sizes |
| geographic_data.csv | 15 | State-level metrics (revenue, customers, penetration, YoY growth) |
| channel_attribution.csv | N/A | Attribution model comparison (first-touch, last-touch, linear) |
| funnel_data.csv | N/A | Marketing funnel stages (Awareness → Purchase) |
| customer_journey.csv | N/A | Multi-touchpoint customer paths (for Sankey diagrams) |
| correlation_matrix.csv | N/A | Pre-computed correlations between marketing metrics |

## 🎨 Features & Interactions

### Data Filtering & Selection
- **Date Range Selector**: Filter campaigns by custom date ranges
- **Multi-select Dropdowns**: Filter by channels, regions, segments
- **Metric Selectors**: Switch between revenue, conversions, ROAS
- **Aggregation Levels**: Toggle between daily, weekly, monthly views

### Interactive Visualizations
- **Hover Tooltips**: Detailed information on data points
- **Click Drill-down**: Navigate hierarchical data (treemaps, sunbursts)
- **Responsive Layout**: Adapts to different screen sizes
- **Export Options**: Download filtered data and charts

### Performance Optimizations
- **Cached Data Loading**: @st.cache_data decorator for efficient data handling
- **Lazy Rendering**: Charts load on demand
- **Responsive Design**: st.columns() for adaptive layouts

## 💡 Key Insights Revealed

### Campaign Analytics
✅ Google Ads and Email drive highest revenue  
✅ West and South regions consistently outperform  
✅ Clear seasonality with Q4 festive season peaks  
✅ Lead generation campaigns consume largest budget share

### Customer Behavior
✅ Customer base skews toward 25-40 age range  
✅ Premium segment shows highest LTV and widest spread  
✅ Strong positive correlation between income and LTV  
✅ Churn segment reveals high-value lost opportunities

### Product Performance
✅ Electronics dominates sales volume  
✅ Fashion has highest profit margins  
✅ High-volume low-margin products identified for pricing review

### Geographic Insights
✅ Maharashtra and Karnataka are top performers  
✅ Eastern states show lower penetration but growth potential  
✅ Metro cities have higher premium segment concentration

### Lead Scoring Model
✅ AUC-ROC around 0.75-0.80 indicates good model  
✅ Webinar attendance and form submissions are strongest predictors  
✅ Model shows no significant overfitting
✅ Optimal classification threshold around 0.4-0.5

## 🔧 Code Quality

### Best Practices Implemented
- **Modular Architecture**: Separate functions for each visualization
- **Data Caching**: Efficient data loading with streamlit cache
- **Clear Variable Names**: Self-documenting code
- **Comprehensive Docstrings**: Function-level documentation
- **Error Handling**: Graceful fallbacks for missing data
- **Code Comments**: Key logic explained for maintainability

### File Organization
```python
# Data loading module
utils/data_loader.py
  - load_campaign_performance()
  - load_customer_data()
  - load_all_data()

# Visualization utilities
utils/visualizations.py
  - create_metric_cards()
  - create_horizontal_bar_chart()
  - create_roc_curve_plot()
  - ... 20+ chart functions
```

## 📈 Visualization Types Implemented

| Chart Type | Count | Pages | Purpose |
|-----------|-------|-------|---------|
| Bar Charts | 12+ | All | Comparison and ranking |
| Line Charts | 3+ | Campaign, Executive | Temporal trends |
| Area Charts | 2+ | Campaign | Cumulative analysis |
| Scatter/Bubble | 2+ | Customer, Product | Relationship analysis |
| Distribution | 3+ | Customer | Customer segmentation |
| Heatmap | 2+ | ML, Attribution | Correlation & matrix |
| Funnel | 1 | Attribution | Conversion stages |
| Donut/Pie | 1+ | Attribution | Part-to-whole |
| Confusion Matrix | 1 | ML | Model classification |
| ROC Curve | 1 | ML | Model discrimination |

## 🎓 Learning Outcomes

By using this dashboard, you will learn:
- ✅ Selecting appropriate chart types for different analytical tasks
- ✅ Visual design principles (color usage, labeling, accessibility)
- ✅ Building interactive dashboards with Streamlit
- ✅ ML model performance visualization and interpretation
- ✅ Deriving meaningful business insights from data

## 🧪 Testing & Validation

### Data Validation
- All data files checked for missing values
- Date formats standardized
- Numeric values validated for outliers

### Functionality Testing
- All 7 pages load without errors
- All filters and interactions work correctly
- Responsive design tested on multiple screen sizes
- Performance optimized for large datasets

## 📝 Configuration

### Streamlit Config (Optional)
Create a `.streamlit/config.toml` file for custom settings:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#f0f2f6"
secondaryBackgroundColor = "#ffffff"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false
```

## 🆘 Troubleshooting

### Common Issues

**Issue**: ModuleNotFoundError when running
```bash
# Solution: Ensure you're in the correct directory
cd /path/to/NovaMart
python -m streamlit run app.py
```

**Issue**: Data files not found
```
# Solution: Ensure marketing_dataset/ folder is in the same directory as app.py
```

**Issue**: Memory error with large datasets
```python
# Solution: Use st.cache_data decorator (already implemented)
```

## 📞 Support & Contact

For issues or questions:
1. Check the [Streamlit Docs](https://docs.streamlit.io)
2. Review the assignment requirements in `marketing_dataset/Assignment.txt`
3. Check data format in CSV files

## 📄 License

This project is created for the Masters of AI in Business Program.

## 🎯 Next Steps & Enhancements

### Bonus Features (Optional)
- ✨ Add Sankey diagram for customer journey visualization
- ✨ Animated charts showing performance evolution
- ✨ Precision-Recall curve for model evaluation
- ✨ Dark mode theme toggle
- ✨ CSV/Excel export functionality

### Future Improvements
- Real-time data integration
- Scheduled report generation
- Advanced forecasting models
- Custom alert thresholds
- User authentication & roles
- Multi-language support

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Charts](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn ML Models](https://scikit-learn.org/stable/)
- [Altair Visualization Grammar](https://altair-viz.github.io/)

---

**Built with ❤️ for NovaMart's Marketing Analytics**

Last Updated: December 2024
