import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


st.set_page_config(
    page_title="AI Voice Transcriber",
    page_icon="🎙️",
    layout="centered",
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    body, .stApp { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 2rem; max-width: 780px; }
    .stTextArea textarea { font-size: 15px; }
    .stDownloadButton > button { width: 100%; }
</style>
""", unsafe_allow_html=True)


st.title("🎙️ AI Voice Transcriber")
st.write("Record your voice **or** upload an audio file and transcribe it instantly with OpenAI Whisper.")
st.divider()


if not api_key:
    st.error(
        " **OPENAI_API_KEY not found.**\n\n"
        "Create a `.env` file in this folder:\n```\nOPENAI_API_KEY=sk-...\n```"
    )
    st.stop()

client = OpenAI(api_key=api_key)


with st.sidebar:
    st.header(" Options")
    language = st.selectbox(
        "Audio language",
        ["Auto-detect", "en", "hi", "fr", "de", "es", "zh", "ar", "ja", "pt"],
        help="Correct language improves accuracy.",
    )
    response_format = st.selectbox(
        "Output format",
        ["text", "srt", "vtt", "verbose_json"],
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.1)
    st.divider()
    st.caption("Supported: mp3 · mp4 · m4a · wav · webm")
    st.caption("Max file size: **25 MB**")


tab1, tab2 = st.tabs([" Record Voice", " Upload File"])

audio_bytes = None
input_name  = "recording.wav"


with tab1:
    st.markdown("#### Record from your microphone")

    try:
        from audiorecorder import audiorecorder
        audio_seg = audiorecorder(" Start Recording", " Stop Recording")
        if len(audio_seg) > 0:
            wav_bytes = audio_seg.export().read()
            st.audio(wav_bytes, format="audio/wav")
            audio_bytes = wav_bytes
            input_name  = "recording.wav"
            st.success(" Recording ready — press **Transcribe** below.")
    except ImportError:
        st.warning(
            "**One extra package needed for live recording:**\n\n"
            "```bash\npip install streamlit-audiorecorder\n```\n\n"
            "Restart the app after installing.  \n"
            "Or use the **Upload File** tab in the meantime."
        )


with tab2:
    st.markdown("#### Upload an audio file")
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"],
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        c1, c2 = st.columns(2)
        c1.metric("File", uploaded_file.name)
        c2.metric("Size", f"{file_size_mb:.2f} MB")

        if file_size_mb > 25:
            st.error(" File exceeds 25 MB. Please compress or split it.")
            st.stop()

        st.audio(uploaded_file, format=uploaded_file.type)
        audio_bytes = uploaded_file.read()
        input_name  = uploaded_file.name


st.divider()

if audio_bytes:
    if st.button(" Transcribe", use_container_width=True, type="primary"):
        suffix = Path(input_name).suffix or ".wav"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            with st.spinner("Transcribing…"):
                kwargs = {
                    "model": "whisper-1",
                    "response_format": response_format,
                    "temperature": temperature,
                }
                if language != "Auto-detect":
                    kwargs["language"] = language

                with open(tmp_path, "rb") as af:
                    transcript = client.audio.transcriptions.create(file=af, **kwargs)

            if response_format == "verbose_json":
                result_text = transcript.text
                st.success("Transcription complete!")
                st.subheader(" Transcribed Text")
                st.write(result_text)
                with st.expander(" Full JSON"):
                    st.json(transcript.model_dump())
            else:
                result_text = transcript
                st.success(" Transcription complete!")
                st.subheader(" Transcribed Text")
                st.text_area("", value=result_text, height=300, label_visibility="collapsed")

            m1, m2 = st.columns(2)
            m1.metric("Words", len(result_text.split()))
            m2.metric("Characters", len(result_text))

            ext_map = {"text": "txt", "srt": "srt", "vtt": "vtt", "verbose_json": "txt"}
            dl_name = Path(input_name).stem + f"_transcript.{ext_map.get(response_format,'txt')}"
            st.download_button(" Download Transcript", data=result_text,
                               file_name=dl_name, mime="text/plain",
                               use_container_width=True)

        except Exception as e:
            st.error(f" Transcription failed: {e}")
        finally:
            os.remove(tmp_path)
else:
    st.info(" Record your voice or upload a file above, then hit **Transcribe**.")
