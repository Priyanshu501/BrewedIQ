''' Coffee Shop Sales: Dashboard '''
import calendar
import streamlit as st
import pandas as pd
import vis

st.set_page_config(page_title="Coffee Shop Sales: Dashboard", layout='wide')

@st.cache_data
def load_data(path):
    """Load the sales data from a Csv file."""
    return pd.read_csv(path)

df = load_data("./CoffeeShopSales.csv")
df['transaction_date'] = pd.to_datetime(df['transaction_date'], format='%d-%m-%Y')

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

filtered_data2 = df[
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
    st.header("Sales Trends Over Time")
    radio_selection = st.columns(2)

    # Data Options
    with radio_selection[0]:
        data_option = st.radio(
            "Select Data Type",
            ['Sales', 'Transactions', 'Ticket Size'],
            horizontal=True,
            key='Sales_Trends',
            index=0
        )

    # Time Granularity Selector
    with radio_selection[1]:
        granularity = st.radio(
            "Select Time Granularity:",
            ['Daily', 'Weekly', 'Monthly'],
            horizontal=True,
            index=2
        )

    if data_option == 'Sales':
        FEATURE = 'total_amount'

    elif data_option == 'Transactions':
        FEATURE = 'transaction_id'

    elif data_option == 'Ticket Size':
        FEATURE = 'transaction_qty'
    else:
        FEATURE = 'total_amount'

    if granularity == 'Daily':
        if FEATURE == 'total_amount' or FEATURE == 'transaction_qty':
            data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('D')
            )[FEATURE].sum()
        if FEATURE == 'transaction_id':
            data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('D')
            )[FEATURE].nunique()


    elif granularity == 'Weekly':
        if FEATURE == 'total_amount' or FEATURE == 'transaction_qty':
            data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('W')
            )[FEATURE].sum()
        if FEATURE == 'transaction_id':
            data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('W')
            )[FEATURE].nunique()

    elif granularity == 'Monthly':
        if FEATURE == 'total_amount' or FEATURE == 'transaction_qty':
            data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('M')
            )[FEATURE].sum()
        if FEATURE == 'transaction_id':
            data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('M')
            )[FEATURE].nunique()
    else:
        data = filtered_data.groupby(
                filtered_data['transaction_date'].dt.to_period('M')
            )[FEATURE].sum()

    graphs = st.columns([0.6, 0.4], gap='medium')

    with graphs[0]:
        st.plotly_chart(
            vis.bar_chart(data, granularity, FEATURE), #pylint: disable=used-before-assignment
            use_container_width=True
        )

    with graphs[1]:
        with st.container():
            st.plotly_chart(
                vis.line_chart(data, granularity, FEATURE),
                use_container_width=True
            )

        with st.container():
            st.plotly_chart(
                vis.growth_chart(data, granularity, FEATURE),
                use_container_width=True
            )

with tab[1]:
    st.header('Time of Day Analysis')

    # Radio button
    data_option = st.radio(
        'Select Data Type:',
        ['Sales', 'Transactions'],
        horizontal=True,
        key='Time_Analysis'
    )

    if data_option == 'Sales':

        # Average Sales by Weekday
        filtered_data['weekday'] = filtered_data['transaction_date'].dt.day_name()
        daywisesales = filtered_data.groupby(
            [filtered_data['transaction_date'].dt.date, 'weekday']
        )['total_amount'].sum().reset_index()
        average_daywisesales = daywisesales.groupby('weekday')['total_amount'].mean()
        weekday_order = list(calendar.day_name)
        average_daywisesales = average_daywisesales.reindex(weekday_order)

        # Average Sales by Hour of Day
        filtered_data['transaction_time'] = pd.to_datetime(
            filtered_data['transaction_time'],
            format='%H:%M:%S'
        ).dt.time
        filtered_data['transaction_hour'] = pd.to_datetime(
            filtered_data['transaction_time'],
            format='%H:%M:%S'
        ).dt.hour
        hourly_sales = filtered_data.groupby(
            [filtered_data['transaction_date'].dt.date, 'transaction_hour']
        )['total_amount'].sum().reset_index()
        average_hourly_sales = hourly_sales.groupby('transaction_hour')['total_amount'].mean()

    if data_option == 'Transactions':

        # Average Sales by Weekday
        filtered_data['weekday'] = filtered_data['transaction_date'].dt.day_name()
        daywisesales = filtered_data.groupby(
            [filtered_data['transaction_date'].dt.date,'weekday']
        ).size().reset_index(name='total_transactions')
        average_daywisesales = daywisesales.groupby('weekday')['total_transactions'].mean()
        weekday_order = list(calendar.day_name)
        average_daywisesales = average_daywisesales.reindex(weekday_order)

        # Average Sales by Hour of Day
        filtered_data['transaction_time'] = pd.to_datetime(
            filtered_data['transaction_time'], format='%H:%M:%S'
        ).dt.time
        filtered_data['transaction_hour'] = pd.to_datetime(
            filtered_data['transaction_time'], format='%H:%M:%S'
        ).dt.hour
        hourly_sales = filtered_data.groupby(
            [filtered_data['transaction_date'].dt.date, 'transaction_hour']
        ).size().reset_index(name='total_transactions')
        average_hourly_sales = hourly_sales.groupby('transaction_hour')['total_transactions'].mean()

    graphs = st.columns([0.5, 0.5], gap='medium')

    with graphs[0]:
        # Average Sales by Weekday
        st.plotly_chart(
            vis.avg_sales_by_week(average_daywisesales, data_option),
            use_container_width=True
        )

    with graphs[1]:
        # Average Sales by Hour of Day
        st.plotly_chart(
            vis.avg_sales_by_hourofday(average_hourly_sales, data_option), #pylint: disable=possibly-used-before-assignment
            use_container_width=True
        )

        # Average Sales by Hour of Day (Product category)
        st.plotly_chart(
            vis.avg_sales_by_hourofday_product(filtered_data, data_option),
            use_container_width=True
        )

with tab[2]:
    st.header('Top Products')

    # Radio Buttons
    data_option = st.radio(
        'Select Data Type:',
        ['Sales', 'Transactions'],
        horizontal=True,
        key='Top_Products'
    )

    if data_option == 'Sales':

        # Top Selling Product Category Distribution (Sales)
        category_distribution = filtered_data.groupby('product_category')['total_amount'].sum()

        # Product Type Sales Distribution
        grouped = filtered_data.groupby(['product_category', 'product_type'])['total_amount'].sum()

        # Top Selling Products
        top_products = filtered_data.groupby('product_type')['total_amount'].sum().sort_values(
            ascending=False
        ).head().reset_index(
            name='Total Sales'
        )

    elif data_option == 'Transactions':

        # Top Selling Product Category Distribution (Transactions)
        category_distribution = filtered_data.groupby('product_category').size()

        # Product Type Sales Distribution
        grouped = filtered_data.groupby(['product_category', 'product_type']).size()

        # Top Selling Products
        top_products = filtered_data.groupby('product_type')['transaction_qty'].sum().sort_values(
            ascending=False
        ).head().reset_index(
            name='Total Quantities Sold'
        )

    graphs = st.columns([0.6, 0.4], gap='medium')

    with graphs[0]:
        # Top Selling Product Category Distribution (Sales)
        st.plotly_chart(
            vis.top_selling_product(category_distribution) #pylint: disable=possibly-used-before-assignment
        )

    with graphs[1]:
        with st.container(height=295, border=False):
            st.write('Top-Selling Products')
            # Top-Selling Products
            st.dataframe(top_products, use_container_width=True) #pylint: disable=possibly-used-before-assignment

        with st.container(height=515, border=False):
            category = st.selectbox(
            label = 'Select Product Category',
            options = filtered_data.product_category.unique().tolist()
            )

            # Product Type Sales Distribution
            st.plotly_chart(vis.category_breakdown(grouped, category)) #pylint: disable=possibly-used-before-assignment

with tab[3]:
    st.header('Store Performance')

    button_column = st.columns(2)
    with button_column[0]:
        # Radio Button
        data_option = st.radio(
            'Select Data Type:',
            ['Sales', 'Transactions'],
            horizontal=True,
            key='Store_Performance'
        )

    with button_column[1]:
        # Radio Button
        granularity = st.radio(
            'Select Time Granularity:',
            ['Daily', 'Weekly', 'Monthly'],
            horizontal=True,
            index=2,
            key='Store_Performance_Granulartiy'
        )

    # KPIs
    store_performance = filtered_data2.groupby('store_location').agg({
    'total_amount': 'sum',
    'transaction_id': 'nunique',
    'transaction_qty': 'sum'
    })

    store_performance.reset_index(inplace=True)

    # Data preparation
    lm = filtered_data2[filtered_data2.store_location == 'Lower Manhattan']
    hk = filtered_data2[filtered_data2.store_location == "Hell's Kitchen"]
    astoria = filtered_data2[filtered_data2.store_location == "Astoria"]

    # KPIs
    lm_avg_ticket_size = lm['total_amount'].sum() / lm['transaction_id'].nunique()
    hk_avg_ticket_size = hk['total_amount'].sum() / hk['transaction_id'].nunique()
    astoria_avg_ticket_size = astoria['total_amount'].sum() / astoria['transaction_id'].nunique()

    # Granularity Adjustment
    if granularity == 'Daily':
        PERIOD = 'D'
    elif granularity == 'Weekly':
        PERIOD = 'W'
    elif granularity == 'Monthly':
        PERIOD = 'M'

    # Store Comparisions
    if data_option == 'Sales':
        lm_sales = lm.groupby(lm.transaction_date.dt.to_period(PERIOD))['total_amount'].sum() #pylint: disable=possibly-used-before-assignment
        hk_sales = hk.groupby(hk.transaction_date.dt.to_period(PERIOD))['total_amount'].sum()
        astoria_sales = astoria.groupby(
            astoria.transaction_date.dt.to_period(PERIOD)
        )['total_amount'].sum()

    elif data_option == 'Transactions':
        lm_sales = lm.groupby(lm.transaction_date.dt.to_period(PERIOD)).size()
        hk_sales = hk.groupby(hk.transaction_date.dt.to_period(PERIOD)).size()
        astoria_sales = astoria.groupby(astoria.transaction_date.dt.to_period(PERIOD)).size()

    # Growth Rates
    lm_weekly_growth = lm_sales.pct_change() * 100 #pylint: disable=possibly-used-before-assignment
    hk_weekly_growth = hk_sales.pct_change() * 100 #pylint: disable=possibly-used-before-assignment
    astoria_weekly_growth = astoria_sales.pct_change() * 100 #pylint: disable=possibly-used-before-assignment

    # Store Sales Distribution
    store_sales = [lm_sales.sum(), hk_sales.sum(), astoria_sales.sum()]
    store_labels = ['Lower Manhattan', "Hell's Kitchen", 'Astoria']

    graphs = st.columns([0.65, 0.45], gap='medium')

    with graphs[0]:
        kpi_columns = st.columns(3, gap='small')
        with st.container():
            with kpi_columns[0]:
                st.write('Astoria')
                st.metric(
                    label = 'Total Sales',
                    value = f'${int(store_performance['total_amount'].loc[
                        store_performance['store_location'] == 'Astoria'
                    ]):,.2f}',
                    border=True
                )

                st.metric(
                    label = 'Number of Transactions',
                    value = f'{int(store_performance['transaction_id'].loc[
                        store_performance['store_location'] == 'Astoria'
                    ]):,}',
                    border=True
                )

                st.metric(
                    label = 'Average Ticket Size',
                    value = f'{astoria_avg_ticket_size:.2f}',
                    border = True
                )

                st.metric(
                    label = 'Total Quantities Sold',
                    value = f'{int(store_performance['transaction_qty'].loc[
                        store_performance['store_location'] == 'Astoria'
                    ]):,}',
                    border = True
                )

        with st.container():
            with kpi_columns[1]:
                st.write("Hell's Kitchen")
                st.metric(
                    label = 'Total Sales',
                    value = f'${int(store_performance['total_amount'].loc[
                        store_performance['store_location'] == "Hell's Kitchen"
                    ]):,.2f}',
                    border=True
                )

                st.metric(
                    label = 'Number of Transactions',
                    value = f'{int(store_performance['transaction_id'].loc[
                        store_performance['store_location'] == "Hell's Kitchen"
                    ]):,}',
                    border=True
                )

                st.metric(
                    label = 'Average Ticket Size',
                    value = f'{hk_avg_ticket_size:.2f}',
                    border = True
                )

                st.metric(
                    label = 'Total Quantities Sold',
                    value = f'{int(store_performance['transaction_qty'].loc[
                        store_performance['store_location'] == "Hell's Kitchen"
                    ]):,}',
                    border = True
                )

        with st.container():
            with kpi_columns[2]:
                st.write("Lower Manhattan")
                st.metric(
                    label = 'Total Sales',
                    value = f'${int(store_performance['total_amount'].loc[
                        store_performance['store_location'] == "Lower Manhattan"
                    ]):,.2f}',
                    border=True
                )

                st.metric(
                    label = 'Number of Transactions',
                    value = f'{int(store_performance['transaction_id'].loc[
                        store_performance['store_location'] == "Lower Manhattan"
                    ]):,}',
                    border=True
                )

                st.metric(
                    label = 'Average Ticket Size',
                    value = f'{hk_avg_ticket_size:.2f}',
                    border = True
                )

                st.metric(
                    label = 'Total Quantities Sold',
                    value = f'{int(store_performance['transaction_qty'].loc[
                        store_performance['store_location'] == "Lower Manhattan"
                    ]):,}',
                    border = True
                )

        # Growth Rates by Store Location
        st.plotly_chart(
            vis.growth_rate(
                lm_weekly_growth,
                hk_weekly_growth,
                astoria_weekly_growth,
                data_option
            )
        )

    with graphs[1]:
        # Store Sales trend
        st.plotly_chart(
            vis.store_sales_trend(lm_sales, hk_sales, astoria_sales, data_option)
        )

        # Store Sales Distribution
        st.plotly_chart(
            vis.store_sale_distribution(store_sales, store_labels, data_option)
        )
