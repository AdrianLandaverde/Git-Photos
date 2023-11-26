import streamlit as st
from github import Github
import pandas as pd
import math
from streamlit_extras.stylable_container import stylable_container 

st.set_page_config(layout="wide")

st.title("My Git Photos")

g= Github(st.secrets["github_token"])
path= st.secrets["github_user"] + "/" + st.secrets["github_repo"]
repo= g.get_repo(path)

contents = repo.get_contents("History.csv")
df = pd.read_csv(contents.download_url)
n_photos= len(df)
df= df.groupby(by=["Album", "Date", "Message"]).count().reset_index(drop=False)
albums= df["Album"].unique()

col1, col2, col3, col4 = st.columns(4)
dates_total= df["Date"].unique()
dates_total= pd.to_datetime(dates_total)
dates_total= dates_total.sort_values()
last_date= dates_total[-1]
last_date= last_date.strftime("%Y-%m-%d")
col1.metric("Total albums", str(len(albums))+ " 📚")
col2.metric("Total stories", str(len(df)) + " 📖")
col3.metric("Total photos", str(n_photos) + " 📷" )
col4.metric("Last day", last_date + " 📅")

for i in range(math.ceil(len(albums)/2)):
    col1, col2 = st.columns(2)
    with col1:
        with stylable_container(key="container_with_border", css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.9);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """):
            if i*3 < len(albums):
                df_album= df[df["Album"]==albums[i*2]]
                df_album= df_album.reset_index(drop=True)
                st.markdown(f"<h4 style='text-align: center;'>{albums[i*2]}</h4>",  unsafe_allow_html=True)
                for j in range(len(df_album)):
                    coldate, colmessage=  st.columns([1,2])
                    date= df_album.iloc[j]["Date"]
                    message= df_album.iloc[j]["Message"]
                    with coldate:
                        st.markdown(f"<p style='text-align: right;'>{date}</p>",  unsafe_allow_html=True)
                    with colmessage:
                        st.markdown(f"<p style='text-align: left;'>{message}</p>",  unsafe_allow_html=True)
    with col2:
        with stylable_container(key="container_with_border", css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.9);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """):
            if i*3+1 < len(albums):
                df_album= df[df["Album"]==albums[i*2+1]]
                df_album= df_album.reset_index(drop=True)
                st.markdown(f"<h4 style='text-align: center;'>{albums[i*2+1]}</h4>",  unsafe_allow_html=True)
                for j in range(len(df_album)):
                    coldate, colmessage= st.columns([1,2])
                    date= df_album.iloc[j]["Date"]
                    message= df_album.iloc[j]["Message"]
                    with coldate:
                        st.markdown(f"<p style='text-align: right;'>{date}</p>",  unsafe_allow_html=True)
                    with colmessage:
                        st.markdown(f"<p style='text-align: left;'>{message}</p>",  unsafe_allow_html=True)