import requests

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

def calculate_factorial(integer):
    accum = 1
    for i in range(integer, 0, -1):
        accum *= i
    return accum
