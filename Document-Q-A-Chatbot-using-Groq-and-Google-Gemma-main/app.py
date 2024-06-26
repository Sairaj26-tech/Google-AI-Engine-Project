import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

#load the GROQ and Google API key from .enc file

groq_api_key = os.getenv("GROQ_API_KEY")
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

st.title("Document Q&A chatbot")

llm = ChatGroq(groq_api_key=groq_api_key, model="Gemma-7b-It")

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question 
    <context> 
    {context}
    <context>
    Questions: {input}

    """
)

def vec_embed():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.loader = PyPDFDirectoryLoader("./us_census")
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) ## Chunk Creation
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs) #splitting
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings) #vector OpenAI embeddings



st.text("Let's create our vector store ")

if st.button("Create Vector Store"):
    vec_embed()
    st.write("Vector Store DB is ready")

prompt1 = st.text_input("what do you want to ask from the documents?")

if prompt1:
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response=retrieval_chain.invoke({'input':prompt1})
    st.write(response['answer'])

