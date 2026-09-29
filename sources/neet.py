from config import APPROVED_SOURCES
from utils import get_official_notices


def fetch_neet_data():
    """
    Retrieves links only from the official NEET source.
    """

    source = APPROVED_SOURCES["NEET"]

    notices, error_message, checked_time = get_official_notices(
        "NEET",
        source["start_url"],
        [
            "neet",
            "ug",
            "notification",
            "application",
            "registration",
            "admission",
            "exam"
        ]
    )

    return {
        "notices": notices,
        "error_message": error_message,
        "checked_time": checked_time
    }
