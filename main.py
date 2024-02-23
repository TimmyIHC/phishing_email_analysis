import json
import sys
from ioc_enrichment import abuse_ipdb, hybrid_analysis
from fetch_emails import get_unread_emails, gmail_authenticate, mark_email_as_read
from open_ai import create_a_report
from ioc_extraction import extract_iocs
from send_emails import send_email


# Main program

def main():
    try:

        print("\033[2;32m_________________________________________________________________________________\033[0;0m")
        print("\033[2;32m_________________________________________________________________________________\033[0;0m")
        print("\033[2;35m PROGRAM EXECUTION COMMENCED \033[0;0m")

        with open("config.json", 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        abuse_ipdb_api_key = data.get("abuse_ipdb_api_key")
        open_ai_api_key = data.get("open_ai_api_key")
        hybrid_analysis_api_key = data.get("hybrid_analysis_api_key")
        email_recipients = data.get("email_recipients")
        open_ai_model = data.get("open_ai_model")

        service = gmail_authenticate()
        print("\033[34m - Authentication Successful \033[0;0m")
        unread_emails_info = get_unread_emails(service)
        if not unread_emails_info:
            print("\033[34m - No Emails Found\033[0;0m")
            sys.exit()
        unread_emails_info = unread_emails_info[0]
        print("\033[34m - Unread Email Fetched \033[0;0m")

        extracted_iocs = extract_iocs(data=unread_emails_info)
        unread_emails_info.update({"extracted_iocs": extracted_iocs})
        print("\033[34m - IOCs Extracted \033[0;0m")

        abuse_ipdb_enrichment = abuse_ipdb(extracted_iocs=unread_emails_info.get("extracted_iocs"),
                                           abuse_ipdb_api_key=abuse_ipdb_api_key,
                                           open_ai_api_key=open_ai_api_key, open_ai_model=open_ai_model)

        hybrid_analysis_enrichment = hybrid_analysis(extracted_iocs=unread_emails_info.get("extracted_iocs"),
                                                     hybrid_analysis_api_key=hybrid_analysis_api_key,
                                                     open_ai_api_key=abuse_ipdb_api_key, open_ai_model=open_ai_model)

        print("\033[34m - Enrichment Completed \033[0;0m")

        report = create_a_report(content=unread_emails_info,
                                 api_key=open_ai_api_key, open_ai_model=open_ai_model)

        report = report.replace("</body>", "")
        report = report.replace("</html>", "")

        if isinstance(abuse_ipdb_enrichment, list):
            for details in abuse_ipdb_enrichment:
                report += details

        report += "<br>"

        if isinstance(hybrid_analysis_enrichment, list):
            for details in hybrid_analysis_enrichment:
                report += details

        report += "</body></html>"

        print("\033[34m - Report Created \033[0;0m")

        send_email(subject="Phishing Email Report", message_text=report, to=email_recipients)
        service = gmail_authenticate()
        mark_email_as_read(service=service, msg_id=unread_emails_info["message_id"])

        print("\033[34m - Email Marked as Read \033[0;0m")

        print("\033[34m - Email Report sent successfully\033[0;0m")

        print("\033[2;32m_________________________________________________________________________________\033[0;0m")
        print("\033[2;32m_________________________________________________________________________________\033[0;0m")
    except:
        print("Error Occured")
        print("\033[2;32m_________________________________________________________________________________\033[0;0m")
        print("\033[2;32m_________________________________________________________________________________\033[0;0m")


import time

if __name__ == "__main__":
    while True:
        main()
        # Wait for 120 seconds (2 minutes) before the next execution
        time.sleep(120)