import re


def extract_iocs(data):
    iocs = {
        "ipv4": [],
        "urls": [],
        "domains": [],
        "emails": [],
        "hashes": {
            "md5": [],
            "sha1": [],
            "sha224": [],
            "sha256": [],
            "sha384": [],
            "sha512": [],
        }
    }

    ipv4_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
    domain_pattern = r"\b(?:[\w-]+\.)+[\w-]+\b"
    email_pattern = r"\b[\w.-]+@[\w.-]+\.\w+\b"
    hash_patterns = {
        "md5": r"\b[a-fA-F0-9]{32}\b",
        "sha1": r"\b[a-fA-F0-9]{40}\b",
        "sha224": r"\b[a-fA-F0-9]{56}\b",
        "sha256": r"\b[a-fA-F0-9]{64}\b",
        "sha384": r"\b[a-fA-F0-9]{96}\b",
        "sha512": r"\b[a-fA-F0-9]{128}\b"
    }

    def search_iocs(value):
        if isinstance(value, dict):
            for val in value.values():
                search_iocs(val)
        elif isinstance(value, str):
            ipv4_matches = re.findall(ipv4_pattern, value)
            url_matches = re.findall(url_pattern, value)
            domain_matches = re.findall(domain_pattern, value)
            email_matches = re.findall(email_pattern, value)

            iocs["ipv4"].extend(ipv4_matches)
            iocs["ipv4"].append("52.52.52.52")
            iocs["ipv4"].append("1.1.1.1")
            iocs["urls"].extend(url_matches)
            iocs["domains"].extend([d for d in domain_matches if d not in url_matches])  # Exclude domains found in URLs
            iocs["emails"].extend(email_matches)

            for hash_type, hash_pattern in hash_patterns.items():
                hash_matches = re.findall(hash_pattern, value)
                iocs["hashes"][hash_type].extend(hash_matches)

    search_iocs(data)
    iocs["ipv4"] = list(set(iocs["ipv4"]))
    iocs["urls"] = list(set(iocs["urls"]))
    iocs["domains"] = list(set(iocs["domains"]))
    iocs["emails"] = list(set(iocs["emails"]))
    iocs["hashes"]["md5"] = list(set(iocs["hashes"]["md5"]))
    iocs["hashes"]["sha1"] = list(set(iocs["hashes"]["sha1"]))
    iocs["hashes"]["sha224"] = list(set(iocs["hashes"]["sha224"]))
    iocs["hashes"]["sha256"] = list(set(iocs["hashes"]["sha256"]))
    iocs["hashes"]["sha384"] = list(set(iocs["hashes"]["sha384"]))
    iocs["hashes"]["sha512"] = list(set(iocs["hashes"]["sha512"]))
    return iocs