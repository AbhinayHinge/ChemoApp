import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

# Security
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
import sqlite3
conn = sqlite3.connect('data3.db')
c = conn.cursor()

# DB Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable (id INTEGER PRIMARY KEY AUTOINCREMENT, mobile_no TEXT, password TEXT)')

def add_userdata(mobile_no, password):
    c.execute('INSERT INTO userstable(mobile_no, password) VALUES (?, ?)', (mobile_no, password))
    conn.commit()

def login_user(mobile_no, password):
    c.execute('SELECT * FROM userstable WHERE mobile_no = ? AND password = ?', (mobile_no, password))
    data3 = c.fetchall()
    return data3

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data3 = c.fetchall()
    return data3

# Session State
class SessionState:
    def __init__(self):
        self.mobile_no = ""
        self.strong_password = ""
        self.selected_task = ""
        self.choice = ""

state = SessionState()

def main():
    """Simple Login App"""
    st.title("ChemoAssist App")

    menu = ["Home", "Login", "SignUp"]
    state.choice = st.sidebar.selectbox("Menu", menu)

    if state.choice == "Home":
        st.subheader("Welcome to Chemo Assist App")
        st.image("Chemo.jpg", caption="Chemo Assist App", use_column_width=True)
        st.markdown(
            "Chemo Assist App is a comprehensive tool designed to assist healthcare professionals and patients in managing chemotherapy treatments. It provides features for recording patient information, tracking physical data, managing chemotherapy protocols, and offering self-management guidelines for symptoms.")

    elif state.choice == "Login":
        st.subheader("Fill in the Patient's data from DATA demographics below")

        state.mobile_no = st.sidebar.text_input("Mobile no", state.mobile_no)
        state.strong_password = st.sidebar.text_input("Password", type='password', value=state.strong_password)
        create_usertable()  # Moved table creation here

        result = login_user(state.mobile_no, check_hashes(state.strong_password, make_hashes(state.strong_password)))
        if result:
            st.success("Logged In as {}".format(state.mobile_no))
        else:
            st.warning("Incorrect Mobile no/Strong Password")

        state.selected_task = st.selectbox("Task",
                            ["Patients Demographic Data", "Physical Data", "Chemotherapy", "Symptom Management"])

        if state.selected_task == "Patients Demographic Data":
            st.subheader("Patients Demographic Data")
            patient_name = st.text_input("Patient's Name")
            dob = st.date_input("Date of Birth", datetime.today())
            date_of_diagnosis = st.date_input("Date of Diagnosis", datetime.today())
            date_of_1st_chemo = st.date_input("Date of 1st chemotherapy", datetime.today())

        elif state.selected_task == "Physical Data":
            st.subheader("Physical Data")
            date = st.date_input("Date", datetime.today())
            temperature = st.text_input("Temperature")
            weight = st.text_input("Weight")
            height = st.text_input("Height")

        elif state.selected_task == "Chemotherapy":
            st.subheader("Chemotherapy")
            protocol_of_chemotherapy = st.text_input("Protocol of chemotherapy")
            phase_of_chemotherapy_week = st.text_input("Phase of chemotherapy week")
            # Add chemotherapy data collection here

        elif state.selected_task == "Symptom Management":
            st.subheader("Symptom Management")
            selected_symptoms = st.multiselect("Select Symptoms",
                                               ["Nausea and Vomiting", "Fever", "Diarrhea", "Constipation", "Pain",
                                                "No Symptoms"])
            st.write(f"Selected Symptoms: {', '.join(selected_symptoms)}")

            if st.button("Self Management Guidelines"):
                # Provide self-management guidelines based on selected symptoms
                st.write("Here are the self-management guidelines for the selected symptoms:")
                for symptom in selected_symptoms:
                    if symptom == "Nausea and Vomiting":
                        st.write("- Stay hydrated and sip clear fluids.")
                    elif symptom == "Fever":
                        st.write("- Rest and drink plenty of fluids.")
                    # Add guidelines for other symptoms here

    elif state.choice == "SignUp":
        st.subheader("Create New Account")
        new_mobile_no = st.text_input("Mobile no")
        new_strong_password = st.text_input("Strong Password", type='password')

        if st.button("Signup"):
            add_userdata(new_mobile_no, make_hashes(new_strong_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

if __name__ == '__main__':
    main()
