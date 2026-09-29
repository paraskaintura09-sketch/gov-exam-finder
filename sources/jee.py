from config import APPROVED_SOURCES
from utils import get_official_notices


def fetch_jee_data():
    """
    Retrieves links only from the official JEE source.
    """

    source = APPROVED_SOURCES["JEE"]

    notices, error_message, checked_time = get_official_notices(
        "JEE",
        source["start_url"],
        [
            "jee",
            "main",
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
