import requests
from bs4 import BeautifulSoup

def get_cve_score(cve_id):
    url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    cvss_link = soup.find("a", id="Cvss2CalculatorAnchor")
    cvss_score = cvss_link.text.strip().split()[0]
    return cvss_score

# Example usage:
cve_id = "CVE-2012-3411"
cvss_score = get_cve_score(cve_id)
print(f"CVSS Score for {cve_id}: {cvss_score}")
