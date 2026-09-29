from config import APPROVED_SOURCES
from utils import get_official_notices


def fetch_railway_data():
    """
    Retrieves links only from the official Railway Recruitment Board source.
    """

    source = APPROVED_SOURCES["Indian Railways"]

    notices, error_message, checked_time = get_official_notices(
        "Indian Railways",
        source["start_url"],
        [
            "recruitment",
            "notification",
            "application",
            "cen",
            "railway"
        ]
    )

    return {
        "notices": notices,
        "error_message": error_message,
        "checked_time": checked_time
    }
