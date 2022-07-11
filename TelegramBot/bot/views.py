import requests
from typing import NamedTuple


def import_contact(data: NamedTuple) -> None:
    url = 'https://s1-nova.ru/app/private_test_python/'
    requests.post(
        url,
        json={'phone': data.phone, 'login': data.login},
        headers={'Content-Type': 'application/json'}
    )
