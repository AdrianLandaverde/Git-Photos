import streamlit as st

def get_container_with_border():
    return """
    {
        border: 1px solid rgba(49, 51, 63, 0.9);
        border-radius: 0.5rem;
        padding: calc(1em - 1px)
    }
    """

def write_text_aligned(align, text, type):
    #return f"<{type} style='text-align: {align};'>{text}</{type}>"
    return st.markdown(f"<{type} style='text-align: {align};'>{text}</{type}>",  unsafe_allow_html=True)


