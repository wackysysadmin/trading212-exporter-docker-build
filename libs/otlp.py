import libs.trading212
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter
)
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


def otlp_provider(otlp_endpoint):
    exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
    reader = PeriodicExportingMetricReader(exporter)
    provider = MeterProvider(
        resource=Resource(
            attributes={SERVICE_NAME: "trading212-exporter"}
        ),
        metric_readers=[reader]
    )
    set_meter_provider(provider)
    return get_meter_provider().get_meter("trading212")


def check_value(v):
    return isinstance(v, int) or isinstance(v, float)


def set_gauge(gauge, metrics, extra_labels={}):
    for k, v in metrics.items():
        if check_value(v):
            gauge.set(v, {"data": k, **extra_labels})


def set_cash_gauge(api_key, gauge):
    metrics = libs.trading212.get_cash(api_key)
    set_gauge(gauge, metrics)


def set_portfolio_gauge(api_key, gauge):
    tickers = libs.trading212.get_portfolio(api_key)
    for ticker in tickers:
        set_gauge(gauge, ticker, {"ticker": ticker['ticker']})


def set_metrics(api_key, otlp_endpoint):
    meter = otlp_provider(otlp_endpoint)
    cash_gauge = meter.create_gauge("trading212_cash")
    portfolio_gauge = meter.create_gauge("trading212_portfolio")
    set_cash_gauge(api_key, cash_gauge)
    set_portfolio_gauge(api_key, portfolio_gauge)
