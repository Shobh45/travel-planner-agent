import json
from datetime import date

import requests
import streamlit as st

DEFAULT_BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="TravelPlannerAgent Frontend",
    page_icon="✈️",
    layout="centered",
)

st.title("TravelPlannerAgent")
st.write("Use this interface to submit travel planning requests and retrieve the generated itinerary report.")

backend_url = st.sidebar.text_input("Backend URL", DEFAULT_BACKEND_URL)

with st.form("travel_request_form"):
    st.subheader("Trip Details")

    origin = st.text_input("Origin city", value="Indore")
    destination = st.text_input("Destination city", value="Delhi")
    start_date = st.date_input("Start date", value=date.today())
    end_date = st.date_input("End date", value=date.today())
    trip_type = st.selectbox("Trip type", ["Solo", "Couple", "Family", "Group"])
    mode_of_transport = st.selectbox("Mode of transport", ["Flight", "Train", "Bus", "Car"])
    budget_total = st.number_input("Total budget", value=20000.0, min_value=0.0, step=100.0)
    budget_currency = st.text_input("Budget currency", value="INR")
    num_travelers = st.number_input("Number of travelers", min_value=1, value=2, step=1)

    submit_button = st.form_submit_button("Plan trip")

if submit_button:
    request_payload = {
        "origin": origin,
        "destination": destination,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "trip_type": trip_type,
        "mode_of_transport": mode_of_transport,
        "budget_total": budget_total,
        "budget_currency": budget_currency,
        "num_travelers": int(num_travelers),
    }

    st.info("Sending request to backend...")

    try:
        response = requests.post(
            f"{backend_url.rstrip('/')}/plan",
            json=request_payload,
            timeout=180,
        )
        response.raise_for_status()
        data = response.json()

        st.success("Travel plan request completed.")
        st.write("### Response")
        st.json(data)

        if data.get("report_file"):
            try:
                report_response = requests.get(
                    f"{backend_url.rstrip('/')}/report",
                    timeout=60,
                )
                report_response.raise_for_status()
                report_data = report_response.json()

                report_text = report_data.get("report", "")
                st.success("Report generated successfully.")

                with st.expander("View full report", expanded=True):
                    st.markdown(report_text)

                st.download_button(
                    "Download Markdown",
                    report_text,
                    file_name="travel_report.md",
                    mime="text/markdown",
                )

                pdf_response = requests.get(
                    f"{backend_url.rstrip('/')}/report/pdf",
                    timeout=60,
                )
                if pdf_response.status_code == 200:
                    st.download_button(
                        "Download PDF",
                        pdf_response.content,
                        file_name="travel_report.pdf",
                        mime="application/pdf",
                    )
                else:
                    st.warning("PDF generation endpoint returned an error.")

            except requests.RequestException as exc:
                st.error(f"Failed to fetch report: {exc}")
                if exc.response is not None:
                    try:
                        st.write(exc.response.text)
                    except Exception:
                        pass
        else:
            st.warning("No report file path returned from the backend.")

    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")
        if exc.response is not None:
            try:
                st.write(exc.response.text)
            except Exception:
                pass
        st.write("Make sure the FastAPI backend is running at the configured URL.")
