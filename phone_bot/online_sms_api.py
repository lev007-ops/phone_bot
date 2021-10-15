import requests
import json
from config import CONFIG
API = CONFIG['api']

def get_numbers(c):
    res = requests.get(f'https://online-sms.org/api/getnumbers?country={c.upper()}&apikey={API}')
    return res.json()

def get_countries():
    res = requests.get(f'https://online-sms.org/api/getnumbers?&apikey={API}')
    return res.json()