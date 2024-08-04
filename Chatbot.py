from langchain_openai import ChatOpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI and LangChain")

def generate_response(input_text):
    model = ChatOpenAI(api_key=openai_api_key)
    return model.invoke(input_text)


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.warning("Please enter your OpenAI API key!", icon="⚠")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = generate_response(prompt)
    msg = response.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)