# Use the official Python image as a base image
FROM python:3.10

WORKDIR /app

COPY . /app

# Install required packages
RUN pip install --trusted-host pypi.python.org -r requirements.txt


RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

COPY . .

EXPOSE 5000

CMD ["python3", "app.py"]