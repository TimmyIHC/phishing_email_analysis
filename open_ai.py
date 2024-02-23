import requests
import os
import json


def create_a_report(content, api_key, open_ai_model):
    try:
        content = str(content)
        content = content[:12000]
        directive = """
        As a professional Cyber Security Analyst, your task is to conduct a thorough analysis of a Phishing email, focusing specifically on the aspects outlined below, without altering the structure, make the narrative very cyber security and professional.: 
        Make sure to add MITRE TTPs where possible
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Phishing Email Analysis Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            font-size: 16px;
            background-color: #f4f7f6;
            color: #333;
        }
        h1, h2, h3 {
            color: #005a87;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #bbcde5;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #e1eff6;
            color: #005a87;
        }
        td {
            background-color: #FFFFFF;
        }
        .info-section {
            background-color: #ffffff;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            padding: 20px;
            border-left: 4px solid #005a87;
        }
    </style>
</head>
<body>
    <h1>Phishing Email Analysis Report</h1>
    <div class="info-section">
        <h2>Email Header Analysis</h2>
        <table>
            <tr>
                <th>Header</th>
                <th>Value</th>
                <th>Description</th>
            </tr>
            <tr>
                <td>Received</td>
                <td>_____VALUE_HERE_____</td>
                <td>Tracks the email path through servers/computers.</td>
            </tr>
            <tr>
                <td>From</td>
                <td>_____VALUE_HERE_____</td>
                <td>Sender's email address (can be spoofed).</td>
            </tr>
            <tr>
                <td>Subject</td>
                <td>_____VALUE_HERE_____</td>
                <td>Crafted to lure the recipient into taking action.</td>
            </tr>
            <tr>
                <td>To</td>
                <td>_____VALUE_HERE_____</td>
                <td>Shows the recipient of the email.</td>
            </tr>
            <tr>
                <td>Date</td>
                <td>_____VALUE_HERE_____</td>
                <td>When the email was sent.</td>
            </tr>
            <tr>
                <td>Message-ID</td>
                <td>_____VALUE_HERE_____</td>
                <td>Unique identifier for the email.</td>
            </tr>
            <tr>
                <td>Content-Type</td>
                <td>_____VALUE_HERE_____</td>
                <td>MIME type and character set of email content.</td>
            </tr>
        </table>
    </div>
    <div class="info-section">
        <h2>Additional Technical Details</h2>
        <p>_____VALUE_HERE_____</p>
    </div>
    <div class="info-section">
        <h2>Content and Phishing Indicators</h2>
        <table>
            <tr>
                <th>Indicator</th>
                <th>Value/Description</th>
            </tr>
            <tr>
                <td>Links/URLs</td>
                <td>_____VALUE_HERE_____</td>
            </tr>
            <tr>
                <td>Phishing Techniques</td>
                <td>_____VALUE_HERE_____</td>
            </tr>
            <tr>
                <td>IP Addresses and URLs</td>
                <td>_____VALUE_HERE_____</td>
            </tr>
        </table>
    </div>
    <div class="info-section">
        <h2>Analysis Summary</h2>
        <p></p>
    </div>
</body>
</html>
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.getenv('OPENAI_API_KEY', api_key),
        }

        json_data = {
            'model': open_ai_model,
            'messages': [
                {
                    'role': 'system',
                    'content': directive,
                },
                {
                    'role': 'user',
                    'content': content,
                },
            ],
        }

        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
        json_response = response.json()
        if response.ok:
            response_content = json_response.get("choices")[0].get("message").get("content")
        else:
            response_content = ("Dear Administrator,<br><br> There seems to be an error with generating the report, "
                                "and as a result, only the raw JSON structure of the phishing email has been provided"
                                " below : <br><br>") + str(content)
    except:
        response_content = ("Dear Administrator,<br><br> There seems to be an error with generating the report, "
                            "and as a result, only the raw JSON structure of the phishing email has been provided "
                            "below : <br><br>") + str(content)
    return response_content


def format_enrichment_details_with_open_ai(ioc, content, api_key, open_ai_model):
    default_error_response = """
    <div class="info-section">
        <h2>Additional Enriched information (AbuseIPDB , Hybrid Analysis)</h2>
            <caption>Indicator Name : ___VALUE___</caption>
            <caption>Error Generating Human Readable Report for IOC : {ioc}<caption>
            <p>The raw JSON structure of the enrichment detail has been provided below : <br><br>{JSON_RESPONSE}</p>
    </div>
        """
    try:
        string_content = str(content)
        ioc = f""" Make sure the below generated content is the content is in HTML format. Enrichment Details for the IOC : {ioc}\n"""
        string_content = ioc + string_content
        string_content = string_content[:12000]

        directive = """
Your primary objective involves a careful review and structuring of the supplied enhancement data, focusing primarily on elements that are critical to a Security Analyst conducting an in-depth analysis of the Indicators of Compromise (IOC).

Begin by providing an overview of the aggregated data.

Please format the content in the below HTML format. 
<div class="info-section">
        <h2>Additional Enriched information (AbuseIPDB , Hybrid Analysis)</h2>
        <caption>Indicator Name : ___VALUE___</caption>
        <table>
            <tr>
                <th>Parameters</th>
                <th>Description</th>
            </tr>
            <tr>
                <td>_____PARAMETER_HERE_____</td>
                <td>_____VALUE_HERE_____</td>
            </tr>
            <tr>
                <td>_____PARAMETER_HERE_____</td>
                <td>_____VALUE_HERE_____</td>
            </tr>
            <tr>
                <td>_____PARAMETER_HERE_____</td>
                <td>_____VALUE_HERE_____</td>
            </tr>
        </table>
    </div>
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.getenv('OPENAI_API_KEY', api_key),
        }

        json_data = {
            'model': open_ai_model,
            'messages': [
                {
                    'role': 'system',
                    'content': directive,
                },
                {
                    'role': 'user',
                    'content': string_content,
                },
            ],
        }

        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
        json_response = response.json()
        if response.ok:
            response_content = json_response.get("choices")[0].get("message").get("content")
        else:
            JSON_RESPONSE = pretty_print_dict(d=content)
            print(JSON_RESPONSE)
            default_error_response = default_error_response.format(ioc=ioc, JSON_RESPONSE=JSON_RESPONSE)
            print(default_error_response)
            response_content = default_error_response
    except:
        JSON_RESPONSE = pretty_print_dict(d=content)
        print(JSON_RESPONSE)
        default_error_response = default_error_response.format(ioc=ioc, JSON_RESPONSE=JSON_RESPONSE)
        print(default_error_response)
        response_content = default_error_response

    return response_content


def pretty_print_dict(d, indent=0):
    """
    Converts a dictionary into a pretty string format with indentation.

    Parameters:
    d (dict): The input dictionary.
    indent (int): The current indentation level.

    Returns:
    str: A pretty-printed string representation of the dictionary.
    """
    items = []
    # Iterate over key-value pairs
    for k, v in d.items():
        # Prepare the key
        if isinstance(k, str):
            key = f"'{k}'"
        else:
            key = repr(k)

        # Prepare the value
        if isinstance(v, dict):
            value = pretty_print_dict(v, indent + 4)  # Recursively format dictionaries
        elif isinstance(v, str):
            value = f"'{v}'"
        else:
            value = repr(v)

        # Add the formatted item (key: value) with indentation
        items.append((' ' * indent) + f"{key}: {value},")

    # Join all items, adding opening and closing brackets with proper indentation
    return "{\n" + "\n".join(items) + "\n" + (' ' * indent) + "}"
