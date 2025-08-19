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

# def line_chart(data, granularity, feature):
#     fig = go.Figure(
#         data=[
#             go.Scatter(
#                 x=data.index.astype(str),
#                 y=data.values,
#                 mode='lines+markers'
#             )
#         ]
#     )
    
#     fig.update_layout(
#         title_text = f'{granularity} Transactions',
#         xaxis_title = f'{granularity}',
#         yaxis_title = yaxis_title,
#         template = 'plotly_dark'
#     )
    
#     return fig

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
        height = 350
    )
    
    return fig