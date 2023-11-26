from github import Github
import streamlit as st
import pandas as pd

def get_github_repo():
    g= Github(st.secrets["github_token"])
    path= st.secrets["github_user"] + "/" + st.secrets["github_repo"]
    repo= g.get_repo(path)
    return repo

def get_history_df():
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
    
