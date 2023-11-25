import streamlit as st
from github import Github
import pandas as pd
import json
from streamlit_tags import st_tags

st.title("Settings")

g= Github(st.secrets["github_token"])
path= st.secrets["github_user"] + "/" + st.secrets["github_repo"]
repo= g.get_repo(path)

try:
    contents = repo.get_contents("History.csv")
except:
    df= pd.DataFrame(columns=["Date", "Album", "Message", "Photos"])
    df_bytes = df.to_csv(index=False).encode()
    repo.create_file("History.csv", "Created history file", df_bytes)
    st.toast('History file created', icon='📸')

try:
    contents = repo.get_contents("Metadata.json")
except:
    json_file= {"Albums": ['Other']}
    json_file_bytes = json.dumps(json_file).encode()
    repo.create_file("Metadata.json", "Created metadata file", json_file_bytes)
    st.toast('Metadata file created', icon='📸')

json_metadata = json.loads(repo.get_contents("Metadata.json").decoded_content)
albums_metadata = json_metadata["Albums"]

user = st.text_input("Github Username", value= st.secrets["github_user"])
repo_name = st.text_input("Github Repository Name", value= st.secrets["github_repo"])
token = st.text_input("Github Token", value= st.secrets["github_token"], type="password")

albums = st_tags(
    label='Albums',
    text='Press enter to add more',
    value=albums_metadata,
    suggestions=['Family', 'Friends', 'Couple', 'School', 'Other'])

if st.button('Update Settings'):
    st.toast('Settings updated', icon='💾')