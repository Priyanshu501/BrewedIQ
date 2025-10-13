import plotly.graph_objects as go


def bar_chart(data, granularity, feature):
    ''' Displays Sales Trends over Time '''
    fig = go.Figure(
        data=[
            go.Bar(
                x=data.index.start_time.astype(str),
                y=data.values,
                text=data.values,
                textposition='auto'
            )
        ]
    )

    if feature == 'total_amount':
        yaxis_title = 'Total Sales Amount'
    elif feature == 'transaction_id':
        yaxis_title = 'Number of Transactions'
    elif feature == 'transaction_qty':
        yaxis_title = 'Total Quantity Sold'
    
    fig.update_layout(
        title_text = f'{yaxis_title}: {granularity}',
        xaxis_title = f'{granularity}',
        yaxis_title = yaxis_title,
        template = 'plotly_dark' ,
        height = 700
    )

    return fig

def line_chart(data, granularity, feature):
    ''' Displays Moving Average '''
    if granularity == 'Daily':
        window = 7
        frequency = 'Days'
    if granularity == 'Weekly':
        window = 4
        frequency = 'Weeks'
    if granularity == 'Monthly':
        window = 2
        frequency = 'Months'
    
    moving_average = data.rolling(window=window).mean()
    
    if feature == 'total_amount':
        yaxis_title = 'Total Sales Amount'
    elif feature == 'transaction_id':
        yaxis_title = 'Number of Transactions'
    elif feature == 'transaction_qty':
        yaxis_title = 'Total Quantity Sold'
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x = data.index.start_time.astype(str),
            y = data.values,
            mode='lines',
            name='Actual Data'
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x = moving_average.index.start_time.astype(str),
            y = moving_average.values,
            mode='lines',
            name=f'{window}-{frequency} Moving Average'
        )
    )
    
    fig.update_layout(
        title_text = f'Growth of {yaxis_title} Over {window}-{frequency}',
        xaxis_title = f'{granularity}',
        yaxis_title = f'{yaxis_title}',
        template = 'plotly_dark',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        height = 350
    )
    
    return fig

def growth_chart(data, granularity, feature):
    growth = data.pct_change() * 100
    growth = growth.round(2)
    
    if granularity == 'Daily':
        frequency = 'Day'
    if granularity == 'Weekly':
        frequency = 'Week'
    if granularity == 'Monthly':
        frequency = 'Month'
    
    fig = go.Figure(
        data=[
            go.Bar(
                x=growth.index.start_time.astype(str),
                y=growth.values,
                text=growth.values,
                textposition='auto'
            )
        ]
    )
    
    if feature == 'total_amount':
        yaxis_title = 'Total Sales Amount'
    elif feature == 'transaction_id':
        yaxis_title = 'Number of Transactions'
    elif feature == 'transaction_qty':
        yaxis_title = 'Total Quantity Sold'
    
    fig.update_layout(
        title_text = f'Growth Rate of {yaxis_title} per {frequency}',
        xaxis_title = f'{granularity}',
        yaxis_title = f'{yaxis_title}',        
        height = 350
    )
    
    return fig

def avg_sales_by_week(data, feature):
    
    if feature == 'Sales':
        graph_title = 'Average Sales by Weekday',
        graph_yaxis = 'Revenue ($)'
    elif feature == 'Transactions':
        graph_title = 'Average Number of Transaction by Weekday',
        graph_yaxis = 'No. of Transactions'
    
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data.values
        )
    )

    fig.update_layout(
        title=str(graph_title[0]),
        xaxis_title='Weekday',
        yaxis_title=graph_yaxis,
        height=700
    )    
    
    return fig

def avg_sales_by_hourofday(data, feature):
    if feature == 'Sales':
        graph_title = 'Average Sales by Hour of Day'
        graph_yaxis = 'Average Sales'
    elif feature == 'Transactions':
        graph_title = 'Average Transactions by Hour of Day'
        graph_yaxis = 'Number of Transactions'  
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data.values,
            mode='lines+markers',
            fill = 'tozeroy',
            fillcolor='rgba(0, 176, 246, 0.2)'
        )
    )

    fig.update_layout(
        title=str(graph_title),
        xaxis_title='Hour of Day',
        yaxis_title=graph_yaxis,
        height=300
    )
    
    return fig

def avg_sales_by_hourofday_product(data, feature):
    fig = go.Figure()
    
    if feature == 'Sales':
        graph_title = 'Average Sales by Hour of Day (Product Category)'
        graph_yaxis = 'Revenue ($)'
        for category in data['product_category'].unique():
            cat_df = data[data['product_category'] == category]
            hourly_sales = cat_df.groupby([cat_df['transaction_date'].dt.date, 'transaction_hour'])['total_amount'].sum().reset_index()
            average_hourly_sales = hourly_sales.groupby('transaction_hour')['total_amount'].mean()
            fig.add_trace(
                go.Scatter(
                    x=average_hourly_sales.index,
                    y=average_hourly_sales.values,
                    mode='lines',
                    name=category
                )
            )
    
    elif feature == 'Transactions':
        graph_title = 'Average Number of Transactions by Hour of Day (Product Category)'
        graph_yaxis = 'Number of Transactions'
        for category in data['product_category'].unique():
            cat_df = data[data['product_category'] == category]
            hourly_transactions = cat_df.groupby([cat_df['transaction_date'].dt.date, 'transaction_hour']).size().reset_index(name='total_transactions')
            average_hourly_transactions = hourly_transactions.groupby('transaction_hour')['total_transactions'].mean()
            fig.add_trace(
                go.Scatter(
                    x=average_hourly_transactions.index,
                    y=average_hourly_transactions.values,
                    mode='lines',
                    name=category
                )
            )
        
    fig.update_layout(
        title=graph_title,
        xaxis_title='Hour of Day',
        yaxis_title=graph_yaxis,
        showlegend=True,
        # legend=dict(
        #     x=0.5,
        #     y=-0.7,
        #     orientation='h',
        #     xanchor='center',
        #     yanchor='bottom'
        # ),
        height=400
    )
    return fig

def top_selling_product(data):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=data.index.astype(str),
            y=data.values
        )
    )
    fig.update_layout(
        title='Product Category Distribution',
        xaxis_title='Product Category',
        yaxis_title='Total Sales',
        height=800
    )
    return fig

def category_breakdown(data, category):
    
    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            values=data[category].values,
            labels=data[category].index.astype(str).tolist(),
            textinfo='percent+label',
            hole=0.3
        )
    )

    fig.update_layout(
        title="Product Type Sales Distribution",
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="center",
        x=0.5
        ),
        height=400
    )

    return fig

def store_sales_trend(store1_sale, store2_sale, store3_sale, feature):
    if feature == 'Sales':
        graph_title = 'Store Sales Comparion (Revenue)'
        graph_yaxis = 'Total Sales'
    elif feature == 'Transactions':
        graph_title = 'Store Sales Comparion (Transactions)'
        graph_yaxis = 'Total Transactions'
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=store1_sale.index.start_time.astype(str),
            y=store1_sale.values,
            mode='lines',
            name='Lower Manhattan'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=store2_sale.index.start_time.astype(str),
            y=store2_sale.values,
            mode='lines',
            name="Hell's Kitchen"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=store3_sale.index.start_time.astype(str),
            y=store3_sale.values,
            mode='lines',
            name='Astoria'
        )
    )

    fig.update_layout(
        title=graph_title,
        xaxis_title='Week',
        yaxis_title=graph_yaxis,
        legend=dict(
            x=0.5,
            y=1.1,
            orientation='h',
            xanchor='center'
        ),
        height=475
    )
    
    return fig

def store_sale_distribution(sale_data, label, feature):
    if feature == 'Sales':
        graph_title = 'Store Sales Distribution (Revenue)'
    elif feature == 'Transactions':
        graph_title = 'Store Sales Distribution (Transactions)'

    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels=label,
            values=sale_data,
            hole=0.3,
            textinfo='percent+label'        
        )
    )

    fig.update_layout(
        title=graph_title,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=475
    )

    return fig

def growth_rate(store1_growth, store2_growth, store3_growth, feature):
    
    if feature == 'Sales':
        graph_title = 'Weekly Growth Rates by Store Location (Revenue)'
    elif feature == 'Transactions':
        graph_title = 'Weekly Growth Rates by Store Location (Number of Transactions)'
    
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=store1_growth.index.start_time.astype(str),
            y=store1_growth.values,
            name="Lower Manhattan"
        )
    )

    fig.add_trace(
        go.Bar(
            x=store2_growth.index.start_time.astype(str),
            y=store2_growth.values,
            name="Hell's Kitchen"
        )
    )

    fig.add_trace(
        go.Bar(
            x=store3_growth.index.start_time.astype(str),
            y=store3_growth.values,
            name="Astoria"
        )
    )

    fig.update_layout(
        title=graph_title,
        xaxis_title="Week",
        yaxis_title="Growth Rate (%)",
        barmode="group",
        legend=dict(
            title="Store Location",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )

    return fig   