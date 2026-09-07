# Speech Recognition App — GoMyCode Checkpoint

A Streamlit speech-recognition application improved according to the GoMyCode checkpoint requirements.

## Features
1. **Speech recognition API selection**
   - Google Speech Recognition
   - CMU Sphinx

2. **Improved error handling**
   - Unrecognized speech
   - API/service errors
   - Missing dependencies/models
   - Unexpected errors

3. **Save transcription**
   - Download the recognized text as a `.txt` file.

4. **Language selection**
   - English (US)
   - English (UK)
   - French
   - Arabic
   - German
   - Spanish
   - Italian

5. **Pause and resume**
   - Pause disables recording/transcription.
   - Resume re-enables the recognition workflow.

## Technical choices

The app uses Streamlit's browser microphone widget (`st.audio_input`) so the user can record directly in the web interface.

Speech transcription is performed with the Python `SpeechRecognition` library:
- `recognize_google()` for Google Speech Recognition.
- `recognize_sphinx()` for CMU Sphinx.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- Google Speech Recognition requires an internet connection.
- CMU Sphinx requires PocketSphinx.
- CMU Sphinx includes US English support out of the box; other languages may require additional language models.
