# AI Sales Forecasting

A Python-based data preparation pipeline for sales forecasting that combines sales data, Google Trends, and economic indicators to create a feature-rich dataset optimized for Power BI analysis and machine learning models.

## Overview

This project processes multiple data sources to create a comprehensive monthly aggregated dataset with advanced feature engineering capabilities. The output is designed for use in Power BI dashboards and predictive analytics models.

## Features

- **Multi-source data integration**: Combines sales data, Google Trends, and economic indicators
- **Monthly aggregation**: Converts daily/weekly data to monthly granularity
- **Advanced feature engineering**:
  - Time-based features (year, month, quarter, season)
  - Lag features (1-month and 3-month revenue lags)
  - Rolling averages (3-month and 6-month windows)
  - Data normalization
  - Outlier handling (winsorization)
- **Indian season mapping**: Custom season classification for Indian market patterns
- **Missing value handling**: Interpolation and forward-fill strategies

## Requirements

- Python 3.7+
- pandas

## Installation

1. Clone this repository or navigate to the project directory:
```bash
cd ai_sales_forecasting
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Data Files

The script expects the following input CSV files in the project directory:

- `sales_data.csv` - Sales data with columns: `date`, `region`, `customer_segment`, `revenue`
- `google_trends.csv` - Google Trends data with columns: `date`, `search_index`
- `economic_indicators.csv` - Economic data with columns: `date`, `gdp_growth`, `inflation_rate`

## Usage

Run the data preparation script:

```bash
python prepare_dataset.py
```

The script will:
1. Load all input CSV files
2. Convert dates to monthly periods
3. Aggregate sales data by month, region, and customer segment
4. Aggregate Google Trends and economic indicators by month
5. Merge all datasets
6. Create advanced features (lags, rolling averages, normalization, etc.)
7. Export the final dataset to `powerbi_dataset_monthly_advanced.csv`

## Output

The script generates `powerbi_dataset_monthly_advanced.csv` with the following features:

### Base Features
- `date` - Monthly date (first day of month)
- `region` - Sales region
- `customer_segment` - Customer segment classification
- `revenue` - Aggregated monthly revenue
- `search_index` - Google Trends search index
- `gdp_growth` - GDP growth rate
- `inflation_rate` - Inflation rate

### Engineered Features
- `year`, `month`, `quarter` - Temporal features
- `is_month_end` - Boolean flag for month-end
- `season` - Indian season classification (Winter, Spring, Summer, Monsoon, Autumn)
- `rev_lag_1`, `rev_lag_3` - Revenue lag features (1 and 3 months)
- `gdp_lag_1`, `infl_lag_1` - Economic indicator lags
- `rev_roll_3`, `rev_roll_6` - Rolling average revenue (3 and 6 months)
- `trend_roll_6` - Rolling average search index (6 months)
- `revenue_norm`, `search_norm` - Normalized features (0-1 scale)
- `revenue_winsorized` - Outlier-handled revenue (1st-99th percentile)

## Project Structure

```
ai_sales_forecasting/
├── prepare_dataset.py          # Main data preparation script
├── requirements.txt            # Python dependencies
├── sales_data.csv              # Input: Sales data
├── google_trends.csv           # Input: Google Trends data
├── economic_indicators.csv     # Input: Economic indicators
├── powerbi_dataset_monthly_advanced.csv  # Output: Processed dataset
└── README.md                   # This file
```

## Notes

- The script uses Indian season mapping (Winter, Spring, Summer, Monsoon, Autumn)
- Missing values in `search_index` are interpolated
- Missing values in economic indicators are forward-filled
- Revenue outliers are clipped to the 1st-99th percentile range

## Next Steps

The generated dataset can be used for:
- Power BI visualization and dashboards
- Time series forecasting models
- Machine learning model training
- Statistical analysis and reporting

## License

This project is provided as-is for sales forecasting and data analysis purposes.

