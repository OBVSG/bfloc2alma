import os
from xml.etree import ElementTree as ET

NS = {
    "bf": "http://id.loc.gov/ontologies/bibframe/",
    "bflc": "http://id.loc.gov/ontologies/bflc/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "madsrdf": "http://www.loc.gov/mads/rdf/v1#",
    "dcterms": "http://purl.org/dc/terms/",
    "lclocal": "http://id.loc.gov/ontologies/lclocal/",
}

# register all namespaces for nicer output (no ns1, ns2, ... prefixes)
for prfx, uri in NS.items():
    ET.register_namespace(prfx, uri)

API_KEY = os.environ.get("API_KEY_PSB") or "put-your-key-here-if-you-absolutely-must"
BASE_URL = "https://api-eu.hosted.exlibrisgroup.com/almaws/v1"
bib_api = BASE_URL + "/bibs/{mms_id}"

ALMA_SESSION_HEADERS = {
    "accept": "application/xml",
    "content-type": "application/xml",
    "validate": "false",
    "authorization": f"apikey {API_KEY}"
}
