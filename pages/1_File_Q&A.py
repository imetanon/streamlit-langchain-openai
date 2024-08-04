import tempfile
import os
import streamlit as st
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate


def get_vectorstore_from_file(path, file_name):
    loader = PyMuPDFLoader(path)
    document = loader.load()

    # split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    document_chunks = text_splitter.split_documents(document)

    # create a vectorstore from the chunks
    vector_store = Chroma.from_documents(documents=document_chunks, embedding=OpenAIEmbeddings(model="text-embedding-3-small",api_key=openai_api_key))

    return vector_store

def get_conversational_rag_chain(retriever):

    llm = ChatOpenAI(model="gpt-4o", api_key=openai_api_key)

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise. Please correct the word or pharse if it incorrect."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, stuff_documents_chain)

def get_response(user_input):
    retriever = st.session_state.vector_store.as_retriever()
    conversation_rag_chain = get_conversational_rag_chain(retriever)
    
    response = conversation_rag_chain.invoke({
        "input": user_input
    })
    
    return response


st.set_page_config(page_title="📝 File Q&A with OpenAI", page_icon="🤖")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("📝 File Q&A with OpenAI")

uploaded_file = st.file_uploader("Upload an article", type=("txt", "pdf"))

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
else:
    # session state
    if "vector_store" not in st.session_state:
        if uploaded_file:
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, uploaded_file.name)
            with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.session_state.vector_store = get_vectorstore_from_file(path, uploaded_file.name)
        else:
            st.info("Please upload file.")

    question = st.text_input(
        "Ask something about the file content",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if question is not None and question != "":
        response = get_response(question)

        st.write("### Answer")
        st.write(response["answer"])

        pages_context = [context.metadata["page"] + 1 for context in response["context"]]
        unique_sorted_list = sorted(set(pages_context))

        # Creating the reference text
        reference_txt = "Reference Pages: " + ", ".join(map(str, unique_sorted_list))

        # Displaying the caption
        st.caption(reference_txt)