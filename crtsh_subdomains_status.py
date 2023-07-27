import requests
import json
import re
from requests.exceptions import RequestException, ConnectTimeout

class crtshAPI(object):
    """crtshAPI main handler."""

    def search(self, domain, wildcard=True, expired=True):
        """
        Search crt.sh for the given domain.

        domain -- Domain to search for
        wildcard -- Whether or not to prepend a wildcard to the domain
                    (default: True)
        expired -- Whether or not to include expired certificates
                    (default: True)

        Return a list of objects, like so:

        {
            "issuer_ca_id": 16418,
            "issuer_name": "C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3",
            "name_value": "hatch.uber.com",
            "min_cert_id": 325717795,
            "min_entry_timestamp": "2018-02-08T16:47:39.089",
            "not_before": "2018-02-08T15:47:39"
        }
        """
        base_url = "https://crt.sh/?q={}&output=json"
        if not expired:
            base_url = base_url + "&exclude=expired"
        if wildcard and "%" not in domain:
            domain = "%.{}".format(domain)
        url = base_url.format(domain)

        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
        req = requests.get(url, headers={'User-Agent': ua})

        if req.ok:
            try:
                content = req.content.decode('utf-8')
                data = json.loads(content)
                return [entry["name_value"] for entry in data]  # Extracting only the "name_value" field
            except ValueError:
                # crt.sh fixed their JSON response. This shouldn't be necessary anymore
                # https://github.com/crtsh/certwatch_db/commit/f4f46ea37c23543c4cdf1a3c8867d68967641807
                data = json.loads("[{}]".format(content.replace('}{', '},{')))
                return [entry["name_value"] for entry in data]
            except Exception as err:
                print("Error retrieving information.")
        return None

if __name__ == "__main__":
    # Create an instance of the crtshAPI class
    crtsh_api = crtshAPI()

    # Specify the domain for which you want to retrieve subdomains
    domain_to_search = "dazn.com"

    # Call the search method to retrieve subdomain information
    result = crtsh_api.search(domain_to_search)

    # Combine all the entries into a single string
    combined_entries = '\n'.join(result)

    # Extract domain names using regular expression
    domain_names = re.findall(r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', combined_entries)

    # Convert the list to a set to remove duplicates, and then back to a list
    unique_domain_names = list(set(domain_names))

    # Check the status codes of the unique domain names and print the results
    print("Domain Name\t\tHTTP Status Code\t\tHTTPS Status Code")
    print("-------------------------------------------------------------")
    for domain_name in unique_domain_names:
        domain_name = domain_name.lstrip('.')
        try:
            # Try HTTP first
            http_response = requests.get(f"http://{domain_name}", timeout=5)
            http_status_code = http_response.status_code
            http_status = f"{http_status_code}" if http_response.ok else f"{http_status_code} (Request Failed)"

            # Try HTTPS next
            https_response = requests.get(f"https://{domain_name}", timeout=5)
            https_status_code = https_response.status_code
            https_status = f"{https_status_code}" if https_response.ok else f"{https_status_code} (Request Failed)"

            print(f"{domain_name}\t\t{http_status}\t\t{https_status}")
        except RequestException as e:
            # Skip domains that are not reachable or encounter other request exceptions
            pass

