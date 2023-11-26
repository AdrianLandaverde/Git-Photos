import streamlit as st
import math
from github import Github
import datetime
from stqdm import stqdm
import pandas as pd
import json
import time
from utils import get_github_repo, create_file, update_history_file

st.set_page_config(layout="wide")

st.title("Upload Photos")

repo= get_github_repo()
json_metadata = json.loads(repo.get_contents("Metadata.json").decoded_content)
try:
    temp= st.session_state.upload_file_key
except:
    st.session_state.upload_file_key= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

col_upload, col_metadata = st.columns([3,1])
with col_upload:
    st.session_state.images = []
    st.session_state.images_names= []

    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True, key=st.session_state.upload_file_key)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.session_state.images.append(bytes_data)
        st.session_state.images_names.append(uploaded_file.name)
        
    for i in range(math.ceil(len(st.session_state.images)/3)):
        col1, col2, col3 = st.columns(3)
        with col1:
            if i*3 < len(st.session_state.images):
                st.image(st.session_state.images[i*3], caption=st.session_state.images_names[i*3], use_column_width = True)
        with col2:
            if i*3+1 < len(st.session_state.images):
                st.image(st.session_state.images[i*3+1], caption=st.session_state.images_names[i*3+1], use_column_width = True)
        with col3:
            if i*3+2 < len(st.session_state.images):
                st.image(st.session_state.images[i*3+2], caption=st.session_state.images_names[i*3+2], use_column_width = True)
            
with col_metadata:
    with st.form("my_form"):
        option = st.selectbox(
        'Album',
        json_metadata["Albums"])

        date = st.date_input("Date of event", value=datetime.datetime.now())
        message = st.text_input(
            "Message 👇",
            placeholder= "An amazing day ✨",
        )

        submitted = st.form_submit_button("Upload Files")
        if submitted:
            list_info= []
            for i in stqdm(range(len(st.session_state.images)), desc="Uploading files"):
                date_string= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                create_file(repo, date_string+".jpg", "Upload photo", st.session_state.images[i])
                list_info.append([date, option, message, date_string+".jpg"])

            with st.spinner('Loading final files into Github...'):
                df= pd.DataFrame(list_info, columns=["Date", "Album", "Message", "Photos"])
                update_history_file(repo, df)

            st.balloons()
            st.toast('Photos uploaded successfully', icon='📸')
            time.sleep(5)
            st.session_state.upload_file_key= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            st.rerun()