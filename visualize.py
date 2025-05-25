import plotly.graph_objs as go

def plot_stock(df, ticker):
    fig = go.Figure()

    # Use the 'Date' column for x-axis if it exists
    x = df['Date'] if 'Date' in df.columns else df.index

    fig.add_trace(go.Scatter(x=x, y=df['Close'], name='Closing'))
    if 'SMA_20' in df.columns:
        fig.add_trace(go.Scatter(x=x, y=df['SMA_20'], name='SMA 20'))

    if 'RSI' in df.columns:
        fig.add_trace(go.Scatter(
            x=x, y=df['RSI'], name='RSI',
            yaxis='y2', line=dict(color='orange', dash='dot')
        ))

    fig.update_layout(
        title=f"{ticker} Price, SMA 20, and RSI",
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price'),
        yaxis2=dict(
            title='RSI',
            overlaying='y',
            side='right',
            range=[0, 100],
            showgrid=False
        ),
        height=600
    )
    fig.show()
