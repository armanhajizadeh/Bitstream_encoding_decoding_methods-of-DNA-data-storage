import streamlit as st

st.title("My Web App")
st.write("This is a simple Streamlit app!")

name = st.text_input("Enter your name")
if name:
    st.write(f"Hello, {name}!")
