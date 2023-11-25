import streamlit as st
import math
from github import Github
import datetime
from stqdm import stqdm

st.set_page_config(layout="wide")

st.title("Upload Photos")

col_upload, col_metadata = st.columns([3,1])

with col_upload:
    st.session_state.images = []
    st.session_state.images_names= []

    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        #st.image(bytes_data)
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
        

    if st.button('Upload Files'):
        g= Github(st.secrets["github_token"])
        path= st.secrets["github_user"] + "/" + st.secrets["github_repo"]
        repo= g.get_repo(path)
        for i in stqdm(range(len(st.session_state.images)), desc="Uploading files"):
            st.write("Uploading file "+str(i))
            datetime= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            repo.create_file(st.session_state.images_names[i], "Upload photo at "+datetime, st.session_state.images[i])
            
with col_metadata:
    option = st.selectbox(
    'Album',
    ('Couple', 'Studyng Abroad', 'Family', 'Other'))

    date = st.date_input("Date of event", value=datetime.datetime.now())
    st.write(date)

    message = st.text_input(
        "Message 👇",
        placeholder= "An amazing day ✨",
    )