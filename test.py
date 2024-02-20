import time

import requests
from bs4 import BeautifulSoup

request_wait_time = 20

def send_get_query(url: str) -> BeautifulSoup:
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    ip = '31.44.188.89:9356'
    ip_login = 'M8FJxh'
    ip_password = '6B74yK'
    ip_with_auth = f'{ip_login}:{ip_password}@{ip}'
    query_proxy = {'http': f'http://{ip_with_auth}',
                   'https': f'http://{ip_with_auth}'}
    try:
        response = requests.get(url, headers=headers, timeout=request_wait_time, proxies=query_proxy)
        soup = BeautifulSoup(response.text, 'lxml')
    except Exception as ex:
        soup = 0
    return soup


def parse_caxap() -> dict:
    url = "https://xn--80aaa6bkfrbe5b.xn--p1ai/depilyatsiya/"
    soup = send_get_query(url)
    while soup == 0:
        time.sleep(request_wait_time)
        soup = send_get_query(url)
    price_list = soup.find('div', class_='service-detail__price-list').find('tbody').find_all('tr')

    service_price = dict()
    current_title = 0
    for service_row in price_list:
        if not isinstance(service_row.b, type(None)):
            current_title = service_row.b.text
            service_price[current_title] = dict()
        else:
            service = service_row.find_all('td')[0].text
            price = service_row.find_all('td')[1].text
            service_price[current_title][service] = price
    
    for k, v in service_price.items():
        print(f'{k}: {v}\n')
    
parse_caxap()

