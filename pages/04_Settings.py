import streamlit as st
from github import Github
import pandas as pd
import json
from streamlit_tags import st_tags
from utils import get_github_repo, check_or_create_config_files

st.set_page_config(layout="wide")

st.title("Settings")

g= Github(st.secrets["github_token"])
path= st.secrets["github_user"] + "/" + st.secrets["github_repo"]
repo= g.get_repo(path)

check_or_create_config_files(repo)

json_metadata = json.loads(repo.get_contents("Metadata.json").decoded_content)
albums_metadata = json_metadata["Albums"]

col1, col2 = st.columns(2)

with col1:
    with st.form("my_form"):

        user = st.text_input("Github Username", value= st.secrets["github_user"])
        repo_name = st.text_input("Github Repository Name", value= st.secrets["github_repo"])
        token = st.text_input("Github Token", value= st.secrets["github_token"], type="password")

        albums = st_tags(
            label='Albums',
            text='Press enter to add more',
            value=albums_metadata,
            suggestions=['Family', 'Friends', 'Couple', 'School', 'Other'])
        
        submit_button = st.form_submit_button(label='Update Settings')

        if submit_button:
            albums = sorted(albums)
            contents = repo.get_contents("Metadata.json")
            json_file= {"Albums": albums}
            json_file_bytes = json.dumps(json_file).encode()
            repo.update_file("Metadata.json", "Updated metadata file", json_file_bytes, contents.sha)
            st.toast('Settings updated', icon='💾')