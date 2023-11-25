import streamlit as st
from github import Github
import pandas as pd
import json

st.set_page_config(layout="wide")

g= Github(st.secrets["github_token"])
path= st.secrets["github_user"] + "/" + st.secrets["github_repo"]
repo= g.get_repo(path)

contents = repo.get_contents("History.csv")
df = pd.read_csv(contents.download_url)

categories = df["Album"].unique()
df_category= df[df["Album"] == categories[0]]
df_category= df_category.sort_values(by=['Date', 'Message'], ascending=[True,False])
dates= df_category["Date"].unique()
messages= df_category["Message"].unique()

try:
    temp= st.session_state.n_history
except:
    st.session_state.n_history= 0

current_date= dates[st.session_state.n_history]
message= messages[st.session_state.n_history]


with st.container():
    col1, col2, col3= st.columns([1, 6, 1])
    with col1:
        if st.session_state.n_history>0:
            st.markdown("<br><br>", unsafe_allow_html=True)
            previous= st.button("Previous Date\n\n"  +dates[st.session_state.n_history-1], type="primary")
            if previous:
                st.session_state.n_history-=1
                st.rerun()
            
    with col2:
        st.markdown(f"<h1 style='text-align: center;'>---{message}---</h1>",  unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center;'>---{current_date}---</h4>",  unsafe_allow_html=True)
    with col3:
        if st.session_state.n_history<len(dates)-1:
            st.markdown("<br><br>", unsafe_allow_html=True)
            next= st.button("Next Date" + "\n\n"+dates[st.session_state.n_history+1], type="primary")
            if next:
                st.session_state.n_history+=1
                st.rerun()
