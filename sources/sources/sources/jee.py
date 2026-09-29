from config import APPROVED_SOURCES
from utils import get_official_notices


def fetch_jee_data():
    """
    Retrieves links only from the official JEE Main NTA source.
    """

    source = APPROVED_SOURCES["JEE"]

    notices, error_message, checked_time = get_official_notices(
        "JEE",
        source["start_url"],
        [
            "jee",
            "notification",
            "information bulletin",
            "application",
            "admission"
        ]
    )

    return {
        "notices": notices,
        "error_message": error_message,
        "checked_time": checked_time
    }
