import streamlit as st   # Streamlit → build web dashboard UI
import pandas as pd      # Pandas → data manipulation
import matplotlib.pyplot as plt   # Matplotlib → plotting graphs

# -----------------------------
# Title
# -----------------------------
st.title("🌍 Oil Price Analysis Dashboard")
# Main heading shown in browser

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("oil.csv")  
# Read CSV file into DataFrame

df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
# Convert Date column → proper datetime format (important for filtering & plotting)

# Extract Year & Month for aggregation (monthly/yearly analysis)
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.to_period("M")

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("📊 Dataset Preview")
st.write(df.head())
# Show first 5 rows (quick look at data)

# -----------------------------
# Filters (VERY IMPORTANT)
# -----------------------------
st.subheader("📅 Select Date Range")

# User selects start and end date
start_date = st.date_input("Start Date", df["Date"].min())
end_date = st.date_input("End Date", df["Date"].max())

# Apply date filter
filtered_df = df[(df["Date"] >= pd.to_datetime(start_date)) &
                 (df["Date"] <= pd.to_datetime(end_date))]
# Keeps only selected date range

# -----------------------------
# Dropdown Filter (Context filter)
# -----------------------------
st.subheader("🎛 Select View")

option = st.selectbox(
    "Choose Data View",
    ["Full Data", "Before War", "After War"]
)

# Apply logical filtering
if option == "Before War":
    filtered_df = filtered_df[filtered_df["Date"] < "2022-02-24"]
elif option == "After War":
    filtered_df = filtered_df[filtered_df["Date"] >= "2022-02-24"]

# -----------------------------
# Main Trend Graph
# -----------------------------
st.subheader("📈 Oil Price Trend")

fig, ax = plt.subplots(figsize=(12, 5))  
# Bigger figure → clearer visualization

# Plot line chart
ax.plot(filtered_df["Date"], filtered_df["Price"],
        label="Oil Price", color="blue", linewidth=2)

# Add vertical line for war event
ax.axvline(pd.to_datetime("2022-02-24"),
           color="red", linestyle="--",
           label="War Start")

# Labels and styling
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.set_title("Oil Price Trend Over Time")

ax.legend(loc="upper left")
ax.grid(True, linestyle="--", alpha=0.5)

# Show graph in Streamlit
st.pyplot(fig)

# -----------------------------
# Monthly Analysis
# -----------------------------
st.subheader("📊 Monthly Average Prices")

filtered_df = filtered_df.copy()  
# IMPORTANT → avoids pandas SettingWithCopyWarning

# Group by month → calculate average
monthly_avg = filtered_df.groupby("Month")["Price"].mean().sort_index()

# Plot monthly trend
fig_month, ax_month = plt.subplots(figsize=(12, 5))
monthly_avg.plot(ax=ax_month, color="green", linewidth=2)

# Reduce clutter → show fewer labels
for i, label in enumerate(ax_month.get_xticklabels()):
    if i % 3 != 0:
        label.set_visible(False)

ax_month.set_xlabel("Month")
ax_month.set_ylabel("Average Price")
ax_month.set_title("Monthly Average Oil Prices")

ax_month.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig_month)

# -----------------------------
# Yearly Analysis
# -----------------------------
st.subheader("📈 Yearly Average Prices")

# Group by year
yearly_avg = filtered_df.groupby("Year")["Price"].mean()

# Show only recent years → cleaner chart
yearly_avg = yearly_avg.tail(12)

# Plot bar chart
fig_year, ax_year = plt.subplots(figsize=(10, 5))
yearly_avg.plot(kind="bar", ax=ax_year, color="orange")

ax_year.set_xlabel("Year")
ax_year.set_ylabel("Average Price")
ax_year.set_title("Yearly Average Oil Prices (Recent Years)")

# Rotate labels → readability
ax_year.tick_params(axis='x', rotation=45)

ax_year.grid(axis="y", linestyle="--", alpha=0.5)

st.pyplot(fig_year)

# -----------------------------
# Analysis (Before vs After War)
# -----------------------------
st.subheader("📉 Analysis Result")

# Split dataset
before = filtered_df[filtered_df["Date"] < "2022-02-24"]
after = filtered_df[filtered_df["Date"] >= "2022-02-24"]

# Calculate averages
before_avg = before["Price"].mean()
after_avg = after["Price"].mean()

# Calculate impact
impact = after_avg - before_avg

# Display results in columns
col1, col2 = st.columns(2)

with col1:
    if pd.isna(before_avg):
        st.metric("Before War Avg", "No Data")
    else:
        st.metric("Before War Avg", f"{before_avg:.2f}")

with col2:
    if pd.isna(after_avg):
        st.metric("After War Avg", "No Data")
    else:
        st.metric("After War Avg", f"{after_avg:.2f}")

# Show impact clearly
if pd.isna(impact):
    st.warning("⚠️ Not enough data to calculate impact")
else:
    st.success(f"🔥 Impact: +{impact:.2f} USD increase")