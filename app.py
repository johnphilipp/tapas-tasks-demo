import streamlit as st
from post_task import post_task
from get_task import get_task


st.markdown("""<a style="display:inline; margin-right: 24px; font-weight: bold; font-size: 2.2em;">Tapas Tasks Demo</a><img src="https://raw.githubusercontent.com/johnphilipp/tapas-tasks-demo/main/qrcode.png" alt="QR Code" style="width:90px; height:90px; display:inline;"></img><br><br>""", unsafe_allow_html=True)

taskName = st.text_input("Task name")
taskType = st.selectbox("Task type", ["computation", "weather"])
if taskType == "computation":
    inputData = st.text_input('Input data (e.g., " 3.5 * sqrt(27) ")')
elif taskType == "weather":
    inputData = st.text_input('Input data (e.g., " St. Gallen ")')
btn = st.button('Submit request')
st.markdown("#")

if btn:
    if taskName == "" or taskType == "" or inputData == "":
        print("x")
        st.warning("Please fill out all fields")
    else:
        result_post = post_task(taskName, taskType, inputData)

        if result_post.status_code == 201:
            st.success("Request posted. Network location: {}".format(
                result_post.headers["Location"]))

            url = result_post.headers["Location"]
            result_get = get_task(url)

            if result_get.status_code == 200:
                result_get = result_get.json()
                if result_get["taskType"] == "computation":
                    if result_get["taskStatus"] == "RUNNING":
                        st.warning("Your request is still running. Please check {} for updates".format(
                            result_post.headers["Location"]))
                    elif "outputData" not in result_get.keys():
                        st.warning(
                            "Sorry, we could not perform this calculation")
                    elif result_get["taskStatus"] == "EXECUTED" and result_get["outputData"] == "FAILED":
                        st.warning(
                            "Sorry, we could not perform this calculation")
                    else:
                        st.success("{} = {}".format(
                            result_get["inputData"], result_get["outputData"]))
                        st.write(result_get)
                elif result_get["taskType"] == "weather":
                    if result_get["taskStatus"] != "EXECUTED":
                        st.warning("Your request is still running. Please check {} for updates".format(
                            result_post.headers["Location"]))
                    # if "outputData" not in result_get.keys():
                    #     st.warning("Your request is still running. Please check {} for updates".format(result_get["inputData"]))
                    elif "java.lang.Object" in result_get["outputData"]:
                        # TODO
                        st.warning("Sorry, we could not find this city")
                    else:
                        st.success("The weather in {} is {} degrees".format(
                            result_get["inputData"], result_get["outputData"]))
                        st.write(result_get)
        else:
            st.warning("Sorry, we could not handle your request.")
