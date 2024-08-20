import streamlit as st
import base64

st.set_page_config()

col1, col2 = st.columns(2)

with col1:
    st.header("          BIG CORGI IS WATCHING!")
    st.write("Stop procrastination with CORGI!")
    st.write("Who controls the past controls the future.")
    st.write("Who controls the present controls the past.")
    st.write("War is peace.")
    st.write("Freedom is slavery.")
    st.write("Ignorance is strength.")
with col2:
    st.image("1.jpg", use_column_width=True)


# Dodaj automatyczne odtwarzanie dźwięku
audio_file = open('rizz1.mp3', 'rb')
audio_bytes = audio_file.read()

# Zakoduj audio na format base64
audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

# Osadź HTML z dźwiękiem w formacie base64
st.markdown(
    f"""
    <audio autoplay>
    <source src="data:audio/wav;base64,{audio_base64}" type="audio/mp3">
    </audio>
    """,
    unsafe_allow_html=True
)

