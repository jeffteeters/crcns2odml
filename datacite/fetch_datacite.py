import json
import os
import requests

import datacite


# Adjust as required
OUTPUT_DIR = os.path.join(os.sep, "tmp", "datacite")
DATACITE_API_ENDPOINT = "https://api.datacite.org/dois"
DATACITE_QUERY = "?query=publisher:CRCNS.org&page[size]=200"


def fetch_datacite():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    datacite_uri = "%s%s" % (DATACITE_API_ENDPOINT, DATACITE_QUERY)

    print("... running DataCite query")
    req = requests.get(datacite_uri)
    req_json = json.loads(req.text.encode("utf-8"))

    datacite_items = req_json["data"]
    print("... query returned %s data-sets" % len(datacite_items))

    # DataCite interaction client without authorization;
    # used to fetch DataCite XML metadata for specific DOIs
    dclient = datacite.DataCiteMDSClient()

    for datacite_item in datacite_items:
        curr_doi = datacite_item['attributes']['doi']
        curr_filename = "%s.xml" % curr_doi.split("/")[1]
        curr_file_path = os.path.join(OUTPUT_DIR, curr_filename)

        print("... fetching DataCite file '%s'" % curr_filename)
        curr_xml = dclient.metadata_get(curr_doi)
        with open(curr_file_path, "w+") as curr_file:
            curr_file.write(curr_xml)


if __name__ == "__main__":
    fetch_datacite()

