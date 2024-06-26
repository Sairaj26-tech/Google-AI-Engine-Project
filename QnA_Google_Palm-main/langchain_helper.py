from langchain.llms import GooglePalm
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
load_dotenv()

llm = GooglePalm(google_api_key=os.environ['GOOGLE_API_KEY'],temperature=0)
instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
vectordb_file_path = "faiss_index"

def create_vector_db():
    loader = CSVLoader(file_path='codebasics_faqs.csv',source_column='prompt')
    data = loader.load()
    vector_db = FAISS.from_documents(documents=data,embedding=instructor_embeddings)
    vector_db.save_local(vectordb_file_path)

def get_qa_chain():
    # load the vector database from local sysytem
    vector_db = FAISS.load_local(vectordb_file_path,instructor_embeddings)

    # create a retriever for querying the vector database
    retriever = vector_db.as_retriever(score_threshold = 0.7)
    prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {question}"""


    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": PROMPT}

    chain = RetrievalQA.from_chain_type(llm=llm,
                                chain_type="stuff",
                                retriever=retriever,
                                input_key="query",
                                return_source_documents=True,
                                chain_type_kwargs=chain_type_kwargs)
    return chain