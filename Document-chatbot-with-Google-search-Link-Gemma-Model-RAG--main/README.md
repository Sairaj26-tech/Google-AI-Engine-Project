**Model Document Q&A (Gemma Model)**

Welcome to the Gemma Model Document Question & Answer (Q&A) application! This Streamlit app allows you to upload PDF documents, ask questions related to their content, and receive answers generated by the Gemma Model, an advanced language model specifically trained for document understanding.

### How to Use:

1. **Upload PDF Files**: Start by uploading any number of PDF files containing the documents you want to explore.

2. **Embedding Documents**: Click the "Documents Embedding" button to process the uploaded PDF files. This step involves splitting the documents into smaller chunks, generating embeddings using the Google Generative AI, and creating a vector store for efficient retrieval.

3. **Ask Questions**: Once the vector store is ready, you can input your questions related to the uploaded documents. Type your question in the text input field provided.

4. **Get Answers**: Click the "Get Answer" button to receive answers to your questions. The Gemma Model will analyze the documents' content and provide accurate responses based on the context.

5. **Explore Document Similarity**: If available, you can expand the "Document Similarity Search" section to explore other document snippets similar to the context of your question.

6. **Additional Information**: For more information related to your question, relevant Google search results will be displayed below the document similarity section.

7. **Conversation History**: You can review the conversation history by clicking the "Show History" button. It displays a chronological list of questions asked and responses received during the session.

### Requirements:

- Python 3.7 or higher
- Streamlit
- Google API Key
- GROQ API Key
- Other necessary dependencies (specified in the code)

### Installation:

1. Clone the repository or download the provided files.

2. Install the required Python dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Google API Key and GROQ API Key as environment variables.

4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

### About Gemma Model:

The Gemma Model is a state-of-the-art language model designed for document understanding tasks, including question-answering, summarization, and document similarity analysis. It leverages advanced techniques in natural language processing and machine learning to provide accurate and contextually relevant responses.

### Contributors:

- Srivatsan (Owner)

### Feedback:

We welcome your feedback and contributions to enhance the Gemma Model Document Q&A application. Please feel free to reach out with any suggestions, bug reports, or feature requests. Happy exploring!
