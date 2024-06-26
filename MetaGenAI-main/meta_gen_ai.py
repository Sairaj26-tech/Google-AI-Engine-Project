# file format -  Parquet, ORC, JSON, CSV
import streamlit as st, fnmatch

# Define custom CSS to adjust column positions
st.set_page_config(layout="wide",
                   page_title="MetaGenAI",
                   page_icon="🧊",
                   )

st.header("MetaGenAI :wave:", divider='rainbow')
st.markdown("###### Where Data Meets Clarity")

class FileTypeIdentification:
    def __init__(self):
        self.files_type = ['Apache ORC', 'Apache Parquet', 'CSV', 'ascii text', 'JSON'] #ascii text for json

    def detect_file_format(self, filename) -> list:
        from polyfile.magic import MagicMatcher
        return MagicMatcher.DEFAULT_INSTANCE.match(filename.read(1024))

    def match_file_type(self, partial_text):
        matches = [file_type for file_type in self.files_type if fnmatch.fnmatch(partial_text, f"{file_type}*")]
        print("bool(matches)", bool(matches), matches)
        return bool(matches), matches

    def detect_exact_file_format(self, filename):
        try:
            ext = []
            files_extensions = list(self.detect_file_format(filename))
            for files_extension in files_extensions:
                matched, ext = self.match_file_type(files_extension.message())
                if matched:
                    break
            if len(ext) == 0:
                return None
            detected_file_format = self.infer_detect_file_format_for_SqlCsvText(filename, ext[0])
            print("Detected File Format: ", detected_file_format)
            return self.infer_schema(filename, detected_file_format) if detected_file_format is not None else None
        except Exception as e:
            raise Exception(e)

    def infer_detect_file_format_for_SqlCsvText(self, file_path, file_format):
        if file_format == 'ascii text':
            file_start = file_path.readline()
            # Check if it starts with { or [
            if file_start.startswith(b'{') or file_start.startswith(b'['):
                return "JSON"
            else:
                return "Unknown"
        return file_format

    def infer_schema(self, file_path, file_format: str):
        if file_format == 'Apache ORC':
            from pyarrow import orc
            orc_file = orc.read_table(file_path)
            return orc_file.schema, orc_file.column_names, orc_file.to_pandas()
        elif file_format == 'Apache Parquet':
            import pyarrow.parquet as pq
            parquet_file = pq.read_table(file_path)
            return parquet_file.schema, parquet_file.column_names, parquet_file.to_pandas()
        elif 'Apache Avro' in file_format:
            pass
        elif 'CSV' == file_format:
            import pandas as pd
            csv_file = pd.read_csv(file_path, header=None)
            return csv_file.dtypes, csv_file.columns, csv_file
        elif file_format == 'JSON':
            from pyarrow import json
            json_file = json.read_json(file_path)
            return json_file.schema, json_file.column_names, json_file.to_pandas()
        return None


submit_button = False
top_k = 150
temperature = 1.0
max_new_tokens = 1200
model = "google/gemma-1.1-7b-it"
response = ""
files_data = []
col1, col2 = st.columns([0.5, 0.5])
file_info = FileTypeIdentification()
query_input = ""


import requests
def query(model, payload):
    try:
        API_URL = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {st.secrets['HUGGING_FACE_KEY']}"}
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Parse response JSON
    except requests.exceptions.RequestException as e:
        print("RequestException:", e)  # Print error message
        raise Exception(e) # Return None if request fails
    except Exception as ex:
        print("Error: ", ex)
        raise Exception(ex)

with col1:
    try:
        with st.form(key='metaGenAIForm'):
            uploaded_files = st.file_uploader("Choose file(s)", accept_multiple_files=True, type=['parquet', 'orc'])
            st.subheader("Features! :smile:", divider='rainbow')
            schema = st.checkbox("Schema Extraction", key='schema', value=True)
            outliers = st.checkbox("Identifying Potential Outliers", key='outliers', value=True)
            contextual = st.checkbox("Contextual Metadata", key='contextual', value=True)
            relationship = st.checkbox("Relationship between datasets", key='relationship', value=True)
            top_k = st.slider("Select your top_k", 0, 1100, 150)
            temperature = st.slider("Select your temperature", 0.00, 100.0, 1.0)
            max_new_tokens = st.slider("Select your max new tokens", 0, 3000, 1200)
            model = st.selectbox(
                "Select your GenAI model",
                ("google/gemma-1.1-7b-it", "meta-llama/Meta-Llama-3-70B-Instruct")
            )
            submit_button = st.form_submit_button(label='Submit')
            questions = {"data_distribution": ["Can you provide a summary of the central tendency measures (mean, median, mode) for each numerical column?",
                                               "How does the skewness or symmetry of the data distribution influence the choice of statistical models or machine learning algorithms?",
                                               "Are there any specific models or techniques that are better suited for skewed or symmetric data distributions?",
                                               "Are there any real-world implications or interpretations of the observed data distribution and skewness?",
                                               "How might the skewness impact decision-making or business strategies?"
                               ],
                         "outliers": ["Are there any outliers present in the numerical columns?",
                                      "How do these outliers impact the overall data distribution and analysis?",
                                      "Are there any techniques or methods you would suggest for handling or analyzing the outliers?"],
                         "contextual": ["What is the primary objective or purpose of collecting this dataset?",
                                        "Are there any specific research questions, business goals, or analytical tasks that this dataset aims to address?",
                                        "Who are the intended users or stakeholders of the dataset, and what are their specific needs or interests?"],
                         "data_quality": ["How many null values are present in the dataset for each field? Which fields are considered key fields and cannot be null? How might the missing values impact any potential joins?",
                                          "Are there any potential data quality issues in the dataset, such as duplicate records or inconsistent formatting? How can I address them?",
                                          "How can I identify and handle missing or null values in the dataset, especially in columns"],
                         "relationship": ["What can you tell me about this model?",
                                          "How are the different tables or entities in the dataset related to each other?"],
                         "schema": ["DDL in sql?"]}


            if submit_button:
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        file_detail_parsed = file_info.detect_exact_file_format(uploaded_file)
                        if file_detail_parsed is not None:
                            schema, columns, df = file_detail_parsed
                            files_data.append((uploaded_file.name, df, columns))
                            st.write("filename: ", uploaded_file.name)
                        else:
                            st.error(f'Unable to load {uploaded_file.name}', icon="🚨")

                if not any([schema, outliers, contextual, relationship]):
                    st.error("Please select at least one feature.")
                elif not uploaded_files:
                    st.error("Please upload at least one file.")
                else:
                    prompts = ""
                    if schema:
                        prompts += "\n".join(questions['schema']) + "\n"
                    if outliers:
                        prompts += "\n".join(questions['outliers']) + "\n"
                    if contextual:
                        prompts += "\n".join(questions['contextual']) + "\n"
                    if relationship:
                        prompts += "\n".join(questions['relationship']) + "\n"

                    for file_data in files_data:
                        print("Data: ", file_data[1].head(1000).to_markdown(tablefmt="grid"))
                        query_input += f"""{str(file_data[1].head(1000).to_string())}\n"""
                    if len(files_data) > 0:
                        query_input += f"I required the following things-\n{prompts}"

    except Exception as e:
        st.error(e)

with col2:
    # tab1, tab2, tab3, tab4 = st.tabs(["Granularity", "File Meta", "Semantic Context", "Data Analysis"])
    tab1, tab2, tab4 = st.tabs(["Granularity", "File Meta", "Data Analysis"])
    with tab1:
        if submit_button:
            with st.spinner("Request. Respond. Repeat. With Meta Gen AI"):
                try:
                    response = query(model, {
                        "inputs": query_input,
                        "parameters": {
                            "top_k": top_k,
                            "max_new_tokens": max_new_tokens,
                            "return_full_text": False,
                            "temperature": temperature,
                        },
                        "options": {
                            "use_cache": False,
                            "wait_for_model": True
                        }
                    })
                    if response is not None:
                        st.balloons()
                        submit_button = False
                        st.markdown(response[0]['generated_text'])
                        st.success("Response received")
                except Exception as ex:
                    st.balloons()
                    submit_button = False
                    st.error(f"Failed to get response from the API. - {ex}")

    with tab2:
        try:
            with st.spinner("Request. Respond. Repeat. With Meta Gen AI"):
                for file_data in files_data:
                    st.title(file_data[0])
                    df = file_data[1]
                    dict_cols = [col for col in df.columns if
                                 df[col].dtype == 'object' and (df[col].apply(lambda x: isinstance(x, dict)).any() or df[col].apply(lambda x: isinstance(x, list)).any())]

                    for col in dict_cols:
                        df[col] = df[col].apply(str)
                    st.dataframe(df.head(1000))
        except Exception as e:
            st.error(e)

    # with tab3:
    #     import pandas as pd
    #     import nltk
    #
    #     # Check if the required data has already been downloaded
    #     try:
    #         nltk.data.find('tokenizers/punkt')
    #         nltk.data.find('corpora/stopwords.zip')
    #         nltk.data.find('corpora/wordnet.zip')
    #         required_data_downloaded = True
    #     except LookupError:
    #         required_data_downloaded = False
    #
    #     # If the required data has not been downloaded, download it
    #     if not required_data_downloaded:
    #         nltk.download('punkt')
    #         nltk.download('stopwords')
    #         nltk.download('wordnet')
    #
    #     def extract_metadata(column_name, df):
    #         try:
    #             from textblob import TextBlob
    #             column_data = df[column_name].dropna().tolist()
    #
    #             # Convert column_data to strings if they are not numeric
    #             if not pd.api.types.is_numeric_dtype(column_data):
    #                 column_data = [str(value) for value in column_data]
    #
    #             blob = TextBlob(" ".join(column_data))
    #             noun_phrases = blob.noun_phrases
    #             metadata = {
    #                 "Column Name": column_name,
    #                 "Data Type": df[column_name].dtype,
    #                 "Unique Values": len(set(column_data)),
    #                 "Sample Values": column_data[:5],
    #                 "Semantic Context": noun_phrases
    #             }
    #             return metadata
    #         except Exception as e:
    #             raise Exception(e)
    #
    #     with st.spinner("Request. Respond. Repeat. With Meta Gen AI"):
    #         try:
    #             for file_data in files_data:
    #                 st.title(file_data[0])
    #                 df = file_data[1].convert_dtypes()
    #                 metadata_list = [extract_metadata(col, df.head(1000)) for col in file_data[2]]
    #                 # Create a DataFrame to store the extracted metadata
    #                 metadata_df = pd.DataFrame(metadata_list)
    #                 st.dataframe(metadata_df)
    #         except Exception as e:
    #             st.error(e)

    with tab4:
        import matplotlib.pyplot as plt
        import seaborn as sns
        try:
            # Disable the PyplotGlobalUseWarning
            st.set_option('deprecation.showPyplotGlobalUse', False)
            # Data distribution and skewness
            with st.spinner("Request. Respond. Repeat. With Meta Gen AI"):
                for file_data in files_data:
                    st.title(file_data[0])
                    st.markdown("###### Data Distribution")  # Add a title for the line chart
                    numeric_columns = file_data[1].select_dtypes(include=['int64', 'float64']).columns
                    # Create a figure and axis for box plots
                    fig, ax = plt.subplots(figsize=(12, 6))
                    for i, col in enumerate(numeric_columns, 1):
                        plt.subplot(1, len(numeric_columns), i)
                        sns.boxplot(x=file_data[1][col], ax=ax)
                        plt.title(f"Box Plot for {col}")
                        ax.set_title(col)
                    st.pyplot(fig)  # Use st.pyplot() to display the plot in Streamlit
                    # Create a histogram for the column
                    fig, ax = plt.subplots(figsize=(12, 6))

                    # Create a list of colors with the same length as the number of columns
                    colors = ['skyblue', 'lightcoral', 'lightgreen', 'purple']  # You can choose your preferred colors

                    for i, col in enumerate(numeric_columns, 1):
                        ax.hist(file_data[1][col], bins=20, alpha=0.7, label=col, color=colors[i % len(colors)])
                        ax.set_xlabel("Values")
                        ax.set_ylabel("Frequency")
                    ax.set_title("Histograms of Numeric Columns")
                    ax.legend()
                    st.pyplot(fig)  # Use st.pyplot() to display the plot in Streamlit

                    st.markdown("##### Skewness")
                    skewness = file_data[1][numeric_columns].skew()
                    # Create a bar chart for skewness
                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.bar(numeric_columns, skewness)
                    ax.set_xlabel("Numeric Columns")
                    ax.set_ylabel("Skewness")
                    ax.set_title("Skewness of Numeric Columns")
                    st.pyplot(fig)
                    st.write(f"Skewbess: {skewness}")
        except Exception as e:
            st.error(e)