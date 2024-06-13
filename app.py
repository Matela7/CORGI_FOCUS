import streamlit as st

st.set_page_config()

col1, col2 = st.columns(2)

with col1:
    st.header("          BIG CORGI IS WATCHING!")
    st.write("Stop procrastination with CORGI!")
    st.write("Who controls the past controls the future.")
    st.write("Who controls the present controls the past.")
    st.write("War is peace.")
    st.write("Freedom is slavery.")
with col2:
    st.image("1.jpg", use_column_width=True, )


