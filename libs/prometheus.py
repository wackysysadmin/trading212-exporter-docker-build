from prometheus_client import Gauge
import libs.trading212


def check_value(v):
    return isinstance(v, int) or isinstance(v, float)


def set_gauge(gauge, metrics, extra_labels={}):
    for k, v in metrics.items():
        if check_value(v):
            gauge.labels(data=k, **extra_labels).set(v)


def set_cash_gauge(api_key, gauge):
    metrics = libs.trading212.get_cash(api_key)
    set_gauge(gauge, metrics)


def set_portfolio_gauge(api_key, gauge):
    tickers = libs.trading212.get_portfolio(api_key)
    for ticker in tickers:
        set_gauge(gauge, ticker, {"ticker": ticker['ticker']})


def cash_gauge():
    return Gauge(
        'trading212_cash',
        'Trading 212 Cash',
        labelnames=['data']
    )


def portfolio_gauge():
    return Gauge(
        'trading212_portfolio',
        'Trading 212 Portfolio',
        labelnames=['ticker', 'data']
    )
