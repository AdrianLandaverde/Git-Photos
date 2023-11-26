import streamlit as st
from github import Github
import pandas as pd
import math
from styles import write_text_aligned
from utils import write_image_of_story, get_github_repo, get_history_df 

st.set_page_config(layout="wide")

repo= get_github_repo()
df = get_history_df(repo)

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
df_n_history= df_category[df_category["Date"]==current_date]

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
        write_text_aligned("center",message, "h1")
        write_text_aligned("center",current_date, "h4")
    with col3:
        if st.session_state.n_history<len(dates)-1:
            st.markdown("<br><br>", unsafe_allow_html=True)
            next= st.button("Next Date" + "\n\n"+dates[st.session_state.n_history+1], type="primary")
            if next:
                st.session_state.n_history+=1
                st.rerun()

with st.container():
    for i in range(math.ceil(len(df_n_history)/4)):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if i*4 < len(df_n_history):
                write_image_of_story(df_n_history.iloc[i*4]["Photos"], repo)
        with col2:
            if i*4+1 < len(df_n_history):
                write_image_of_story(df_n_history.iloc[i*4+1]["Photos"], repo)
        with col3:
            if i*4+2 < len(df_n_history):
                write_image_of_story(df_n_history.iloc[i*4+2]["Photos"], repo)
        with col4:
            if i*4+3 < len(df_n_history):
                write_image_of_story(df_n_history.iloc[i*4+3]["Photos"], repo)
