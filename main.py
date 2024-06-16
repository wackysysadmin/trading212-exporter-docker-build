#!/usr/bin/env python3

import click
import libs.http
import libs.otlp


@click.command()
@click.option(
    '--api-key',
    envvar='TRADING212_API_KEY',
    required=True,
    help='Trading212 API Key'
)
@click.option(
    '--metrics-type',
    envvar='METRICS_TYPE',
    default="prometheus",
    type=click.Choice(
        ['prometheus', 'otlp'],
        case_sensitive=True
    ),
    help='Use a prometheus HTTP server or post to an OTLP endpoint'
)
@click.option(
    '--otlp-endpoint',
    envvar='OTLP_ENDPOINT',
    default="http://localhost:4317/v1/metrics",
    help='OTLP Endpoint'
)
@click.option(
    '--prometheus-host',
    envvar='PROMETHEUS_HOST',
    default="0.0.0.0",
    help='Which IP do you want the Prometheus exporter to listen on'
)
@click.option(
    '--prometheus-port',
    envvar='PROMETHEUS_PORT',
    default=5001,
    help='Which port do you want the Prometheus exporter to listen on'
)
def cli(api_key, metrics_type, otlp_endpoint, prometheus_host, prometheus_port):  # noqa: E501
    if metrics_type == "prometheus":
        libs.http.run(api_key, prometheus_host, prometheus_port)
    else:
        libs.otlp.set_metrics(api_key, otlp_endpoint)


if __name__ == '__main__':
    cli()
