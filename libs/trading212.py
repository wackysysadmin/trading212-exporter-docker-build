import requests


def get_http(api_key, url):
    headers = {"Authorization": api_key}
    response = requests.get(url, headers=headers)
    return response.json()


def get_portfolio(api_key):
    return get_http(
        api_key,
        "https://live.trading212.com/api/v0/equity/portfolio"
    )


def get_cash(api_key):
    return get_http(
        api_key,
        "https://live.trading212.com/api/v0/equity/account/cash"
    )
