# This is a simple code that acts a sensor that transmits data every N seconds.
# Inputs (as environment variables) of the program:
# - DATASET_PATH:   Path at which this programs grabs data and sends
# - SLEEP_TIME:     Specifies the time interval between each transmission
# - TARGET_URL:     Specifies the server url to which the requests are sent to
# TODO: Add the request method as an input (GET, POST, PUT, ...)
# Author: Navid Alipour

import requests
import json
import os
from time import time
from random import randint
import threading

dataset_path = os.environ['DATASET_PATH']
sleep_time = float(os.environ['SLEEP_TIME'])
target_url = os.environ['TARGET_URL']

# Number of requests sent in second
throughput = 0

# Base time 
start_time = time() 

def update_throughput():
    global throughput
    global start_time

    throughput = throughput + 1
    time_diff = (time() - start_time) * 1000
    
    # Update the start_time every 1s
    if (time_diff > 1000):
        start_time = time()
        data = {}
        data["throughput"] = throughput
        print(json.dumps(data))
        throughput = 0


# Reads all the lines from a given file and returns them
def read_data(path):
    f = open(path, 'r')
    return f.readlines()


# Selects random data entry from the given dataset
def get_random_datapoint(dataset):
    x = randint(0, len(dataset) - 1)
    return json.loads(dataset[x])


# Sends a request to the url containing the a random record of the dataset as the payload
def send_request(url, payload, method='POST'):
    res = requests.post(url, data=payload)
    return res


# This is were the emulation happens:
# 1- Reads all the data records from the dataset_path
# 2- Selects a random data record
# 3- Sends an HTTP request to the given server URL
# 4- Sets up another thread to do it all over again
def run_task():
    dataset = read_data(dataset_path)

    random_data = get_random_datapoint(dataset)
    x = send_request(target_url, random_data)
    
    update_throughput()

    threading.Timer(sleep_time, run_task).start()


def main():
   run_task() 
    

main()
