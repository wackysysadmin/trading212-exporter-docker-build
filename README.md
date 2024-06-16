# trading212-exporter

This repo allows people to run a simple webapp to publish metrics which can be scraped by [Prometheus](https://prometheus.io/) and then displayed through [Grafana](https://grafana.com/). There is also support for sending metrics to an OpenTelemetry endpoint.

## Prerequisites

1. Trading212 API Key [https://helpcentre.trading212.com/hc/en-us/articles/14584770928157-How-can-I-generate-an-API-key](https://helpcentre.trading212.com/hc/en-us/articles/14584770928157-How-can-I-generate-an-API-key)
2. [Docker](https://www.docker.com/)
3. An instance of Grafana & Prometheus. Here are some options for running your own:
  * [On a Raspberry Pi](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/)
  * [AWS Prometheus](https://aws.amazon.com/prometheus/). Be careful to stay within the free tier limits.
  * [Grafana Cloud](https://grafana.com/products/cloud/). Only has 14 days free retention.

## How to Run

1. Create an env file for credentials `cp .env.example .env`
2. Add API credentials to `.env`
3. Run with Docker:
```
docker run -p 5001:5001 --restart always -d --env-file .env --name trading212-exporter trading212-exporter
```

### Configuring Prometheus

Add the following to your Prometheus config file:

```
scrape_configs:
  - job_name: trading212-exporter
    scrape_interval: 30s
    static_configs:
    - targets:
      - your-host:5001
```

### Send metrics to OpenTelemetry

It's possible to send metrics to OpenTelemetry using the following:

```
pip install -r requirements.txt

./main.py --api-key foo --metrics-type otlp --otlp-endpoint http://bar:4317/v1/metrics

# Or with Environment Variables
export TRADING212_API_KEY="foo"
export METRICS_TYPE="otlp"
export OTLP_ENDPOINT="http://bar:4317/v1/metrics"
./main.py
```

### Running locally

The `docker-compose.yaml` in this repo will run an instance of Grafana, Prometheus, Alloy and the trading212-exporter.

After setting up your `.env` you only need to run the following:

```
docker-compose run -P grafana
```

You will then be able to see your metrics at [http://localhost:3000/dashboards](http://localhost:3000/dashboards)
