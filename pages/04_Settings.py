import streamlit as st
from github import Github
import pandas as pd
import json

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
    json_file= {"Albums": []}
    json_file_bytes = json.dumps(json_file).encode()
    repo.create_file("Metadata.json", "Created metadata file", json_file_bytes)
    st.toast('Metadata file created', icon='📸')