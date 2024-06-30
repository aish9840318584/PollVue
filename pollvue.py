import streamlit as st
import dashboard
import new
import login
import my_nltk_script


st.set_page_config(page_title="PollVue", layout="wide")


st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", ["Home", "Dashboard", "Login/Signup", "Statistics"])


if page == "Home":
    new.main()
elif page == "Dashboard":
    dashboard.main()
elif page == "Login/Signup":
    login.main()
elif page == "Statistics":
    my_nltk_script.main()



