import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime
import sqlite3

# Security
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
conn = sqlite3.connect('user_data.db')
c = conn.cursor()

# DB Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable (id INTEGER PRIMARY KEY AUTOINCREMENT, mobile_no TEXT, password TEXT)')

def add_userdata(mobile_no, password):
    c.execute('INSERT INTO userstable(mobile_no, password) VALUES (?, ?)', (mobile_no, password))
    conn.commit()

def create_patient_datatable():
    c.execute('CREATE TABLE IF NOT EXISTS patientstable (id INTEGER PRIMARY KEY AUTOINCREMENT, mobile_no TEXT, patient_name TEXT, dob DATE, date_of_diagnosis DATE, date_of_1st_chemo DATE, date DATE, temperature TEXT, weight TEXT, height TEXT, protocol_of_chemotherapy TEXT, phase_of_chemotherapy_week TEXT, selected_symptoms TEXT)')

def add_patient_data(mobile_no, patient_name, dob, date_of_diagnosis, date_of_1st_chemo, date, temperature, weight, height, protocol_of_chemotherapy, phase_of_chemotherapy_week, selected_symptoms):
    c.execute('INSERT INTO patientstable(mobile_no, patient_name, dob, date_of_diagnosis, date_of_1st_chemo, date, temperature, weight, height, protocol_of_chemotherapy, phase_of_chemotherapy_week, selected_symptoms) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (mobile_no, patient_name, dob, date_of_diagnosis, date_of_1st_chemo, date, temperature, weight, height, protocol_of_chemotherapy, phase_of_chemotherapy_week, selected_symptoms))
    conn.commit()

def login_user(mobile_no, password):
    c.execute('SELECT * FROM userstable WHERE mobile_no = ? AND password = ?', (mobile_no, password))
    data3 = c.fetchall()
    return data3

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data3 = c.fetchall()
    return data3

def view_previous_data(mobile_no):
    c.execute('SELECT * FROM patientstable WHERE mobile_no = ?', (mobile_no,))
    data3 = c.fetchall()
    return data3

# Session State
class SessionState:
    def __init__(self):
        self.mobile_no = ""
        self.strong_password = ""
        self.selected_task = ""
        self.choice = ""
        self.logged_in = False  # Track login status

state = SessionState()

def main():
    """Simple Login App"""
    st.title("ChemoAssist App")

    menu = ["Home", "Login", "SignUp","Previous Data"]
    state.choice = st.sidebar.selectbox("Menu", menu)

    if state.choice == "Home":
        st.subheader("Welcome to Chemo Assist App")
        st.image("Chemo.jpg", caption="Chemo Assist App", use_column_width=True)
        st.markdown(
            "Chemo Assist App is a comprehensive tool designed to assist healthcare professionals and patients in managing chemotherapy treatments. It provides features for recording patient information, tracking physical data, managing chemotherapy protocols, and offering self-management guidelines for symptoms.")

    elif state.choice == "Login":
        if not state.logged_in:  # Display login section only if not logged in
            st.subheader("Fill in the Patient's data from DATA demographics below")

            state.mobile_no = st.sidebar.text_input("Mobile no", state.mobile_no)
            state.strong_password = st.sidebar.text_input("Password", type='password', value=state.strong_password)
            create_usertable()  # Moved table creation here

            if st.sidebar.button("Login"):
                result = login_user(state.mobile_no, check_hashes(state.strong_password, make_hashes(state.strong_password)))
                if result:
                    state.logged_in = True  # Mark user as logged in
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
                if st.button("Save Patient Data"):
                    create_patient_datatable()
                    add_patient_data(state.mobile_no, patient_name, dob, date_of_diagnosis, date_of_1st_chemo, datetime.today(), "", "", "", "", "", "")
                    st.success("Patient Data saved successfully!")

            elif state.selected_task == "Physical Data":
                st.subheader("Physical Data")
                date = st.date_input("Date", datetime.today())
                temperature = st.text_input("Temperature")
                weight = st.text_input("Weight")
                height = st.text_input("Height")
                if st.button("Save Physical Data"):
                    add_patient_data(state.mobile_no, "", "", "", "", date, temperature, weight, height, "", "", "")
                    st.success("Physical Data saved successfully!")

            elif state.selected_task == "Chemotherapy":
                st.subheader("Chemotherapy")
                protocol_of_chemotherapy = st.text_input("Protocol of chemotherapy")
                phase_of_chemotherapy_week = st.text_input("Phase of chemotherapy week")
                if st.button("Save Chemotherapy Data"):
                    add_patient_data(state.mobile_no, "", "", "", "", datetime.today(), "", "", "", protocol_of_chemotherapy, phase_of_chemotherapy_week, "")
                    st.success("Chemotherapy Data saved successfully!")

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
                    st.success("Symptom Management Data saved successfully!")

    elif state.choice == "SignUp":
        st.subheader("Create New Account")
        new_mobile_no = st.text_input("Mobile no")
        new_strong_password = st.text_input("Strong Password", type='password')

        if st.button("Signup"):
            add_userdata(new_mobile_no, make_hashes(new_strong_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

    elif state.choice == "Previous Data":  # Handle the "Previous Data" section
        st.subheader("Previous Data")
        if not state.logged_in:
            previous_data = view_previous_data(state.mobile_no)
            if previous_data:
                st.write("Previous Data:")
                df = pd.DataFrame(previous_data, columns=["ID", "Mobile No", "Patient Name", "DOB", "Date of Diagnosis",
                                                          "Date of 1st Chemo", "Date", "Temperature", "Weight",
                                                          "Height", "Protocol of Chemotherapy",
                                                          "Phase of Chemotherapy Week", "Selected Symptoms"])
                st.dataframe(df)
            else:
                st.info("No previous data found.")
        else:
            st.warning("Please log in to view previous data.")
if __name__ == '__main__':
    main()
