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
from time import strftime
from time import localtime
from random import randint
import threading
import logging

dataset_path = os.environ['DATASET_PATH']
sleep_time = float(os.environ['SLEEP_TIME'])
target_url = os.environ['TARGET_URL']

# Number of requests sent in second
number_of_reqs = 0
total_rtt = 0

# Base time 
start_time = time() 

def update_metrics(req_rtt, experiment_mode=False):
    global number_of_reqs 
    global start_time
    global total_rtt
    global sleep_time
    step = 0.01
    timer_lower_bound = 0.01


    number_of_reqs = number_of_reqs + 1
    time_diff = (time() - start_time) * 1000
    total_rtt = total_rtt + req_rtt
    
    # Update the start_time every 1s
    if (time_diff > 1000):
        start_time = time()
        data = {}

        if (experiment_mode == True):
            sleep_time = sleep_time - step

        data["number_of_reqs"] = number_of_reqs 
        data["time"] = strftime("%H: %M: %S", localtime()) 
        data["avg_rtt"] = total_rtt / number_of_reqs
        data["interval"] = sleep_time

        print(json.dumps(data))
        if (("MODE" in os.environ) and (os.environ["MODE"] in ["DEBUG", "INFO"])):
            logging.info(json.dumps(data))

        number_of_reqs = 0
        total_rtt = 0


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
def run_task(experiment_mode=False):
    dataset = read_data(dataset_path)
    random_data = get_random_datapoint(dataset)
    x = send_request(target_url, random_data)
    timer_lower_bound = 0.01

    update_metrics(x.elapsed.total_seconds(), experiment_mode)
    if (experiment_mode is False):
        threading.Timer(sleep_time, run_task).start()
    else:
        if (sleep_time > timer_lower_bound):
            threading.Timer(sleep_time, run_task, [True]).start()
        else:
            threading.Timer(timer_lower_bound, run_task, [True]).start()


def main():
    hostname = os.environ["HOSTNAME"]

    if (("MODE" in os.environ) and (os.environ["MODE"] in ["DEBUG", "INFO"])):
        log_dir = "/var/log"
        if ("LOG_PATH" in os.environ):
            log_dir = os.environ["LOG_PATH"]
        logging.basicConfig(filename="{}/{}.log".format(log_dir, hostname), level=logging.INFO)
        

    run_task(experiment_mode=False) 
    

main()
