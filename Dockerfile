# Use the latest Ubuntu image as the base
FROM ubuntu:latest

# Set environment variables to make Python installation silent
ENV DEBIAN_FRONTEND=noninteractive

# Update apt repository and install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip cron

# Set the working directory in the container
WORKDIR /app

# Copy the phishing_email_analysis directory to the working directory in the container
COPY main.py .
COPY fetch_emails.py .
COPY ioc_enrichment.py .
COPY ioc_extraction.py .
COPY open_ai.py .
COPY send_emails.py .
COPY config.json .
COPY requirements.txt .
COPY token.json .


# Install the Python dependencies from requirements.txt
RUN pip3 install -r requirements.txt
