import tempfile
import os
import streamlit as st
from openai import AzureOpenAI

st.set_page_config(page_title="Whisper Model in Azure OpenAI Service", page_icon="🤖")

with st.sidebar:
    azure_open_api_key = st.text_input("Azure OpenAI API Key", key="azure_open_api_key", type="password")
    azure_open_api_endpoint = st.text_input("Azure OpenAI Endpoint", key="azure_open_api_endpoint", type="default")
    deployment_id = st.text_input("Deployment Name", key="deployment_id", type="default")


st.title("Whisper Model in Azure OpenAI Service")

uploaded_file = st.file_uploader("Upload Audio File")


if not azure_open_api_key:
    st.info("Please add your Azure OpenAI API key to continue.")
if not azure_open_api_endpoint:
    st.info("Please add your Azure OpenAI Endpoint to continue.")
if not deployment_id:
    st.info("Please add your Deployment Name to continue.")
else:
    if uploaded_file:
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getvalue())

        st.audio(path, loop=True)
        
        client = AzureOpenAI(
            api_key=azure_open_api_key,  
            api_version="2024-02-01",
            azure_endpoint=azure_open_api_endpoint
        )

        with st.spinner('Transcribing audio...'):
            # Create the transcription
            result = client.audio.transcriptions.create(
                file=open(path, "rb"),            
                model=deployment_id
            )

        st.write(result.text)

    else:
        st.info("Please upload file.")
