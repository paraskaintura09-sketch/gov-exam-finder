import streamlit as st
from datetime import date

from database import create_database, save_result
from utils import calculate_age
from eligibility import evaluate_student

from sources.uksssc import fetch_uksssc_data
from sources.railways import fetch_railway_data
from sources.jee import fetch_jee_data
from sources.neet import fetch_neet_data


# ------------------------------------------------
# STREAMLIT PAGE SETTINGS
# ------------------------------------------------

st.set_page_config(
    page_title="Gov & Exam Finder",
    page_icon="🎓",
    layout="wide"
)

create_database()


# ------------------------------------------------
# SIMPLE CSS FOR POLISHED DESIGN
# ------------------------------------------------

st.markdown("""
<style>

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}

.hero-box {
    background: linear-gradient(120deg, #083344, #155e75);
    color: white;
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 20px;
}

.result-card {
    border: 1px solid #cbd5e1;
    border-left: 6px solid #0891b2;
    background-color: #f8fafc;
    padding: 18px;
    border-radius: 12px;
    margin-top: 12px;
    margin-bottom: 12px;
}

.small-text {
    color: #475569;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------
# TITLE
# ------------------------------------------------

st.markdown("""
<div class="hero-box">
    <h1>GOV & EXAM FINDER</h1>
    <p>
        Find examinations and government recruitment opportunities
        you may be eligible for.
    </p>
</div>
""", unsafe_allow_html=True)

st.info(
    "Official notifications and official websites are the final authority. "
    "Verify the latest information before applying."
)


# ------------------------------------------------
# STUDENT FORM
# ------------------------------------------------

with st.form("student_form"):

    st.subheader("Enter Your Academic Information")

    left_column, right_column = st.columns(2)

    with left_column:

        user_dob = st.date_input(
            "Date of Birth",
            value=None,
            min_value=date(1950, 1, 1),
            max_value=date.today()
        )

        user_qualification = st.selectbox(
            "Highest Educational Qualification",
            [
                "Select",
                "Class 10",
                "Class 12",
                "ITI",
                "Diploma",
                "Graduation",
                "Post Graduation"
            ]
        )

        class_10_status = st.selectbox(
            "Class 10 Status",
            [
                "Select",
                "Passed",
                "Appearing",
                "Not Passed"
            ]
        )

        class_12_status = st.selectbox(
            "Class 12 Status",
            [
                "Select",
                "Passed",
                "Appearing",
                "Not Passed",
                "Not Applicable"
            ]
        )

    with right_column:

        user_stream = st.selectbox(
            "Stream",
            [
                "Select",
                "PCM",
                "PCB",
                "PCMB",
                "Science",
                "Commerce",
                "Arts/Humanities",
                "Other"
            ]
        )

        user_subjects = st.multiselect(
            "Subjects Studied",
            [
                "Physics",
                "Chemistry",
                "Mathematics",
                "Biology/Biotechnology",
                "English",
                "Computer Science",
                "Other"
            ]
        )

        user_state = st.selectbox(
            "State / UT",
            [
                "Select",
                "Uttarakhand",
                "Other State / UT"
            ]
        )

        user_category = st.selectbox(
            "Category (only used if an official rule requires it)",
            [
                "Select / Prefer not to say",
                "General",
                "OBC",
                "SC",
                "ST",
                "EWS",
                "Other"
            ]
        )

        graduation_status = st.selectbox(
            "Graduation Qualification / Status",
            [
                "Not Applicable",
                "Graduated",
                "Appearing",
                "Not Graduated"
            ]
        )

    submit_button = st.form_submit_button(
        "Check Official Opportunities",
        use_container_width=True
    )


# ------------------------------------------------
# FORM PROCESSING
# ------------------------------------------------

if submit_button:

    if user_dob is None:
        st.error("Please enter your date of birth.")

    elif user_dob > date.today():
        st.error("Date of birth cannot be in the future.")

    elif user_qualification == "Select":
        st.error("Please select your highest qualification.")

    elif class_10_status == "Select":
        st.error("Please select your Class 10 status.")

    elif class_12_status == "Select":
        st.error("Please select your Class 12 status.")

    elif user_stream == "Select":
        st.error("Please select your stream.")

    elif user_state == "Select":
        st.error("Please select your State / UT.")

    else:

        user_age = calculate_age(user_dob)

        profile = {
            "age": user_age,
            "qualification": user_qualification,
            "class_10_status": class_10_status,
            "class_12_status": class_12_status,
            "stream": user_stream,
            "subjects": user_subjects,
            "state": user_state,
            "category": user_category,
            "graduation_status": graduation_status
        }

        with st.spinner("Checking approved official sources only..."):

            retrieved_data = {
                "UKSSSC": fetch_uksssc_data(),
                "Indian Railways": fetch_railway_data(),
                "JEE": fetch_jee_data(),
                "NEET": fetch_neet_data()
            }

            results = evaluate_student(profile, retrieved_data)

            for result in results:
                save_result(result)

            st.session_state["results"] = results

        st.success(
            "Official-source check completed. "
            "Your personal form details were not stored permanently."
        )


# ------------------------------------------------
# RESULT DISPLAY
# ------------------------------------------------

if "results" in st.session_state:

    results = st.session_state["results"]

    st.header("Your Results")

    filter_column_1, filter_column_2 = st.columns(2)

    with filter_column_1:

        status_filter = st.selectbox(
            "Filter by Status",
            [
                "All",
                "ELIGIBLE",
                "POTENTIALLY ELIGIBLE",
                "NOT ELIGIBLE",
                "INFORMATION UNAVAILABLE"
            ]
        )

    with filter_column_2:

        source_filter = st.selectbox(
            "Filter by Source",
            [
                "All",
                "UKSSSC",
                "Indian Railways",
                "JEE",
                "NEET"
            ]
        )

    search_text = st.text_input(
        "Search Retrieved Results",
        placeholder="Search exam name, source, or official notice..."
    ).lower()

    result_groups = [
        "Government Recruitment",
        "Entrance Examinations"
    ]

    for group_name in result_groups:

        st.subheader(group_name)

        results_shown = 0

        for result in results:

            search_data = (
                result["name"]
                + " "
                + result["source_key"]
                + " "
                + result["notice_title"]
                + " "
                + result["reason"]
            ).lower()

            if result["organization"] != group_name:
                continue

            if status_filter != "All":
                if result["status"] != status_filter:
                    continue

            if source_filter != "All":
                if result["source_key"] != source_filter:
                    continue

            if search_text != "":
                if search_text not in search_data:
                    continue

            results_shown += 1

            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            st.markdown("### " + result["name"])

            if result["status"] == "ELIGIBLE":
                st.success("Status: " + result["status"])

            elif result["status"] == "POTENTIALLY ELIGIBLE":
                st.info("Status: " + result["status"])

            elif result["status"] == "NOT ELIGIBLE":
                st.error("Status: " + result["status"])

            else:
                st.warning("Status: " + result["status"])

            st.write(
                "**Your calculated age:** "
                + str(result["user_age"])
                + " years"
            )

            st.write("**Reason:** " + result["reason"])

            st.write(
                "**Age requirement:** "
                + result["age_requirement"]
            )

            st.write(
                "**Qualification requirement:** "
                + result["qualification_requirement"]
            )

            st.write(
                "**Subject requirement:** "
                + result["subject_requirement"]
            )

            st.write(
                "**Important dates:** "
                + result["important_dates"]
            )

            st.write(
                "**Retrieved official item:** "
                + result["notice_title"]
            )

            st.write(
                "**Source:** "
                + result["source_name"]
            )

            st.link_button(
                "Open Official Source / Notification",
                result["notification_url"]
            )

            st.markdown(
                '<p class="small-text">Last checked: '
                + result["last_checked"]
                + '</p>',
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

        if results_shown == 0:
            st.caption("No results match the selected filters.")
