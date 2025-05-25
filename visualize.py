import plotly.graph_objs as go

def plot_stock(df, ticker):
    fig = go.Figure()
    x = df['Date'] if 'Date' in df.columns else df.index

    fig.add_trace(go.Scatter(x=x, y=df['Close'], name='Close'))
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

def plot_forecast(df, forecast, conf_int, ticker):
    import pandas as pd
    # Prepare forecast dates
    last_date = pd.to_datetime(df['Date'].iloc[-1]) if 'Date' in df.columns else pd.to_datetime(df.index[-1])
    forecast_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=len(forecast), freq='B')

    fig = go.Figure()
    # Plot historical close
    x = df['Date'] if 'Date' in df.columns else df.index
    fig.add_trace(go.Scatter(x=x, y=df['Close'], name='Close'))
    # Plot forecast
    fig.add_trace(go.Scatter(x=forecast_dates, y=forecast, name='Forecast', line=dict(color='green', dash='dash')))
    # Plot confidence interval
    fig.add_trace(go.Scatter(
        x=forecast_dates, y=conf_int.iloc[:, 0], fill=None, mode='lines', line=dict(color='lightgreen'), name='Lower CI'
    ))
    fig.add_trace(go.Scatter(
        x=forecast_dates, y=conf_int.iloc[:, 1], fill='tonexty', mode='lines', line=dict(color='lightgreen'), name='Upper CI'
    ))

    fig.update_layout(
        title=f"{ticker} Forecasted Close Prices with Confidence Interval",
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price'),
        height=600
    )
    fig.show()
