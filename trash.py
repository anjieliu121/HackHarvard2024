
import speech_recognition as sr
from pydub import AudioSegment
import io
from streamlit_TTS import text_to_speech
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from chat import Chat






# Function to convert audio file to text
def convert_audio_to_text(chatInstance, audio_bytes):
   try:
      # Load audio bytes into AudioSegment
      audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
      # Save to a temporary wav file
      temp_wav_path = "temp.wav"
      audio_segment.export(temp_wav_path, format="wav")
      # Initialize recognizer
      recognizer = sr.Recognizer()
      with sr.AudioFile(temp_wav_path) as source:
         audio_data = recognizer.record(source)
         text = recognizer.recognize_google(audio_data)
         st.write(text)
      st.success("Conversion Successful!")
   except Exception as e:
      text = "Mumbling"
   return text

def convert_text_to_speech(text):
   text_to_speech(text, language='en')

def record_audio(chatInstance, key, automatic=False):
   if automatic:
      audio_bytes = audio_recorder(key=key, auto_start=True)


   else:

      #chatInstance.reset()
      print("hi")
      audio_bytes = audio_recorder(text="Click to Test",
                                   recording_color="#e8b62c",
                                   neutral_color="#6aa36f",
                                   icon_name="user",
                                   icon_size="6x",
                                   auto_start=False,
                                   key = key)
      print(audio_bytes)

   # st.audio(audio_bytes, format="audio/wav")
   if audio_bytes:
      return convert_audio_to_text(chatInstance, audio_bytes)
   if not audio_bytes:
      return "Mumbling."


# first conversation: User
c = Chat()
c.reset()
text_output = record_audio(c, key='0')
print("1.0", text_output)
print("This is kinda insane.")

# first conversation: AUTO
response = c.handle_message(text_output)
convert_text_to_speech(response)
print("1.1", response)

# second conversation: User
text_output = record_audio(c, key='1', automatic=False)
print("2.0", text_output)

# second conversation: AUTO
response = c.handle_message(text_output)
convert_text_to_speech(response)
print("2.1", response)

# third conversation: User
text_output = record_audio(c, key='2', automatic=False)
print("3.0", text_output)

# third conversation: AUTO
response = c.final_response(text_output)
convert_text_to_speech(response)
print("3.1", response)

#st.stop()
st.cache_data.clear()