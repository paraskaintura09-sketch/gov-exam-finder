from config import APPROVED_SOURCES
from utils import get_official_notices


def fetch_uksssc_data():
    """
    Retrieves links only from the official UKSSSC source.
    """

    source = APPROVED_SOURCES["UKSSSC"]

    notices, error_message, checked_time = get_official_notices(
        "UKSSSC",
        source["start_url"],
        [
            "recruitment",
            "notification",
            "advertisement",
            "group",
            "vacancy"
        ]
    )

    return {
        "notices": notices,
        "error_message": error_message,
        "checked_time": checked_time
    }
