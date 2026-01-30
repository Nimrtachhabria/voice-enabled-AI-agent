import os
import tempfile
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from st_audiorec import st_audiorec
from deepgram import Deepgram

load_dotenv()
try:
    from rag.retriever import get_retriever
    from rag.prompts import SYSTEM_PROMPT
    from rag.llms import ask_gemini, ask_deepseek
except ImportError as e:
    st.error(f"Module import error: {e}")
    st.info("Please check your directory structure: rag/retriever.py, rag/prompts.py, rag/llms.py should exist")

# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(
    page_title="Sunmarke Voice AI Agent",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 Sunmarke School Voice AI Agent")
st.caption("Ask questions using your voice or text and compare AI models")

# --------------------------------------------------
# Session state
# --------------------------------------------------
st.session_state.setdefault("query", "")
st.session_state.setdefault("show_results", False)

# --------------------------------------------------
# Deepgram setup
# --------------------------------------------------
deepgram = Deepgram(os.getenv("DEEPGRAM_API_KEY"))


# --------------------------------------------------
# Browser Text To Speech
# --------------------------------------------------
def speak_browser(text):
    safe = text.replace('"', "").replace("\n", " ")
    js = f"""
    <script>
        const msg = new SpeechSynthesisUtterance("{safe}");
        msg.lang = "en-US";
        msg.rate = 1;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js, height=0)

# --------------------------------------------------
# Voice input UI
# --------------------------------------------------
st.markdown("## 🎙️ Voice Input")

audio = st_audiorec()

# ---------------------------------
# Deepgram transcription function
# ---------------------------------
import asyncio
def transcribe_with_deepgram(audio_path):
    async def run():
        with open(audio_path, "rb") as audio:
            source = {"buffer": audio, "mimetype": "audio/wav"}

            response = await deepgram.transcription.prerecorded(
                source,
                {
                    "punctuate": True,
                    "language": "en",
                    "model": "nova"
                }
            )
            return response

    response = asyncio.run(run())

    return response["results"]["channels"][0]["alternatives"][0]["transcript"]


# ---------------------------------
# Voice input handling
# ---------------------------------
if audio is not None:
    st.success("Recording completed")

    if st.button("Submit voice question", type="primary"):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio)
            audio_path = f.name

        with st.spinner("Converting speech to text..."):
            transcript = transcribe_with_deepgram(audio_path)

        if transcript and transcript.strip():
            st.success("Voice converted successfully")
            st.write("Your question:", transcript)
            
            st.session_state.query = transcript
            st.session_state.show_results = True

         
        else:
            st.error("No speech detected")
# --------------------------------------------------
# Text fallback
# --------------------------------------------------
st.markdown("## ⌨️ Or type your question")

text_q = st.text_input("Type here")

if st.button("Submit text question"):
    if text_q.strip():
        st.session_state.query = text_q
        st.session_state.show_results = True
        st.rerun()

# --------------------------------------------------
# RAG + LLM
# --------------------------------------------------
if st.session_state.query and st.session_state.show_results:

    st.divider()
    st.subheader("🔍 Knowledge Search")

    with st.spinner("Searching school website content..."):
        retriever = get_retriever()
        docs = retriever.invoke(st.session_state.query)

        if len(docs) == 0:
            context = ""
            st.warning("No documents found")
        else:
            context = "\n\n".join(d.page_content for d in docs)

    final_prompt = f"""
{SYSTEM_PROMPT}

CONTEXT:
{context}

QUESTION:
{st.session_state.query}

Answer only using the context above.
If not found, say you do not have that information.
"""

    st.divider()
    st.subheader("🤖 AI Model Comparison")

    col1, col2 = st.columns(2)

    def model_card(col, name, func):
        with col:
            st.markdown(f"### {name}")

            with st.spinner("Thinking..."):
                try:
                    answer = func(final_prompt)
                    st.write(answer)

                    if st.button(f"🔊 Play {name}", key=name):
                        speak_browser(answer)

                except Exception as e:
                    st.error(str(e))

    model_card(col1, "Gemini", ask_gemini)
    
    model_card(col2, "DeepSeek", ask_deepseek)

    st.divider()
    if st.button("Ask another question"):
        st.session_state.query = ""
        st.session_state.show_results = False
        st.rerun()




