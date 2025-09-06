import streamlit as st

st.title("Health Care AI Assistance")

st.text_input("Enter your health-related question: ")

st.sidebar.header("Patient Profile")

st.sidebar.text_input("Name")

st.sidebar.number_input("Age",0,100)

st.sidebar.selectbox("Gender",["Male","Female","Other"])

st.sidebar.text_area("Medical History")

st.sidebar.text_area("Current Medications")

st.sidebar.text_input("Allergies")
