# Note: Environment Variable "TARGET_URL" should be set before launching the container!

FROM python:3.7

# Install requests
RUN pip3 install requests

# Copy the humidity dataset into `/dataset/` directory
COPY ./dataset/hum.txt /dataset/hum.txt # Note: Change according to the desired dataset
COPY ./src/http/sensor-app.py /app.py

# Set some environment variables
ENV SENSOR_TYPE="Humidity"              # Note: Change according to the desired dataset
ENV DATASET_PATH="/dataset/hum.txt"     # Note: Change according to the desired dataset
ENV SLEEP_TIME=0.01                     # Time interval between each data transmission

# These env-variables are needed to make sure 
# that the throughput of the program is shown 
# in `docker logs` command!
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONUNBUFFERED=1

CMD ["python3", "/app.py"]
