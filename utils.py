from datetime import date, datetime
from urllib.parse import urljoin

import requests
import re

from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT, is_approved_url


HEADERS = {
    "User-Agent": "GovExamFinderSchoolProject/1.0"
}


def calculate_age(user_dob, cutoff_date=None):
    """
    Calculates age properly.

    It does not simply subtract birth year.
    It checks if the birthday has happened this year.
    """

    if user_dob is None:
        return None

    if cutoff_date is None:
        cutoff_date = date.today()

    age = cutoff_date.year - user_dob.year

    birthday_not_happened = (
        cutoff_date.month,
        cutoff_date.day
    ) < (
        user_dob.month,
        user_dob.day
    )

    if birthday_not_happened:
        age = age - 1

    return age


def clean_text(text):
    """
    Removes extra spaces and new lines from text.
    """

    return re.sub(r"s+", " ", text).strip()


def get_official_page(url, source_name):
    """
    Downloads one official webpage.

    It rejects unsafe URLs and rejects redirects
    to websites outside the approved source domain.
    """

    if not is_approved_url(url, source_name):
        return None, "Unauthorized URL rejected."

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True
        )

        if not is_approved_url(response.url, source_name):
            return None, "Redirected to an unauthorized URL. Request rejected."

        if response.status_code != 200:
            return None, "Official source returned HTTP " + str(response.status_code)

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if "text/html" not in content_type:
            return None, "Official page is not readable HTML."

        return response.text, None

    except requests.exceptions.Timeout:
        return None, "Official source timed out."

    except requests.exceptions.RequestException:
        return None, "Official source could not be reached."

    except Exception:
        return None, "Unknown error while retrieving official source."


def get_official_notices(source_name, start_url, keywords):
    """
    Finds relevant links only on the approved official website.

    It does not use Google, blogs, social media,
    coaching sites, or third-party websites.
    """

    checked_time = datetime.now().strftime(
        "%d %b %Y, %I:%M %p"
    )

    html, error_message = get_official_page(
        start_url,
        source_name
    )

    if error_message is not None:
        return [], error_message, checked_time

    try:
        soup = BeautifulSoup(html, "html.parser")

        notices = []
        saved_urls = []

        for link_tag in soup.find_all("a", href=True):
            title = clean_text(
                link_tag.get_text(" ")
            )

            full_url = urljoin(
                start_url,
                link_tag["href"]
            )

            combined_text = (
                title + " " + full_url
            ).lower()

            keyword_found = False

            for keyword in keywords:
                if keyword.lower() in combined_text:
                    keyword_found = True

            if keyword_found:
                if is_approved_url(full_url, source_name):
                    if full_url not in saved_urls:

                        saved_urls.append(full_url)

                        notices.append({
                            "title": title if title else "Official notice or link",
                            "url": full_url
                        })

            if len(notices) >= 8:
                break

        return notices, None, checked_time

    except Exception:
        return [], "Official page could not be parsed.", checked_time
