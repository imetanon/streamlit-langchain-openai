import azure.cognitiveservices.speech as speechsdk
import streamlit as st
import time

chunks = []

def create_speech_recognizer():
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language="th-TH"
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    return recognizer

def start_continuous_recognition():
    recognizer = create_speech_recognizer()

    st.session_state['done'] = False

    def recognizing_cb(evt):
        chunks.append(evt.result.text)
        print(f"RECOGNIZING: {evt.result.text}")

    def recognized_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            chunks.append(evt.result.text)
            print(f"RECOGNIZED: {evt.result.text}")
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("NOMATCH: Speech could not be recognized.")
        elif evt.result.reason == speechsdk.ResultReason.Canceled:
            print(f"CANCELED: {evt.result.cancellation_details.reason}")

    def session_started_cb(evt):
        print(f"SESSION STARTED: {evt}")

    def session_stopped_cb(evt):
        print(f"SESSION STOPPED {evt}")
        recognizer.stop_continuous_recognition()
        st.session_state['done'] = True

    # recognizer.recognizing.connect(recognizing_cb)
    recognizer.recognized.connect(recognized_cb)
    recognizer.session_started.connect(session_started_cb)
    recognizer.session_stopped.connect(session_stopped_cb)

    recognizer.start_continuous_recognition()

    st.info("Say something...")

    while not st.session_state['done']:
        if chunks:
            st.chat_message("AI",avatar=":material/graphic_eq:").write(chunks[0])
            chunks.clear()
        time.sleep(0.5)

def stop_continuous_recognition():
    st.session_state['done'] = True


st.set_page_config(page_title="Speech to text", page_icon="🤖")

st.title("Speech to text")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    service_region = st.text_input("Service Region", key="service_region", type="default")
    speech_key = st.text_input("Speech Key", key="speech_key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")

if not service_region:
    st.info("Please add your Service Region to continue.")

if not speech_key:
    st.info("Please add your Speech to continue.")
else:
    if st.button("Start Recognition"):
        if st.button("Stop Recognition"):
            stop_continuous_recognition()
        start_continuous_recognition()

