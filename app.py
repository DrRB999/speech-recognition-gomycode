import io

import speech_recognition as sr
import streamlit as st


st.set_page_config(
    page_title="Speech Recognition App",
    page_icon="🎙️",
    layout="centered",
)

st.title("🎙️ Speech Recognition App")
st.markdown(
    """
    Record your voice, choose a recognition engine and language, then transcribe it.

    **How to use**
    1. Choose a speech recognition API.
    2. Choose the language you are speaking.
    3. Record an audio message.
    4. Use **Pause** / **Resume** to control the recognition process.
    5. Click **Transcribe recording**.
    6. Download the transcription as a text file.
    """
)

if "paused" not in st.session_state:
    st.session_state.paused = False

if "transcription" not in st.session_state:
    st.session_state.transcription = ""

api_choice = st.selectbox(
    "Speech recognition API",
    ["Google Speech Recognition", "CMU Sphinx"],
    help="Google uses an online speech service. CMU Sphinx works offline when PocketSphinx is installed.",
)

language_options = {
    "English (US)": "en-US",
    "English (UK)": "en-GB",
    "French": "fr-FR",
    "Arabic": "ar-SA",
    "German": "de-DE",
    "Spanish": "es-ES",
    "Italian": "it-IT",
}

language_name = st.selectbox("Language", list(language_options.keys()))
language_code = language_options[language_name]

if api_choice == "CMU Sphinx" and language_code != "en-US":
    st.info(
        "CMU Sphinx supports en-US out of the box. Other languages require the corresponding PocketSphinx language model."
    )

control_col1, control_col2 = st.columns(2)

with control_col1:
    if st.button("⏸️ Pause", use_container_width=True):
        st.session_state.paused = True

with control_col2:
    if st.button("▶️ Resume", use_container_width=True):
        st.session_state.paused = False

if st.session_state.paused:
    st.warning("Speech recognition is paused.")
else:
    st.success("Speech recognition is ready.")

audio_value = st.audio_input(
    "Record your voice",
    sample_rate=16000,
    disabled=st.session_state.paused,
)

if audio_value is not None:
    st.audio(audio_value)


def transcribe_speech(audio_file, api_name, language):
    """Convert recorded speech to text with meaningful error handling."""
    recognizer = sr.Recognizer()

    try:
        audio_bytes = audio_file.getvalue()

        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)

        if api_name == "Google Speech Recognition":
            return recognizer.recognize_google(audio_data, language=language)

        if api_name == "CMU Sphinx":
            return recognizer.recognize_sphinx(audio_data, language=language)

        raise ValueError("Unsupported speech recognition API.")

    except sr.UnknownValueError:
        st.error(
            "The speech could not be understood. Try speaking more clearly or recording in a quieter environment."
        )

    except sr.RequestError as error:
        st.error(
            "The speech recognition service could not be reached. "
            f"Details: {error}"
        )

    except FileNotFoundError:
        st.error(
            "A required recognition model or dependency is missing. For CMU Sphinx, install the required PocketSphinx language model."
        )

    except Exception as error:
        st.error(
            "An unexpected error occurred while transcribing the audio. "
            f"Details: {error}"
        )

    return None


transcribe_disabled = st.session_state.paused or audio_value is None

if st.button(
    "📝 Transcribe recording",
    type="primary",
    disabled=transcribe_disabled,
    use_container_width=True,
):
    with st.spinner("Transcribing..."):
        result = transcribe_speech(audio_value, api_choice, language_code)

    if result:
        st.session_state.transcription = result

if st.session_state.transcription:
    st.subheader("Transcribed text")

    edited_text = st.text_area(
        "Review or edit the transcription",
        value=st.session_state.transcription,
        height=180,
    )

    st.session_state.transcription = edited_text

    st.download_button(
        label="💾 Save transcription as TXT",
        data=edited_text.encode("utf-8"),
        file_name="transcription.txt",
        mime="text/plain",
        use_container_width=True,
    )

    if st.button("🗑️ Clear transcription", use_container_width=True):
        st.session_state.transcription = ""
        st.rerun()
