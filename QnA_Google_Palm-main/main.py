import streamlit as st
from langchain_helper import create_vector_db,get_qa_chain
import pyautogui

st.title("Tech Master QnA Section❓")

question = st.text_input("Question: ")

if question:
    print(question)
    chain = get_qa_chain()
    response = chain(question)

    st.header("Answer: ")
    st.write(response['result'])
    st.warning('Note: If not satisfied by the answer then send us your query on techmaster@xyz.com')
    if st.button("Reset"):
        pyautogui.hotkey("ctrl","F5")