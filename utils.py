from github import Github
import streamlit as st
import pandas as pd
import json

def get_github_repo():
    g= Github(st.secrets["github_token"])
    path= st.secrets["github_user"] + "/" + st.secrets["github_repo"]
    repo= g.get_repo(path)
    return repo

def get_history_df(repo=None):
    if repo is None:
        repo= get_github_repo()
    contents = repo.get_contents("History.csv")
    df = pd.read_csv(contents.download_url)
    return df

def get_albums_metrics(df):
    df= df.groupby(by=["Album", "Date", "Message"]).count().reset_index(drop=False)
    albums= df["Album"].unique()
    n_photos= len(df)
    df= df.groupby(by=["Album", "Date", "Message"]).count().reset_index(drop=False)
    albums= df["Album"].unique()
    dates_total= df["Date"].unique()
    dates_total= pd.to_datetime(dates_total)
    dates_total= dates_total.sort_values()
    last_date= dates_total[-1]
    last_date= last_date.strftime("%Y-%m-%d")
    return albums, n_photos, last_date, df

def create_file(repo, name, message, content):
    repo.create_file(name, message, content)

def update_history_file(repo, df):
    contents= repo.get_contents("History.csv")
    df_original= pd.read_csv(contents.download_url)
    df= pd.concat([df_original, df])
    df_bytes = df.to_csv(index=False).encode()
    repo.update_file("History.csv", "Updated history file", df_bytes, contents.sha)

def write_image_of_story(photo, repo):
    contents = repo.get_contents(photo)
    image= contents.download_url
    return st.image(image, use_column_width = True)

def check_or_create_config_files(repo):
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
    
