from urllib.parse import urlparse


# All approved official sources are written in one place.
# Do not add unofficial websites here.

APPROVED_SOURCES = {
    "UKSSSC": {
        "name": "Official UKSSSC",
        "domain": "sssc.uk.gov.in",
        "start_url": "https://sssc.uk.gov.in/recruitment-notification/"
    },

    "Indian Railways": {
        "name": "Official Railway Recruitment",
        "domain": "rrb.indianrailways.gov.in",
        "start_url": "https://rrb.indianrailways.gov.in/"
    },

    "JEE": {
        "name": "Official JEE",
        "domain": "jeemain.nta.nic.in",
        "start_url": "https://jeemain.nta.nic.in/"
    },

    "NEET": {
        "name": "Official NEET",
        "domain": "neet.nta.nic.in",
        "start_url": "https://neet.nta.nic.in/"
    }
}


REQUEST_TIMEOUT = 12


def is_approved_url(url, source_name):
    """
    Checks whether a URL belongs to the correct approved official source.
    """

    try:
        parsed_url = urlparse(url)

        if parsed_url.scheme != "https":
            return False

        website_domain = parsed_url.netloc.lower().split(":")[0]

        approved_domain = APPROVED_SOURCES[source_name]["domain"]

        if website_domain == approved_domain:
            return True

        if website_domain.endswith("." + approved_domain):
            return True

        return False

    except Exception:
        return False
