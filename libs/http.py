from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from flask import Flask, Response, current_app
import libs.prometheus

app = Flask(__name__)

cash_gauge = libs.prometheus.cash_gauge()
portfolio_gauge = libs.prometheus.portfolio_gauge()

@app.route("/metrics")
def metrics():
    api_key = current_app.config['API_KEY']
    libs.prometheus.set_cash_gauge(api_key, cash_gauge)
    libs.prometheus.set_portfolio_gauge(api_key, portfolio_gauge)
    # Use the older "text/plain; version=0.0.4" content type:
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

def run(api_key, prometheus_host, prometheus_port):
    app.config['API_KEY'] = api_key
    app.run(debug=False, port=prometheus_port, host=prometheus_host)
