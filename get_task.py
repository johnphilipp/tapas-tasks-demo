import streamlit as st
import requests


@st.cache(suppress_st_warning=True)
def get_task(url):
    return requests.get(url)
