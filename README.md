# Derivative-Project
# 📊 Global Derivative Transactions Dashboard

## Overview
This project provides an interactive **data visualization dashboard** to analyze **global derivative transactions** using historical data from the **Bank for International Settlements (BIS)**. The dashboard includes:

- **Time Series Analysis:** Analyzes transaction trends across different risk categories.
- **Geospatial Analysis:** Visualizes transaction volumes by country on an interactive map.
- **Customizable Filters:** Allows users to explore data through various risk categories and time periods.

## 📂 Project Structure
```
├── mainData
│   ├── CountryDataURL_list.xlsx       # External links to country-specific data
│   ├── DerivativeData_Geo.csv         # Country-level transaction data
│   ├── DerivativeData_TimeSeries.csv  # Time series transaction data
│
├── rawData
│   ├── derivativeData.csv             # Raw transaction dataset
│
├── README.md                          # Project documentation
├── programCode.py                      # Main Streamlit dashboard script
```

## 🚀 Features
### 🔹 Time Series Analysis
- **Data:** Turnover - notional amounts (daily average) in **USD billions**.
- **Filters:** Users can select specific risk categories.
- **Interactivity:**
  - Hover over points for exact transaction values.
  - Use the range slider to zoom into specific time periods.
  - Download filtered transaction data as CSV.

### 🔹 Geospatial Analysis
- **Data:** Aggregated transaction volumes per country.
- **Filters:** Select a **quarterly time period** for analysis.
- **Interactivity:**
  - Hover over countries to view transaction volumes.
  - Click on a country to download detailed transaction data.
  - View color-coded transaction intensities.

## ⚙️ Installation & Usage
### 1️⃣ Install Required Libraries
Make sure you have **Python 3.8+** installed. Install dependencies using:
```sh
pip install streamlit pandas plotly openpyxl
```

### 2️⃣ Run the Dashboard
Execute the following command in the terminal:
```sh
streamlit run programCode.py
```

### 3️⃣ Open in Browser
Once the command runs, you will see a **local URL** (e.g., `http://localhost:8501`). Open it in your browser to access the dashboard.

## 📌 Data Source
All data used in this project is sourced from the **Bank for International Settlements (BIS)**.

## 📜 License
This project is licensed under the **MIT License**.

## 📬 Contact
For any questions or suggestions, feel free to reach out!

---
✨ *Happy analyzing!* 🚀

