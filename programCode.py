import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 读取数据
file_path = "DerivativeData_TimeSeries.csv"
df = pd.read_csv(file_path)

df.columns = [col.strip().lower() for col in df.columns]

x_col = "period"
y_col = "value"
category_col = "risk category"

df[x_col] = pd.to_datetime(df[x_col], errors='coerce')
df = df.dropna(subset=[x_col])
df = df.sort_values(by=x_col)

risk_categories = df[category_col].unique()

# 侧边栏翻页机制
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Info", "📈 Time Series Analysis", "🌍 Geospatial Analysis"])

# Info 页面
if page == "Info":
    st.title("Global Derivative Transactions Dashboard")
    st.markdown("""
    ## 🌍 Overview
    **Data Source:** *The data is sourced from the **Bank for International Settlements (BIS)**.*
    
    This dashboard allows users to explore global derivative transactions through **interactive visualizations**.

    ### 🔹 Time Series Analysis
    - **Description**: Examines derivative transaction trends across different risk categories.
    - **Included Data**: Turnover - notional amounts (daily average) in **USD billions**.
    - **Time Range**: Covers multiple historical periods.
    - **Usage**:
      - Select risk categories in the sidebar.
      - Hover over data points for transaction details.
      - Use the **range slider** to zoom in on specific timeframes.
    
    ### 🔹 Geospatial Analysis
    - **Description**: Displays country-level derivative transaction volumes on an interactive map.
    - **Included Data**: Aggregated transactions per country in **USD billions**.
    - **Available Time Periods**: Selectable quarters (*2023-Q4, 2024-Q2, 2024-Q3*).
    - **Usage**:
      - Select a **time period** from the sidebar.
      - Hover over a country to view its transaction volume.
      - Click on a country to download **historical transaction data** (if available).
    
    🛠 **Navigation:** Use the left sidebar to switch between analysis pages.
    """)

# Time Series Analysis 页面
elif page == "📈 Time Series Analysis":
    st.title("📈 Global Derivative Transactions by " + category_col)
    st.markdown("This dashboard provides an overview of global derivative transactions by risk category.")
    st.markdown("Calculation index: **Turnover - notional amounts (daily average) in USD billions.**")
    st.sidebar.header("⚙️ Settings")
    
    selected_categories = st.sidebar.multiselect(
        "Select Risk Category:",
        options=risk_categories,
        default=risk_categories[:1]
    )
    
    filtered_df = df[df[category_col].isin(selected_categories)]
    
    fig = go.Figure()
    
    for category in selected_categories:
        category_df = filtered_df[filtered_df[category_col] == category]
        fig.add_trace(go.Scatter(
            x=category_df[x_col],
            y=category_df[y_col],
            mode='lines',
            name=category
        ))
    
    fig.update_xaxes(rangeslider_visible=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.subheader("📃 Data Preview")
    st.download_button(
        label="📥 Download Data",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )
    
    st.dataframe(filtered_df, height=300, width=1000)
    
    st.markdown("<br>📌 *The data is sourced from the **Bank for International Settlements (BIS).***", unsafe_allow_html=True)

# Geospatial Analysis 页面
else:
    st.title("🌍 Global Derivative Transactions Map")
    file_path_geo = "DerivativeData_Geo.csv"
    df_geo = pd.read_csv(file_path_geo)
    
    url_file_path = "CountryDataURL_list.xlsx"
    df_urls = pd.read_excel(url_file_path)
    
    currency_to_country = {
        "Australian Dollar": "Australia",
        "Brazilian Real": "Brazil",
        "Canadian Dollar": "Canada",
        "Swiss Franc": "Switzerland",
        "Renminbi": "China",
        "Euro": "Eurozone",
        "British Pound": "United Kingdom",
        "Indian Rupee": "India",
        "Japanese Yen": "Japan",
        "Mexican Peso": "Mexico",
        "Russian Ruble": "Russia",
        "US Dollar": "United States",
        "South African Rand": "South Africa",
        "New Zealand Dollar": "New Zealand",
        "Singapore Dollar": "Singapore",
        "Hong Kong Dollar": "Hong Kong",
        "South Korean Won": "South Korea",
    }
    
    df_geo["Country"] = df_geo["Unnamed: 0"].map(currency_to_country)
    df_geo["Category"] = df_geo["Unnamed: 0"].apply(lambda x: "Interest Rate" if x == "Interest rate" else "Foreign Exchange")
    
    df_forex = df_geo[df_geo["Category"] == "Foreign Exchange"].drop(columns=["Category"])
    df_forex_grouped = df_forex.groupby("Country").sum().reset_index()
    
    df_interest_rate = df_geo[df_geo["Category"] == "Interest Rate"].drop(columns=["Country", "Category"])
    df_interest_rate_total = df_interest_rate.sum(numeric_only=True).reset_index()
    df_interest_rate_total.columns = ["Period", "Total Interest Rate Volume"]
    
    df_total_transactions = df_forex_grouped.copy()
    df_total_transactions.set_index("Country", inplace=True)
    interest_rate_sums = df_interest_rate_total.set_index("Period")["Total Interest Rate Volume"]
    
    for period in interest_rate_sums.index:
        df_total_transactions[period] = df_total_transactions.get(period, 0) + interest_rate_sums[period]
    
    df_total_transactions.reset_index(inplace=True)
    
    st.sidebar.header("📌 Select Time Period for Map")
    time_options = ["2023-Q4", "2024-Q2", "2024-Q3"]
    selected_time = st.sidebar.selectbox("Select Time Period:", time_options)
    total_transaction_value = df_total_transactions[selected_time].sum()
    st.sidebar.markdown(f"**Total Transactions ({selected_time}):** `{total_transaction_value:,.2f}`")
    
    df_map = df_total_transactions[["Country", selected_time]].rename(columns={selected_time: "Transaction Volume"})
    
    country_coords = {
        "United States": [-98.35, 39.50],
        "Canada": [-106.35, 56.13],
        "United Kingdom": [-3.44, 55.38],
        "Australia": [133.77, -25.27],
        "Brazil": [-51.93, -14.24],
        "India": [78.96, 20.59],
        "China": [104.19, 35.86],
        "Japan": [138.25, 36.20],
        "South Africa": [22.94, -30.56],
        "Mexico": [-102.55, 23.63],
        "Russia": [105.32, 61.52],
        "New Zealand": [174.89, -40.90],
        "Switzerland": [8.23, 46.82],
        "Eurozone": [10.45, 51.17],
        "South Korea": [127.98, 37.57],
        "Singapore": [103.82, 1.35],
        "Hong Kong": [114.17, 22.32],
    }
    
    df_map["lat"] = df_map["Country"].map(lambda x: country_coords.get(x, [None, None])[1])
    df_map["lon"] = df_map["Country"].map(lambda x: country_coords.get(x, [None, None])[0])
    df_map = df_map.dropna(subset=["lat", "lon"])
    
    fig = px.scatter_mapbox(
        df_map, lat="lat", lon="lon", size="Transaction Volume",
        color="Transaction Volume", hover_name="Country",
        hover_data={"lat": False, "lon": False, "Transaction Volume": ":,.0f"},
        color_continuous_scale="Viridis", size_max=50, zoom=0.5,
        mapbox_style="carto-positron"
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # **下载国家数据**
    selected_country = st.selectbox("Select a Country:", df_map["Country"].unique())

    # **匹配 URL**
    country_currency = [k for k, v in currency_to_country.items() if v == selected_country]
    country_url = df_urls[df_urls["currency"].isin(country_currency)]["url"].values

    if len(country_url) > 0:
        data_url = country_url[0]

        # 读取 CSV 数据
        try:
            df_country = pd.read_csv(data_url)
            
            # 生成 CSV 下载
            csv = df_country.to_csv(index=False).encode("utf-8")
            st.download_button(
                label=f"Download {selected_country} Data",
                data=csv,
                file_name=f"{selected_country}_transactions.csv",
                mime="text/csv"
            )    
            # 显示数据预览
            st.subheader(f"📃 {selected_country} - Historical Transactions")
            st.dataframe(df_country.head(10), height=300, width=1000)
            
           
        except:
            st.warning(f"Failed to fetch data for {selected_country}.")
    else:
        st.warning(f"No data available for {selected_country}.")
    
    st.markdown("<br>📌 *The data is sourced from the **Bank for International Settlements (BIS).***", unsafe_allow_html=True)
