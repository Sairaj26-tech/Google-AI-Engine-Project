import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import time
import tempfile
from googlesearch import search

# Load environment variables
load_dotenv()

# Load the GROQ and Google API keys
groq_api_key = os.getenv('GROQ_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

st.title("Model Document Q&A (Gemma Model)")

llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Questions:{input}
    """
)

def vector_embedding(uploaded_files):
    if "final_documents" not in st.session_state:
        if not uploaded_files or len(uploaded_files) < 2:
            st.write("Please upload at least two PDF files.")
            return

        docs = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name
            loader = PyPDFLoader(temp_file_path)
            docs.extend(loader.load())

        if not docs:
            st.write("No documents found. Please check the uploaded files.")
            return

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        final_documents = text_splitter.split_documents(docs[:20])  # Process the first 20 documents

        if not final_documents:
            st.write("No documents were successfully split. Please verify the document content and try again.")
            return

        # Create embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # Create vector store
        vectors = FAISS.from_documents(final_documents, embeddings)

        # Store in session state
        st.session_state.final_documents = final_documents
        st.session_state.embeddings = embeddings
        st.session_state.vectors = vectors
        st.session_state.vector_store_ready = True

# File uploader widget
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if st.button("Documents Embedding"):
    vector_embedding(uploaded_files)
    st.write("Vector Store DB Is Ready")

# Only show question input if the vector store is ready
if st.session_state.get("vector_store_ready", False):
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "response" not in st.session_state:
        st.session_state.response = None

    new_question = st.text_input("Enter Your Question From Documents")

    if st.button("Get Answer"):
        if new_question:
            st.session_state.conversation.append(f"Q: {new_question}")
            prompt1 = new_question

            document_chain = create_stuff_documents_chain(llm, prompt)
            retriever = st.session_state.vectors.as_retriever()
            retrieval_chain = create_retrieval_chain(retriever, document_chain)

            start = time.process_time()
            response = retrieval_chain.invoke({'input': prompt1})
            response_time = time.process_time() - start

            st.session_state.response = response
            st.session_state.conversation.append(f"A: {response['answer']}")
            st.session_state.conversation.append(f"Response time: {response_time:.2f} seconds")

            st.write("### Answer from PDF")
            st.write(f"**Answer:** {response['answer']}")
            st.write(f"**Response time:** {response_time:.2f} seconds")

            if "context" in st.session_state.response:
                with st.expander("Document Similarity Search"):
                    for i, doc in enumerate(st.session_state.response["context"]):
                        st.write(doc.page_content)
                        st.write("--------------------------------")

            # Google Search
            st.write("### For More info, Take a look in these link")
            try:
                google_results = list(search(new_question, num_results=4))
                for result in google_results:
                    st.write(result)
            except Exception as e:
                st.error(f"Error during Google search: {e}")

    if st.button("Show History"):
        st.write("### Conversation History")
        for message in st.session_state.conversation:
            st.write(message)
