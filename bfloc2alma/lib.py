import os
from xml.etree import ElementTree as ET

import requests

# our configuration
# from bfloc2alma.config import NS

# get BIBFRAME from LoC
def get_bibframe_from_loc(loc_id, entity="work", compact=True, as_tree=False, session=None):
    """Get a BIBFRAME work from LoC. Return the xml of the record.

    entity: "work" or "instance"
    If compact: get compact format.
    If as_tree: return the XML as ElementTree
    """
    url = f"https://id.loc.gov/resources/{entity}s/{loc_id}{'.bibframe' if compact else ''}.rdf"

    # use session if available
    if session:
        response = session.get(url)
    else:
        response = requests.get(url)

    response.raise_for_status()

    if as_tree:
        return ET.fromstring(response.text)
    else:
        return response.text

# prep BIBFRAME record for Alma
def prep_rec(bf_rec):
    """Wrap BIBFRAME to be posted to Almas API.

    <bib>
      <record_format>lcbf_work</record_format>
      <record>
        [BIBFRAME HERE ...]
      </record>
    </bib>
    """
    NS = {"bf": "http://id.loc.gov/ontologies/bibframe/"}
    # bf_rec needs to be an ET.Element to be handled further
    if type(bf_rec) == str:
        bf_rec = ET.fromstring(bf_rec)
    elif type(bf_rec) != ET.Element:
        raise Error("bf_rec must be str or ET.Element!")

    # check which entity we have
    if bf_rec.find('bf:Work', NS) is not None:
        entity = "work"
    elif bf_rec.find('bf:Instance', NS) is not None:
        entity = "instance"
    else:
        raise Exception("Input is neither a work nor an instance!")

    # create XML tree
    bib = ET.Element('bib')
    record_format = ET.Element('record_format')
    record_format.text = f"lcbf_{entity}"
    bib.append(record_format)
    record = ET.Element("record")
    record.append(bf_rec)
    bib.append(record)

    return ET.tostring(bib)

def get_mmsid(response):
    """Get the MMS ID from an Alma API response."""
    response_tree = ET.fromstring(response.text)
    mms = response_tree.find('mms_id')
    return mms.text
