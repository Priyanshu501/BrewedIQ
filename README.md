# BrewedIQ: Insights into Managing a Coffee Chain

A streamlit dashboard for analyzing coffee shop sales. Features interactive filters, KPI tracking, and visualiations for sales trends, time-of-day performance, top products, and store comparions.

Live Demo: **[View Dashboard](https://brewediq.streamlit.app/)**

## Table of Contents

- [About The Project](#about-the-project)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [How to Run Locally](#how-to-run-locally)
- [Data Source & Citation](#data-source--citation)

## About The Project

This project is an interactive web dashboard built with Streamlit to analyze sales data from a multi-location coffee shop. It provides a comprehensive, high-level overview of business performance, allowing users to drill down into specific metrics.

The dashboard allows users to filter the entire dataset by **store location** and **date range**. The analysis is then presented across four key areas:
1. **Sales Trends:** Analyzing revenue, transactions, and ticket size over time (daily, weekly, monthly).
2. **Time of Day:** Identifying peak hours and busiest days of the week.
3. **Product Performance:** Highlighting top-selling products and categories.
4. **Store Performance:** Comparing sales, growth, and trends acrooss different store locations.

All visualizations are created using Plotly for a clean, interactive experience.

![Dashboard Screenshot](screenshots\dashboard.png)

## Key Features

* **Global Filters:** Filter all dashboard data by one or more **Store Locations** and a specific **Date Range**.

* **KPI Cards:** At-a-glance metrics for **Total Sales**, **Total Transactions**, **Average Quantitiy per Ticket**, and **Average Sale Value**.

* **Tabbed Interface:** Cleanly organized analysis across four distinct categories.

* **Sales Trends Analysis:**
    * View metrics by 'Sales', 'Transactions', or 'Ticket Size'.
    * Change time granularitiy between 'Daily', 'Weekly', and 'Monthly'.
    * Toggle on/off a **moving average** to identify trends.
    * View **period-over-period growth** (e.g., Month-over-Month).

* **Time of Day Analysis:**
    * Bar chart of average performance by **day of the week**.
    * Line chart of average performance by **hour of the day**.
    * **Heatmap** showing product category performance by the hour.

* **Top Products Analysis:**
    * **Pie Chart** of sales/transaction distribution by product category.
    * **Treemap** for distribution by specific product type.
    * **Bar Chart** identifying the Top 5 best-selling products.

* **Store Performance Comparison:**
    * KPI breakdowns for each individual store.
    * **Line Chart** comparing sales trends across all stores.
    * **Pie Chart** showing the percentage of total sales contributed by each store.
    * **Bar Chart** comparing weekly growth rates for each location.

## Technologies Used

* **Python:** Core Programming language.
* **Streamlit:** For building and deploying the interactive web app.
* **Pandas:** For data loading, manipulation, and analysis.
* **Plotly:** For creating interactive data visualizations.
* **Jupyter Notebook:** For initial exploratory data analysis (EDA).

## File Structure
```bash
.
├── 📄 dashboard.py # Main Streamlit application file
├── 📄 vis.py # Module for all Plotly visualization functions
├── 📓 analysis.ipynb # Jupyter Notebook for initial EDA
├── 🗂️ CoffeeShopSales.csv # The dataset used by the dashboard
├── 📄 requirements.txt # Python dependencies
└── 📄 README.md # You are here!
```

## How to Run Locally

Follow these steps to get a local copy up and running.

### Prerequisites

You must have [Python](https://www.python.org/downloads/) (3.15.5 or newer) installed on your system.

### Installation

1. **Clone the repository:**
    ```sh
    git clone [https://github.com/Codon-s/BrewedIQ.git](https://github.com/Codon-s/BrewedIQ.git)

    cd BrewedIQ
    ```

2. **Create and activate a virtual environment (recommended):**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

### Running the App

Execute the following command in your terminal:

```sh
streamlit run dashboard.py
```
Open your web browser and go to ```http://localhost:8501``` to view the app.

## Data Source & Citation

The dataset used for this project is the "Coffee Shop Sales" dataset provided by **Maven Analytics**.

* **Source:** [Maven Analytics](https://mavenanalytics.io/data-playground)

* **Direct Link:** [https://mavenanalytics.io/data-playground/coffee-shop-sales](https://mavenanalytics.io/data-playground/coffee-shop-sales)