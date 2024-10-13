import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from pydub import AudioSegment
import io
from streamlit_TTS import text_to_speech


audio_bytes = audio_recorder(text="Click to Test",
   recording_color="#e8b62c",
   neutral_color="#6aa36f",
   icon_name="user",
   icon_size="6x",)



# Function to convert audio file to text
def convert_audio_to_text(audio_bytes):
   # Load audio bytes into AudioSegment
   audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
   # Save to a temporary wav file
   temp_wav_path = "temp.wav"
   audio_segment.export(temp_wav_path, format="wav")
   print('file done')
   # Initialize recognizer
   recognizer = sr.Recognizer()
   with sr.AudioFile(temp_wav_path) as source:
      audio_data = recognizer.record(source)
      text = recognizer.recognize_google(audio_data)
   return text

def temp_text_to_speech(text):
   text_to_speech(text, language='en')

if audio_bytes:
   st.audio(audio_bytes, format="audio/wav")
   if st.button("Convert to Text"):
      try:
         text_output = convert_audio_to_text(audio_bytes)
         st.success("Conversion Successful!")
         st.write(text_output)
         temp_text_to_speech("This sounds like an important phone call. Anjie will call you later.")
      except Exception as e:
         print(f"Error: {e}")