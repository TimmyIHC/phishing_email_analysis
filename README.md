# Automated Phishing Email Analysis Report Script

## Introduction
The essence of this project is to implement an automated method for generating detailed phishing email analysis reports. This involves automatically fetching potentially suspicious emails from a Gmail mailbox and compiling a structured report for simpler analysis tasks.

## Operation
The script is designed to execute at two-minute intervals, searching for any unread emails within a specified mailbox. It looks specifically for emails attached as `.eml` files, analyzes these files, and then generates a comprehensive report. The report includes both extracted and enriched indicators of compromise (IoCs) found within the email content. This structured report is subsequently emailed to a designated recipient for further analysis.

## Pre-Process Conditions
In a typical security operations environment, there is usually a specific mailbox allocated for individuals to forward phishing emails they receive. These emails should be forwarded as `.eml` files. The script is tailored to specifically search for and process these files. 

## Pre-Requisites
To deploy this script, a basic understanding of managing Docker containers and running Python scripts is required. Though the following guide should suffice in setting up and running the system, possessing this foundational knowledge can be beneficial in troubleshooting potential issues.

## Credentials Required
- **Google OAuth2 Credentials**: Necessary for accessing emails from the Gmail mailbox intended for phishing email collection. Follow the steps outlined in [Google's guide](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid) to obtain these credentials. Ensure you download the credentials file and name it `credentials.json`.
- **AbuseIPDB API Credentials**: These can be acquired by creating a free account on the AbuseIPDB website and generating an API key.
- **Hybrid Analysis Credentials**: Similarly, create a free account on the Hybrid Analysis website and generate an API key.
- **OpenAI API Credentials**: Generate an API key via the [OpenAI Playground](https://platform.openai.com/playground).

## Setup Steps
1. Fork the repository to your local environment.
2. Open the `config.json` file and fill in all necessary details.
3. Replace the existing `credentials.json` file with your own.
4. Install all the requirements listed in the `requirements.txt` file. It is advisable to use a temporary environment interpreter for this step.
5. Execute the `get_token.py` file. This will prompt you for consent to read, modify, and send emails using your credentials. Once consent is given, a `token.json` file will be generated in the same directory, mirroring the `token_sample.json` file.
6. Transfer all forked files, along with the newly created `token.json`, to the server where you intend to run this script. Ensure all files are placed within the same directory.
7. If not already installed, ensure Docker is set up on your server following the instructions provided [here](https://docs.docker.com/engine/install/ubuntu/).
8. Build and run the Docker container using the following commands:
    ```
    docker build -t phishing_email_traiging .
    docker run -it --name phishing_analysis_container phishing_email_traiging bash
    ```
9. Within the container, initiate the script execution with the following command:
    ```
    python3 main.py
    ```
10. Allow the script to complete a few cycles. Once satisfied, you can detach from the container using the keystroke combination: `ctrl+p` followed by `ctrl+q`.

This setup will facilitate the automated analysis and reporting of phishing emails, making it easier for security operations teams to identify and respond to potential threats.