''' Coffee Shop Sales: Dashboard '''
import streamlit as st
import pandas as pd
import vis

st.set_page_config(page_title="Coffee Shop Sales: Dashboard", layout='wide')

@st.cache_data
def load_data(path):
    """Load the sales data from an Excel file."""
    return pd.read_excel(path, engine='openpyxl')

df = load_data("CoffeeShopSales.xlsx")

# Sidebar Filters

store = st.sidebar.multiselect(
    "Select Store",
    df['store_location'].unique().tolist(),
    default=df['store_location'].unique().tolist()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['transaction_date'].min(), df['transaction_date'].max()]
)

df['total_amount'] = df['transaction_qty'] * df['unit_price']

# Filtered Data

filtered_data = df[
    (df['store_location'].isin(store))&
    (df['transaction_date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

# Setting Title
st.title("Dashboard")

# Showing KPIs

a,b,c,d = st.columns(4)

a.metric(
    label = 'Total Sales',
    value = f'${filtered_data.total_amount.sum():,.2f}'
)

b.metric(
    label = 'Total Transactions',
    value = f'{filtered_data.transaction_id.nunique():,}'
)

c.metric(
    label = 'Average Qty per Ticket',
    value = f'{filtered_data.transaction_qty.mean():,.2f}'
)

d.metric(
    label = 'Average Sale Value',
    value = f'${filtered_data.total_amount.sum()/filtered_data.transaction_id.nunique():,.2f}'
)

# Module Wise Analysis

tab = st.tabs([
    "Sales Trends Over Time",
    "Time of Day Analysis",
    "Top Products",
    "Store Performance"
])

## Module: Sales Trends Over Time

with tab[0]:
    st.subheader("Sales Trends Over Time")
    radio_selection = st.columns(2)

    # Data Options
    with radio_selection[0]:
        data_option = st.radio(
            "Select Data Type",
            ['Sales', 'Transactions', 'Ticket Size'],
            horizontal=True,
            index=0
        )

    # Time Granularity Selector
    with radio_selection[1]:
        granularity = st.radio(
            "Select Time Duration",
            ['Daily', 'Weekly', 'Monthly'],
            horizontal=True,
            index=2
        )

    if data_option == 'Sales':
        feature = 'total_amount'

    elif data_option == 'Transactions':
        feature = 'transaction_id'

    elif data_option == 'Ticket Size':
        feature = 'transaction_qty'

    if granularity == 'Daily':
        if feature == 'total_amount' or feature == 'transaction_qty':
            data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('D')
            )[feature].sum()
        if feature == 'transaction_id':
            data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('D')
            )[feature].nunique()


    elif granularity == 'Weekly':
        if feature == 'total_amount' or feature == 'transaction_qty':
            data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('W')
            )[feature].sum()
        if feature == 'transaction_id':
            data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('W')
            )[feature].nunique()

    elif granularity == 'Monthly':
        if feature == 'total_amount' or feature == 'transaction_qty':
            data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('M')
            )[feature].sum()
        if feature == 'transaction_id':
            data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('M')
            )[feature].nunique()


    graphs = st.columns([0.6, 0.4], gap='medium')
    
    with graphs[0]:
        st.plotly_chart(
            vis.bar_chart(data, granularity, feature),
            use_container_width=True
        )

    with graphs[1]:
        with st.container():
            st.plotly_chart(
                vis.line_chart(data, granularity, feature),
                use_container_width=True
            )                

        with st.container():
            st.plotly_chart(
                vis.growth_chart(data, granularity, feature),
                use_container_width=True
            )