import streamlit as st


def selectbox(label: str, options: dict, index: int) -> st.selectbox:

    return st.selectbox(
        label = label,
        options = list(options.keys()),
        index = index,
        format_func = lambda x:options[ x ])