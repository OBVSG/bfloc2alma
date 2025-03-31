#!/usr/bin/env python3

import argparse
from sys import exit

import requests

from config import *
from lib import *

parser = argparse.ArgumentParser()
parser.add_argument("loc_ids",
                    nargs="+",
                    help="The LoC-IDs to be imported into Alma")
parser.add_argument("-c",
                    "--cleanup",
                    help="Delete created records afterwards",
                    action="store_true")

args = parser.parse_args()

session = requests.Session()
session.headers.update(ALMA_SESSION_HEADERS)

# get the records from loc
loc_bf = []
for loc_id in args.loc_ids:
    print(f"Getting bf work from loc: {loc_id}")
    bf_work = get_bibframe_from_loc(loc_id, "work")
    loc_bf.append(bf_work)
    print(f"Getting bf instance from loc: {loc_id}")
    bf_instance = get_bibframe_from_loc(loc_id, "instance")
    loc_bf.append(bf_instance)

# lists for the MMS-IDs for later use
mmsids = []

## prepare the XML and import it into alma

for bf in loc_bf:
    post_res = session.post(bib_api.format(mms_id=""),
                 prep_rec(bf))

    # blow up if HTTP error
    try:
        post_res.raise_for_status()
    except Exception as error:
        print(post_res.text)
        continue

    mms = get_mmsid(post_res)
    mmsids.append(mms)
    entity = "work" if mms.startswith("97") else "instance"
    print(f"Imported {entity}: {mms}")

if args.cleanup:
    # iterate over reversed list, so to delete the instances first
    mmsids.reverse()
    for mmsid in mmsids:
        print(f"deleting {mmsid}")
        del_res = session.delete(bib_api.format(mms_id=mmsid))
        print(f"   {del_res.status_code}")
