from config import APPROVED_SOURCES, is_approved_url


UNAVAILABLE_MESSAGE = (
    "Information unavailable from the approved official source."
)


def make_result(
    name,
    organization,
    source_key,
    checked_time,
    notice,
    error_message,
    user_age
):
    """
    Creates one result for the website.

    This project does not create fake eligibility conditions.
    It only shows verified information from an approved official source.
    """

    source = APPROVED_SOURCES[source_key]

    notification_url = source["start_url"]

    notice_title = "Not available from official source."

    if notice is not None:
        if is_approved_url(notice["url"], source_key):
            notification_url = notice["url"]

            notice_title = notice["title"]

    if error_message is not None:

        reason = (
            "Official information could not be retrieved automatically. "
            + error_message
        )

    elif notice is not None:

        reason = (
            "An official notice or link was retrieved. However, complete "
            "verified eligibility requirements could not be safely extracted "
            "as structured data. Open the official notice and verify before applying."
        )

    else:

        reason = UNAVAILABLE_MESSAGE

    result = {
        "name": name,
        "organization": organization,
        "source_key": source_key,
        "source_name": source["name"],
        "source_url": source["start_url"],
        "notification_url": notification_url,
        "notice_title": notice_title,

        "status": "INFORMATION UNAVAILABLE",

        "reason": reason,

        "age_requirement": "Not available from official source.",

        "qualification_requirement": (
            "Not available from official source."
        ),

        "subject_requirement": (
            "Not available from official source."
        ),

        "important_dates": (
            "Not available from official source."
        ),

        "last_checked": checked_time,

        "user_age": user_age
    }

    return result


def evaluate_student(profile, retrieved_data):
    """
    Creates results for all four approved sources.
    """

    results = []

    source_details = [
        {
            "key": "UKSSSC",
            "name": "UKSSSC Opportunities",
            "organization": "Government Recruitment"
        },

        {
            "key": "Indian Railways",
            "name": "Indian Railways / RRB Opportunities",
            "organization": "Government Recruitment"
        },

        {
            "key": "JEE",
            "name": "JEE",
            "organization": "Entrance Examinations"
        },

        {
            "key": "NEET",
            "name": "NEET",
            "organization": "Entrance Examinations"
        }
    ]

    for item in source_details:

        source_key = item["key"]

        source_data = retrieved_data[source_key]

        first_notice = None

        if len(source_data["notices"]) > 0:
            first_notice = source_data["notices"][0]

        result = make_result(
            item["name"],
            item["organization"],
            source_key,
            source_data["checked_time"],
            first_notice,
            source_data["error_message"],
            profile["age"]
        )

        results.append(result)

    return results
