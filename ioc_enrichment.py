import requests
from open_ai import format_enrichment_details_with_open_ai


def abuse_ipdb(extracted_iocs, abuse_ipdb_api_key, open_ai_api_key, open_ai_model):
    if extracted_iocs.get("ipv4"):
        final_response_json = []
        for ioc in extracted_iocs.get("ipv4"):
            default_error = f"""
                                <div class="info-section">
                                    <h2>Additional Enrichment Details</h2>
                                    <p>There was an Error while trying to enrich the IOC : {ioc} from AbuseIPDB.</p>
                                </div>
                            """
            try:
                headers = {
                    'Key': abuse_ipdb_api_key,
                    'Accept': 'application/json',
                }
                response = requests.get(f'https://api.abuseipdb.com/api/v2/check?ipAddress={ioc}&maxAgeInDays=90&verbose', headers=headers)
                if response.ok:
                    response_json = response.json()
                    response_json = format_enrichment_details_with_open_ai(ioc=ioc, content=response_json, api_key=open_ai_api_key, open_ai_model=open_ai_model)
                else:
                    response_json = default_error
            except:
                response_json = default_error

            final_response_json.append(response_json)

    else:
        final_response_json = "There are no IOCs to enrich from AbuseIPDB"

    return final_response_json


def hybrid_analysis(extracted_iocs, hybrid_analysis_api_key, open_ai_api_key, open_ai_model):

    if extracted_iocs.get("hashes").get("md5") or extracted_iocs.get("hashes").get("sha1") or extracted_iocs.get(
            "hashes").get("sha256"):
        all_enrichable_hashes = extracted_iocs.get("hashes").get("md5") + extracted_iocs.get("hashes").get(
            "sha1") + extracted_iocs.get("hashes").get("sha256")
        final_response_json = []
        for ioc in all_enrichable_hashes:
            default_error = f"""
                                <div class="info-section">
                                    <h2>Additional Enrichment Details</h2>
                                    <p>There was an Error while trying to enrich the IOC : {ioc} from Hybrid Analysis.</p>
                                </div>
                            """
            try:
                headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded',
                           'api-key': hybrid_analysis_api_key}
                data = {'hash': ioc}
                response = requests.post('https://www.hybrid-analysis.com/api/v2/search/hash', headers=headers,
                                         data=data)

                if response.ok:
                    response_json = response.json()
                    response_json = format_enrichment_details_with_open_ai(ioc=ioc, content=response_json, api_key=open_ai_api_key, open_ai_model=open_ai_model)
                else:
                    response_json = default_error
            except:
                response_json = default_error

            final_response_json.append(response_json)

    else:
        final_response_json = "There are no IOCs to enrich from Hybrid Analysis"

    return final_response_json
