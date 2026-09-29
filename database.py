import sqlite3
from pathlib import Path


DATABASE_FILE = Path("data/exams.db")


def create_database():
    """
    Creates the SQLite database and table if they do not exist.
    """

    DATABASE_FILE.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS official_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_name TEXT,
            organization TEXT,
            source_name TEXT,
            source_url TEXT,
            notification_url TEXT,
            last_checked TEXT,
            retrieval_status TEXT
        )
    """)

    connection.commit()

    connection.close()


def save_result(result):
    """
    Saves only official result information.

    Student personal information is not stored.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO official_results (
            exam_name,
            organization,
            source_name,
            source_url,
            notification_url,
            last_checked,
            retrieval_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        result["name"],
        result["organization"],
        result["source_name"],
        result["source_url"],
        result["notification_url"],
        result["last_checked"],
        result["status"]
    ))

    connection.commit()

    connection.close()
