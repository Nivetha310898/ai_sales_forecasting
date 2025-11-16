import pandas as pd

# -------------------------------
# 1) LOAD THE DATA
# -------------------------------
sales = pd.read_csv("sales_data.csv", parse_dates=["date"])
google = pd.read_csv("google_trends.csv", parse_dates=["date"])
eco = pd.read_csv("economic_indicators.csv", parse_dates=["date"])

# -------------------------------
# CONVERT DATE → MONTH START
# -------------------------------
sales["month_date"] = sales["date"].dt.to_period("M").dt.to_timestamp()
google["month_date"] = google["date"].dt.to_period("M").dt.to_timestamp()
eco["month_date"] = eco["date"].dt.to_period("M").dt.to_timestamp()

# -------------------------------
# 2) AGGREGATE SALES MONTHLY
# -------------------------------
sales_month = (
    sales.groupby(["month_date", "region", "customer_segment"])
    .agg({"revenue": "sum"})
    .reset_index()
)

# -------------------------------
# 3) AGGREGATE GOOGLE MONTHLY
# -------------------------------
google_month = (
    google.groupby("month_date")["search_index"]
    .mean()
    .reset_index()
)

# -------------------------------
# 4) AGGREGATE ECONOMIC DATA MONTHLY
# -------------------------------
eco_month = (
    eco.groupby("month_date")[["gdp_growth", "inflation_rate"]]
    .last()
    .reset_index()
)

# -------------------------------
# 5) MERGE ALL DATASETS (ON month_date)
# -------------------------------
df = sales_month.merge(google_month, on="month_date", how="left")
df = df.merge(eco_month, on="month_date", how="left")

# -------------------------------
# 6) RENAME month_date → date (for Power BI)
# -------------------------------
df.rename(columns={"month_date": "date"}, inplace=True)

# -------------------------------
# 7) SORT AND FILL MISSING VALUES
# -------------------------------
df = df.sort_values("date")
df["search_index"] = df["search_index"].interpolate()
df["gdp_growth"] = df["gdp_growth"].fillna(method="ffill")
df["inflation_rate"] = df["inflation_rate"].fillna(method="ffill")

# =========================================================
#  ADVANCED FEATURE ENGINEERING
# =========================================================

# TIME FEATURES
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["quarter"] = df["date"].dt.quarter
df["is_month_end"] = df["date"].dt.is_month_end

# INDIAN SEASONS
df["season"] = df["month"].map({
    12:"Winter", 1:"Winter", 2:"Winter",
    3:"Spring",
    4:"Summer", 5:"Summer", 6:"Summer",
    7:"Monsoon", 8:"Monsoon", 9:"Monsoon",
    10:"Autumn", 11:"Autumn"
})

# LAG FEATURES
df["rev_lag_1"] = df.groupby(["region","customer_segment"])["revenue"].shift(1)
df["rev_lag_3"] = df.groupby(["region","customer_segment"])["revenue"].shift(3)
df["gdp_lag_1"] = df["gdp_growth"].shift(1)
df["infl_lag_1"] = df["inflation_rate"].shift(1)

# ROLLING FEATURES
df["rev_roll_3"] = df.groupby(["region","customer_segment"])["revenue"].transform(lambda x: x.rolling(3).mean())
df["rev_roll_6"] = df.groupby(["region","customer_segment"])["revenue"].transform(lambda x: x.rolling(6).mean())
df["trend_roll_6"] = df["search_index"].rolling(6).mean()

# NORMALIZATION
df["revenue_norm"] = (df["revenue"] - df["revenue"].min()) / (df["revenue"].max() - df["revenue"].min())
df["search_norm"] = (df["search_index"] - df["search_index"].min()) / (df["search_index"].max() - df["search_index"].min())

# WINSORIZATION (OUTLIERS)
lower = df["revenue"].quantile(0.01)
upper = df["revenue"].quantile(0.99)
df["revenue_winsorized"] = df["revenue"].clip(lower, upper)

# =========================================================
# EXPORT
# =========================================================
df.to_csv("powerbi_dataset_monthly_advanced.csv", index=False, na_rep="NULL")

print("SUCCESS! File saved:", "powerbi_dataset_monthly_advanced.csv")
