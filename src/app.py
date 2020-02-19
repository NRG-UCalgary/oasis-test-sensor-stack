import requests
import json
import os
import time
from random import randint

dataset_path = os.environ['DATASET_PATH']
sleep_time = int(os.environ['SLEEP_TIME'])
target_url = os.environ['TARGET_URL']

def read_data(path):
    f = open(path, 'r')
    return f.readlines()


def get_random_datapoint(dataset):
    x = randint(0, len(dataset))
    return json.loads(dataset[x])


def send_request(url, payload, method='POST'):
    res = requests.post(url, data=payload)
    return res


def main():
    dataset = read_data(dataset_path)

    while True:
        time.sleep(sleep_time)
        random_data = get_random_datapoint(dataset)
        x = send_request(target_url, random_data)
        print(x)

main()
