import streamlit as st
import math

st.title("Git Photos")

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
    