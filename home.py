import streamlit as st
from github import Github
import pandas as pd
import math
from streamlit_extras.stylable_container import stylable_container 
from utils import get_history_df, get_albums_metrics
from styles import get_container_with_border, write_text_aligned

st.set_page_config(layout="wide")

st.title("My Git Photos")

df = get_history_df()
albums, n_photos, last_date, df= get_albums_metrics(df)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total albums", str(len(albums))+ " 📚")
col2.metric("Total stories", str(len(df)) + " 📖")
col3.metric("Total photos", str(n_photos) + " 📷" )
col4.metric("Last day", last_date + " 📅")

for i in range(math.ceil(len(albums)/2)):
    col1, col2 = st.columns(2)
    with col1:
        with stylable_container(key="c1", css_styles=get_container_with_border()):
            if i*3 < len(albums):
                df_album= df[df["Album"]==albums[i*2]].reset_index(drop=True)
                write_text_aligned("center",albums[i*2], "h4")
                for j in range(len(df_album)):
                    coldate, colmessage=  st.columns([1,2])
                    date= df_album.iloc[j]["Date"]
                    message= df_album.iloc[j]["Message"]
                    with coldate:
                        write_text_aligned("right", date, "p")
                    with colmessage:
                        write_text_aligned("left", message, "p")
    with col2:
        with stylable_container(key="c2", css_styles=get_container_with_border()):
            if i*3+1 < len(albums):
                df_album= df[df["Album"]==albums[i*2+1]].reset_index(drop=True)
                write_text_aligned("center",albums[i*2+1], "h4")
                for j in range(len(df_album)):
                    coldate, colmessage= st.columns([1,2])
                    date= df_album.iloc[j]["Date"]
                    message= df_album.iloc[j]["Message"]
                    with coldate:
                        write_text_aligned("right", date, "p")
                    with colmessage:
                        write_text_aligned("left", message, "p")