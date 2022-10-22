import streamlit as st
import requests


@st.cache(suppress_st_warning=True)
def post_task(taskName, taskType, inputData):
    data = {
        "taskName": taskName,
        "taskType": taskType,
        "originalTaskUri": "http://example.org",
        "inputData": inputData
    }
    headers = {"Content-Type": "application/task+json"}
    url = "https://tapas-tasks.86-119-35-40.asse.scs.unisg.ch/tasks/"
    return requests.post(url, headers=headers, json=data)
